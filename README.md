# 🔍 Business Finder Assistant

A conversational local business discovery assistant built using Python, Streamlit, and an intent-driven LLM router.

The assistant helps users discover nearby businesses (mechanics, garages, services, etc.) **only from a private database**, with a controlled fallback to online search when data is missing.

---

## 🚀 Features

- Intent-based routing (NOT a free-form chatbot)
- SQL-only database access (safe by design)
- Smart business ranking (rating, reviews, freshness)
- Bot & abuse detection
- Online fallback via Google Maps (SerpAPI)
- Missing-query logging for dataset improvement
- Human-like responses without exposing SQL or logic

---

## 🧠 Supported Intents

| Intent       | Description |
|--------------|------------|
| `sql_search` | Business or service discovery |
| `about`      | Platform purpose |
| `faq`        | How it works / why use it |
| `chat`       | Greetings & casual queries |

---

## 🗂️ Database Schema

Table: `google_maps_listings`

```text
id, name, address, website, phone_number,
reviews_count, reviews_average,
category, subcategory,
city, state, area,
created_at
```

## Create a .env file 
```
OPEN_ROUTER_API_KEY=your_openrouter_key
SERPAPI_KEY=your_serpapi_key
```

# Flow:
```
User Input (Streamlit UI)
        ↓
Bot & Abuse Detection
(bot_detector.py)
        ↓
LLM Intent Routing
(llm_router.py + OpenRouter)
        ↓
┌───────────────────────────────┐
│ Intent Classification Result  │
└───────────────────────────────┘
        ↓
────────────────────────────────────────
│                                      │
│ 1️⃣ sql_search                       │
│ 2️⃣ about / faq / chat               │
│                                      │
────────────────────────────────────────
```

```
User Query
   ↓
LLM generates:
- intent = sql_search
- safe SELECT SQL
   ↓
SQL Execution (db.py)
(SQLite database)
   ↓
Raw Results (up to 200 rows)
   ↓
Ranking & Filtering (dp.py)
- remove closed businesses
- deduplicate entries
- rating confidence adjustment
- popularity scoring
- freshness bonus
   ↓
Top-N Results (default = 10)
   ↓
Human-readable response
(Streamlit UI)
```

```
SQL returns 0 rows
        ↓
SerpAPI Google Maps Search
(serpapi_search.py)
        ↓
Display limited online results
        ↓
Log missing query
(missing_data_logger.py)
        ↓
Used later to improve database coverage
```

```
User Query
   ↓
LLM Intent Router
   ↓
about / faq / chat
   ↓
Predefined conversational response
(no database access)
```

```
Incoming Request
   ↓
Input length check
   ↓
Request frequency check
   ↓
Block if suspicious
   ↓
Allow if human-like
```

```
Streamlit UI
   ↓
Bot Detector
   ↓
LLM Router (Intent + SQL)
   ↓
Local Database (SQLite)
   ↓
Ranking Engine
   ↓
User Response
```
