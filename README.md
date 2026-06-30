# SearchX — Simple Search Engine (Flask)

A lightweight Flask web app that performs a DuckDuckGo web search and also supports **smart math**, **unit conversion**, and **basic currency parsing**.

---

## Features

- 🌐 **Web Search**: Uses Selenium + DuckDuckGo and shows the top results.
- 🧮 **Smart Math** (via SymPy):
  - Percent queries (e.g., `20% of 150`)
  - Square root / cube root
  - Simple algebra equations (one variable) (e.g., `2x + 3 = 7`)
  - Expression factorization for identities involving `x` or `y`
  - Basic arithmetic expressions (e.g., `10*(2+3)`)
- 📏 **Unit Conversion**: Supports `km`, `m`, `cm`, `mm` conversion phrasing like `5 km to m`.
- 💱 **Currency Parsing**: Parses inputs like `100 usd to inr` (UI note: conversion message says live conversion is coming soon).
- 🎨 Responsive UI with a polished loader animation.

---

## Tech Stack

- **Backend**: Flask
- **Math/Algebra**: SymPy
- **Web Scraping/Search**: Selenium (headless Chrome)
- **Frontend**: HTML templates (Jinja2) + CSS

---

## Project Structure

- `app.py` — Flask app, routing, and the query logic
- `templates/`
  - `index.html` — search landing page
  - `result.html` — renders search results or computed outputs
- `static/`
  - `style.css` — styling
- `test.py` — small Playwright sanity check (not required for the app)
- `requirements.txt` — Python dependencies

---

## Setup & Run

### 1) Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- Windows (cmd):

```bash
venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the server

```bash
python app.py
```

Open your browser:

- http://localhost:5000

---

## How It Works

1. User submits a query from the home page.
2. Server processes the query in this order:
   1. **Smart math** (`smart_math`) — if detected, renders the calculation result.
   2. **Unit conversion** (`detect_unit`) — if detected, renders converted value.
   3. **Currency parsing** (`detect_currency`) — if detected, renders a UI message.
   4. Otherwise performs a **DuckDuckGo search** (`search_duckduckgo`).

---

## Examples

### Smart math

- `20% of 150`
- `sqrt 25`
- `cube root of 27`
- `2x + 3 = 7`
- `10*(2+3)`

### Unit conversion

- `5 km to m`
- `20 cm to mm`

### Currency parsing (UI)

- `100 usd to inr`

---

## Notes / Limitations

- DuckDuckGo scraping uses **Selenium** and may be slower than API-based search.
- Smart math parsing supports a limited set of patterns; more complex natural-language math may not be recognized.
- Currency conversion currently only parses and displays a placeholder message.

---

## License

MIT (or replace with your preferred license). 

