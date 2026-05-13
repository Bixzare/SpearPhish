import requests
import joblib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import whois
import pandas as pd


class URLPhishingDetector:
  """
  Detect phishing URLs using Layer 2 and Layer 3 features.
  This is adapted from the L2 notebook for use in the backend.
  """

  def __init__(
    self,
    model_path: str = "l2_l3_xgboost_model.pkl",
    scaler_path: str = "scaler.joblib",
    tld_map_path: str = "l2_l3_tld_map.pkl",
  ) -> None:
    self.model_path = model_path
    self.scaler_path = scaler_path
    self.tld_map_path = tld_map_path
    self._model = None
    self._scaler = None
    self._tld_map = None

  @property
  def model(self):
    if self._model is None:
      self._model = joblib.load(self.model_path)
    return self._model

  @property
  def scaler(self):
    if self._scaler is None:
      self._scaler = joblib.load(self.scaler_path)
    return self._scaler

  @property
  def tld_map(self):
    if self._tld_map is None:
      self._tld_map = joblib.load(self.tld_map_path)
    return self._tld_map

  @staticmethod
  def get_tld(url: str) -> str:
    try:
      domain = urlparse(url).netloc
      if not domain:
        return "none"
      parts = domain.split(".")
      if len(parts) > 1:
        return (
          ".".join(parts[-2:])
          if len(parts[-1]) == 2 and len(parts[-2]) <= 3
          else parts[-1]
        )
      return "none"
    except Exception:
      return "error"

  def analyze_redirects(self, start_url: str):
    l2_features = {
      "hop_count": -1,
      "uses_url_shortener": 0,
      "final_url_tld": "none",
    }

    redirect_chain = []
    current_url = str(start_url)
    max_hops = 10

    try:
      if urlparse(current_url).netloc in [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "buff.ly",
      ]:
        l2_features["uses_url_shortener"] = 1
    except Exception:
      pass

    try:
      for _ in range(max_hops):
        response = requests.head(
          current_url,
          allow_redirects=False,
          timeout=5,
          headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
          },
        )
        redirect_chain.append(current_url)

        if 300 <= response.status_code < 400 and "Location" in response.headers:
          next_url = response.headers["Location"]
          if not urlparse(next_url).netloc:
            next_url = requests.compat.urljoin(current_url, next_url)
          current_url = next_url
        else:
          break

      l2_features["hop_count"] = len(redirect_chain) - 1

    except requests.exceptions.RequestException:
      return None, l2_features

    final_url = current_url
    l2_features["final_url_tld"] = self.get_tld(final_url)
    return final_url, l2_features

  def analyze_html(self, url: str):
    l3_features = {
      "num_script_tags": -1,
      "has_password_field": -1,
      "num_external_links": -1,
      "dom_depth": -1,
    }

    if not url:
      return l3_features

    try:
      response = requests.get(
        url,
        timeout=10,
        headers={
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36"
        },
      )
      response.raise_for_status()

      soup = BeautifulSoup(response.content, "html.parser")

      l3_features["num_script_tags"] = len(soup.find_all("script"))
      l3_features["has_password_field"] = (
        1 if soup.find("input", {"type": "password"}) else 0
      )

      external_links = 0
      current_domain = urlparse(url).netloc
      for link in soup.find_all("a", href=True):
        link_domain = urlparse(link["href"]).netloc
        if link_domain and link_domain != current_domain:
          external_links += 1
      l3_features["num_external_links"] = external_links

      def get_depth(element, depth):
        if not hasattr(element, "children"):
          return depth
        max_child_depth = depth
        for child in element.children:
          if getattr(child, "name", None):
            child_depth = get_depth(child, depth + 1)
            if child_depth > max_child_depth:
              max_child_depth = child_depth
        return max_child_depth

      l3_features["dom_depth"] = get_depth(soup, 0)

    except requests.exceptions.RequestException:
      pass
    except Exception:
      pass

    return l3_features

  def preprocess_url(self, url: str):
    final_url, l2_features = self.analyze_redirects(url)

    if l2_features["hop_count"] == -1:
      raise ConnectionError(f"Unable to connect to URL: {url}")

    if final_url:
      l3_features = self.analyze_html(final_url)
    else:
      l3_features = {
        "num_script_tags": -1,
        "has_password_field": -1,
        "num_external_links": -1,
        "dom_depth": -1,
      }

    combined_features = {
      "hop_count": l2_features["hop_count"],
      "uses_url_shortener": l2_features["uses_url_shortener"],
      "num_script_tags": l3_features["num_script_tags"],
      "has_password_field": l3_features["has_password_field"],
      "num_external_links": l3_features["num_external_links"],
      "dom_depth": l3_features["dom_depth"],
    }

    tld = l2_features["final_url_tld"]
    combined_features["final_url_tld_freq"] = self.tld_map.get(tld, 1)

    feature_columns = [
      "hop_count",
      "uses_url_shortener",
      "num_script_tags",
      "has_password_field",
      "num_external_links",
      "dom_depth",
      "final_url_tld_freq",
    ]

    features_df = pd.DataFrame([combined_features], columns=feature_columns)

    # Model was retrained without scaling; keep this aligned with notebook comment.
    scaled_features = features_df
    return combined_features, scaled_features

  def predict(self, url: str, return_probability: bool = False):
    features_dict, scaled_features = self.preprocess_url(url)

    if return_probability:
      probabilities = self.model.predict_proba(scaled_features)[0]
      prediction = {
        "benign": float(probabilities[0]),
        "phishing": float(probabilities[1]),
      }
      confidence = float(max(probabilities))
    else:
      pred = self.model.predict(scaled_features)[0]
      probabilities = self.model.predict_proba(scaled_features)[0]
      prediction = "phishing" if pred == 1 else "benign"
      confidence = float(probabilities[pred])

    return {
      "url": url,
      "prediction": prediction,
      "confidence": confidence,
      "features": features_dict,
    }


def analyze_url(url: str) -> str:
  """
  Wrapper around the Layer 2/3 URL phishing detector.
  Accepts a URL string and returns a simple human-readable summary.
  """
  if not isinstance(url, str):
    raise ValueError("URL must be a string")
  if not url or url.strip() == "":
    raise ValueError("Empty URL - nothing to analyze")

  detector = URLPhishingDetector()
  result = detector.predict(url)
  label = result["prediction"]
  confidence_pct = result["confidence"] * 100

  return f"Layer 2/3 URL analysis: {label} (confidence {confidence_pct:.2f}%)."

