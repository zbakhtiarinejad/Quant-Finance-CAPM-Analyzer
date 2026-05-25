import yfinance as yf # Importing the yfinance library to fetch financial data
import pandas as pd # Importing pandas for data manipulation and analysis
import numpy as np # Importing numpy for numerical operations
from scipy.stats import linregress # Imports linear regression function. used to caldulate: trend line, slope, correlation and R-squared value
import matplotlib.pyplot as plt # Importing matplotlib for data visualization

# REPORTLAB IMPORTS(PDF CREATION)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# imports date/time tools. used to get today's date automatically.
from datetime import datetime


# CONFIGURATION

STOCKS = ["AAPL", "MSFT", "GOOGL", "TSLA"] # list of stocks to analyze. you can change this list to include any stocks you want.
MARKET_INDEX = "^GSPC"

START_DATE = "2021-01-01" # start date for historical data. you can change this to any date you want.

# end date for historical data. set to today's date automatically.
END_DATE = datetime.today().strftime('%Y-%m-%d')

RISK_FREE_RATE = 0.04 # Assumes a 4% risk-free interest rate. Used in CAPM calculations.

PDF_REPORT_NAME = "Financial_CAPM_Report.pdf" # name of the generated PDF report. you can change this to any name you want.


# DOWNLOAD MARKET DATA

# display a message in the terminal.
print("Downloading stock data...")

all_tickers = STOCKS + [MARKET_INDEX]

# download historical stock data.
data = yf.download(
    all_tickers,
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True,
    progress=False
)

adj_close = data["Close"]

# prints completion message.
print("Data download complete.\n")


# CALCULATE RETURNS

# pct_change(): Calculates daily percentage return.
# dropna(): Removes the first row which will be NaN after percentage change calculation.
returns = adj_close.pct_change().dropna()

# extracts only S&P 500 returns.
market_returns = returns[MARKET_INDEX]


# ANALYTICS FUNCTION

def calculate_analytics(stock_returns, market_returns):

    covariance = np.cov(stock_returns, market_returns)[0][1]

    market_variance = np.var(market_returns)

    # Beta calculation: measures the stock's volatility relative to the market.
    beta = covariance / market_variance

    # Correlation calculation: measures the strength and direction
    # of the linear relationship between the stock and the market.
    correlation = np.corrcoef(stock_returns, market_returns)[0][1]

    annual_stock_return = stock_returns.mean() * 252

    annual_market_return = market_returns.mean() * 252

    annual_volatility = stock_returns.std() * np.sqrt(252)

    # this is a CAPM formula:
    expected_return = (
        RISK_FREE_RATE
        + beta * (annual_market_return - RISK_FREE_RATE)
    )

    alpha = annual_stock_return - expected_return

    regression = linregress(market_returns, stock_returns)

    r_squared = regression.rvalue ** 2

    return {
        "Stock Beta": round(beta, 4),
        "Alpha": round(alpha, 4),
        "Expected Return (%)": round(expected_return * 100, 2),
        "Actual Annual Return (%)": round(annual_stock_return * 100, 2),
        "Volatility (%)": round(annual_volatility * 100, 2),
        "Correlation": round(correlation, 4),
        "R-Squared": round(r_squared, 4)
    }


# PROCESS ALL STOCKS

results = []

for stock in STOCKS:

    stock_returns = returns[stock]

    metrics = calculate_analytics(stock_returns, market_returns)

    metrics["Stock"] = stock

    results.append(metrics)

# convert results into dataframe
results_df = pd.DataFrame(results)

print("\n===== ANALYTICS RESULTS =====\n")
print(results_df)


# GENERATE CHARTS

chart_files = []

for stock in STOCKS:

    plt.figure(figsize=(10, 5))

    # NORMALIZATION

    normalized = (
        adj_close[[stock, MARKET_INDEX]]
        / adj_close[[stock, MARKET_INDEX]].iloc[0]
    ) * 100

    normalized.plot(ax=plt.gca())

    plt.title(f"{stock} vs Market Performance")

    plt.xlabel("Date")

    plt.ylabel("Normalized Price")

    plt.grid(True)

    # creates filename dynamically:
    chart_name = f"{stock}_chart.png"

    # save chart as image
    plt.savefig(chart_name, bbox_inches="tight")

    chart_files.append(chart_name)

    # close figure to free memory
    plt.close()


# PDF REPORT CREATION

print("\nGenerating PDF report...")

doc = SimpleDocTemplate(
    PDF_REPORT_NAME,
    pagesize=letter
)

styles = getSampleStyleSheet()

elements = []


# TITLE

title = Paragraph(
    "Real-Time Financial Data Pipeline & CAPM Analysis",
    styles['Title']
)

# adds title to PDF:
elements.append(title)

elements.append(Spacer(1, 20))


# INTRODUCTION

intro_text = f"""
This report provides quantitative financial analysis
for selected equities using CAPM regression modeling,
historical return analysis, volatility analytics,
and beta risk calculations.

Market Benchmark: {MARKET_INDEX}<br/>
Analysis Period: {START_DATE} to {END_DATE}
"""

intro = Paragraph(intro_text, styles['BodyText'])

elements.append(intro)

elements.append(Spacer(1, 20))


# TABLE DATA

table_data = [list(results_df.columns)]

for row in results_df.values:
    table_data.append(list(row))

# safety check
if results_df.empty:
    print("ERROR: results dataframe is empty.")
    exit()

table = Table(table_data)

table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),

    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
]))

elements.append(table)

elements.append(Spacer(1, 30))


# ADD CHARTS

for chart in chart_files:

    elements.append(Image(chart, width=500, height=250))

    elements.append(Spacer(1, 20))


# FOOTER SUMMARY

summary = Paragraph(
    """
    Key Insights:
    <br/><br/>
    - Beta > 1 indicates higher volatility than market.
    <br/>
    - Positive alpha suggests outperformance.
    <br/>
    - Higher R-squared means stronger market relationship.
    <br/>
    - CAPM expected return estimates required return based on risk.
    """,
    styles['BodyText']
)

elements.append(summary)


# BUILD PDF

doc.build(elements)

print(f"\nPDF report generated successfully: {PDF_REPORT_NAME}")


# EXPORT CSV

results_df.to_csv("financial_metrics.csv", index=False)

print("CSV export completed.")

print("\nPROJECT FINISHED SUCCESSFULLY.")