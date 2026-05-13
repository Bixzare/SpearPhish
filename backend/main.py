from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import traceback

from text_classification import classify_email_text
from link_analysis import analyze_url


class TextRequest(BaseModel):
    text: str


class LinkRequest(BaseModel):
    url: str


class TextResponse(BaseModel):
    result: str


class LinkResponse(BaseModel):
    result: str


app = FastAPI(title="SpearPhish Backend")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/classify-text", response_model=TextResponse)
async def classify_text(payload: TextRequest) -> TextResponse:
    """
    Layer 1 text classification endpoint.
    Takes raw email text and returns a simple summary string.
    """
    try:
        result_text = classify_email_text(payload.text)
        return TextResponse(result=result_text)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Model files not found: {str(e)}. Please ensure model files are in the backend directory."
        )
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


@app.post("/analyze-link", response_model=LinkResponse)
async def analyze_link(payload: LinkRequest) -> LinkResponse:
    """
    Layer 2/3 link analysis endpoint.
    Takes a URL and returns a simple summary string.
    """
    try:
        result_text = analyze_url(payload.url)
        return LinkResponse(result=result_text)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Model files not found: {str(e)}. Please ensure model files are in the backend directory."
        )
    except ConnectionError as e:
        print(f"Connection error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Unable to connect to URL: {str(e)}"
        )
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Link analysis failed: {str(e)}"
        )


@app.get("/health")
async def health():
    return {"status": "ok"}
