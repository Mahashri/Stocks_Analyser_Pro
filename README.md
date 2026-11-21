# Stock Analyser Pro

A Flask-based stock-market visualization project that groups equities into market and sector categories and compares their current prices with 52-week trading ranges.

## Features visible in the source
- Broad Indian stock universe.
- Sector-oriented groups, including banking, railways, defence, gold/finance, power/cement and FMCG/AMC.
- US stock watchlist.
- Retrieval of company names, current prices and 52-week high/low values through yfinance.
- Matplotlib range visualizations rendered as embedded images.

## Technology stack
- Python and Flask
- yfinance
- NumPy
- Matplotlib
- Gunicorn (listed in requirements)

## Run locally
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask entry point:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000`.

## Engineering considerations
The current source performs many sequential yfinance requests during a page request. This can cause slow responses and provider throttling. Consider batch downloads, caching, background refresh and explicit data timestamps. Validate missing fields before plotting and ensure company-name arrays always match the valid ticker list.

## Future improvements
- Split data acquisition, sector configuration and chart generation into modules.
- Add caching and scheduled data refresh.
- Add tests for range positioning and missing/invalid quote values.
- Add responsive tabular views and accessible chart alternatives.
- Configure production WSGI deployment and CI.

## Disclaimer
Quotes may be delayed, incomplete or unavailable. This project is not investment advice.


---

## Live Demo

[Open the deployed application](https://stocks-analyser-pro.vercel.app/)
