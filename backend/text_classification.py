import re
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

_VECTORIZER_CACHE = None
_MODEL_CACHE = None


def _ensure_nltk_data() -> None:
  try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
  except LookupError:
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)


def _load_vectorizer(vectorizer_path: str = "l1_vectorizer.pkl"):
  global _VECTORIZER_CACHE
  if _VECTORIZER_CACHE is None:
    _VECTORIZER_CACHE = joblib.load(vectorizer_path)
  return _VECTORIZER_CACHE


def _load_model(model_path: str = "l1_nlp_model.pkl"):
  global _MODEL_CACHE
  if _MODEL_CACHE is None:
    _MODEL_CACHE = joblib.load(model_path)
  return _MODEL_CACHE


def classify_email_text(email_text: str) -> str:
  """
  End-to-end helper that:
  - preprocesses the raw email text
  - runs the trained model
  - returns a simple human-readable summary string
  """
  if not isinstance(email_text, str):
    raise ValueError("Input must be a string")

  if not email_text or email_text.strip() == "":
    raise ValueError("Empty string - no content to process")

  _ensure_nltk_data()

  # Load vectorizer and model (cached)
  vectorizer = _load_vectorizer()
  model = _load_model()

  # Basic cleaning (mirrors the notebook logic but kept compact)
  text = email_text.replace(u"\u00a0", " ")
  text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
  text = re.sub(r"[-_=]{4,}", "", text)
  text = text.lower()
  text = re.sub(r"http\S+|www\S+|https\S+", " _URL_ ", text, flags=re.MULTILINE)
  text = re.sub(r"[\w\.-]+@[\w\.-]+", " _EMAIL_ ", text, flags=re.MULTILINE)
  text = re.sub(r"\d+", " _NUM_ ", text, flags=re.MULTILINE)

  try:
    tokens = word_tokenize(text)
  except Exception:
    tokens = text.split()

  lemmatizer = WordNetLemmatizer()
  stop_words = set(stopwords.words("english"))
  email_junk = {
    "re",
    "fw",
    "fwd",
    "subject",
    "date",
    "from",
    "to",
    "cc",
    "spama",
    "spamassassin",
    "razor",
    "exmh",
    "rpm-l",
    "nbsp",
    "html",
    "font",
    "http",
    "https",
  }
  stop_words.update(email_junk)

  clean_tokens = []
  for word in tokens:
    if word in ["_URL_", "_EMAIL_", "_NUM_"]:
      clean_tokens.append(word)
    elif word.isalpha() and word not in stop_words:
      clean_tokens.append(word)

  lemmatized_tokens = [lemmatizer.lemmatize(token) for token in clean_tokens]
  cleaned_text = " ".join(lemmatized_tokens)

  if not cleaned_text.strip():
    raise ValueError("Empty string after preprocessing - no meaningful content")

  features = vectorizer.transform([cleaned_text])
  prediction = model.predict(features)[0]
  probabilities = model.predict_proba(features)[0]
  class_labels = model.classes_
  prob_dict = {label: prob for label, prob in zip(class_labels, probabilities)}
  predicted_confidence = prob_dict[prediction]

  label = "phishing" if prediction == "Phishing Email" else "legitimate"
  confidence_pct = predicted_confidence * 100

  return f"Layer 1 classification: {label} (confidence {confidence_pct:.2f}%)."


