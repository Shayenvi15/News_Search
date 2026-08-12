# NewsSearch API Playground

### Localized News Retrieval with FastAPI & SerpApi

A lightweight **news search API and interactive playground** built with **FastAPI, JavaScript, Tailwind CSS, and SerpApi**.

The project provides a REST API that accepts a search topic, country, and language, retrieves relevant news results through an external search service, and transforms the response into a clean, structured JSON format.

The accompanying frontend provides a simple playground for interacting with the API and inspecting the returned data.

---

## ✨ Overview

NewsSearch demonstrates a practical:

**Frontend → REST API → External Search Service → Structured Response**

workflow.

```text
┌─────────────────────┐
│    User / Browser   │
│                     │
│  Search Topic       │
│  Country            │
│  Language           │
└──────────┬──────────┘
           │
           │ HTTP GET
           ▼
┌─────────────────────┐
│      FastAPI        │
│                     │
│  /api/news-search   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Query Processing  │
│                     │
│  q + gl + hl        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      SerpApi        │
│    Google News      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Structured JSON     │
│                     │
│ News Results        │
│ Source              │
│ Links               │
│ Dates               │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Browser / Client  │
└─────────────────────┘
