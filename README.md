# Quant-Finance-CAPM-Analyzer
# Real-Time Financial Data Pipeline & CAPM Analyzer

A quantitative finance project that automates stock market analysis using live financial data, CAPM modeling, statistical risk analytics, and PDF report generation.

This project was built to demonstrate practical skills in:
- Financial data engineering
- API integration
- Quantitative finance
- Statistical modeling
- Data visualization
- Python automation

---

# Features

- Live stock market data download using Yahoo Finance API
- Historical price analysis
- CAPM (Capital Asset Pricing Model) calculations
- Beta and Alpha risk analysis
- Volatility and correlation metrics
- Regression-based financial analytics
- Automated PDF report generation
- Interactive Streamlit dashboard
- Multi-stock portfolio support
- Data visualization with charts

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| yfinance | Financial market API |
| Pandas | Data manipulation |
| NumPy | Numerical calculations |
| SciPy | Statistical regression |
| Matplotlib | Data visualization |
| ReportLab | PDF report generation |
| Streamlit | Interactive dashboard |

---

# Project Structure

```text
quant-finance-project/
│
├── data/
│   └── downloaded_data.csv
│
├── reports/
│   ├── Financial_Report.pdf
│   └── charts/
│
├── src/
│   ├── data_loader.py
│   ├── analytics.py
│   ├── report_generator.py
│   ├── dashboard.py
│   └── utils.py
│
├── images/
│   └── dashboard_preview.png
│
├── requirements.txt
├── README.md
└── main.py
