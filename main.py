from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os


# ============================================================
# CONFIGURATION
# ============================================================

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

app = FastAPI(
    title="News Search API",
    description="A FastAPI service for retrieving structured news search results.",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ENDPOINT
# ============================================================

@app.get("/api/news-search")
async def news_search(
    query: str = Query(
        ...,
        description="The topic, keyword, person, organization or event to search for."
    ),

    gl: str = Query(
        "us",
        description="Two-letter country code for localized results."
    ),

    hl: str = Query(
        "en",
        description="Two-letter language code for the search."
    )
):

    if not SERPAPI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="SERPAPI_API_KEY environment variable is not configured."
        )


    # ========================================================
    # SERPAPI PARAMETERS
    # ========================================================

    params = {
        "engine": "google_news",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "gl": gl,
        "hl": hl
    }


    # ========================================================
    # API REQUEST
    # ========================================================

    try:

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        raise HTTPException(
            status_code=504,
            detail="News search request timed out."
        )

    except requests.exceptions.RequestException as e:

        raise HTTPException(
            status_code=503,
            detail=f"Error communicating with the search service: {e}"
        )


    # ========================================================
    # EXTRACT NEWS RESULTS
    # ========================================================

    news_results = data.get("news_results", [])

    structured_results = []


    for result in news_results:

        source = result.get("source", {})

        structured_results.append({

            "title": result.get(
                "title",
                "N/A"
            ),

            "summary": result.get(
                "snippet",
                "No summary available."
            ),

            "source": source.get(
                "name",
                "Unknown"
            ),

            "link": result.get(
                "link",
                "#"
            ),

            "date": result.get(
                "date",
                ""
            ),

            "iso_date": result.get(
                "iso_date",
                ""
            ),

            "type": result.get(
                "type",
                ""
            ),

            "position": result.get(
                "position"
            )
        })


    # ========================================================
    # STRUCTURED RESPONSE
    # ========================================================

    return {

        "status": "success",

        "search_parameters": {

            "query": query,

            "country": gl,

            "language": hl

        },

        "results_count": len(
            structured_results
        ),

        "news_results": structured_results,

        "search_metadata": data.get(
            "search_metadata"
        )
    }
