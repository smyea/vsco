# **Reddit Community Engagement & Stock Price Analysis: r/VictoriasSecret**

Analyzing the relationship between r/VictoriasSecret subreddit activity and VSCO stock price movements

### **Author:** Smyan Kapoor  
### **Date:** February 2, 2026

## Overview

This project investigates whether **community engagement on Reddit predicts stock price movements**. We analyze the r/VictoriasSecret subreddit (25.6k members) and test for correlations with **VSCO (Victoria's Secret & Co.)** stock price data.

**Key Question:** Does Reddit activity correlate with stock performance?

**Answer:** No—Reddit activity is largely independent of stock price, driven instead by product discussions and community engagement patterns.

## Table of Contents
- [Overview](#overview)
- [Key Findings](#key-findings)
- [Data](#data)
- [Methodology](#methodology)
- [Installation](#installation)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [References](#references)

## Key Findings

| Metric | Correlation | Interpretation |
|--------|-------------|-----------------|
| Posts per day ↔ Stock price | +0.1358 | Weak/negligible |
| Comments per day ↔ Stock price | +0.0735 | Weak/negligible |
| Posts per day ↔ Comments per day | +0.7999 | **Strong positive** |
| Best predictive model (R²) | 0.0734 | Only explains 7.3% of variance |

**Conclusion:** Reddit posting activity moves independently of stock price. Community engagement is driven by product interest, not market conditions. Posts and comments show strong internal correlation—when one metric rises, so does the other.

## Data

- **Source:** r/VictoriasSecret subreddit via Reddit API
- **Collection Period:** November 26, 2025 - February 1, 2026 (68 days)
- **Posts:** 881 total
- **Comments:** 8,920 total
- **Subscribers:** 25,600
- **Stock Data:** VSCO daily prices (synthetic data for 2026 projections)

## Methodology

### Data Collection
- Used PRAW (Python Reddit API Wrapper) for authentication and data extraction
- Pulled posts and comments in JSON format
- Normalized and stored in SQLite database (3 tables: subreddits, posts, comments)
- Ensured data integrity with relational constraints

### Analysis Techniques
- **Correlation Analysis:** Pearson correlation coefficients between metrics
- **Regression Modeling:** Multi-variable linear regression with standardized features
- **Time Series Analysis:** Lagged regression to test predictive power at 1-3 day intervals
- **Sentiment Analysis:** TextBlob polarity scoring for all posts and comments
- **Statistical Testing:** Scipy linregress for R² values and p-values
- **Visualization:** lets-plot for interactive charts and plots

### Key Metrics Computed
- **Activity Metrics:** Posts/day, comments/day, upvotes (normalized per 100k subscribers)
- **Engagement Ratios:** Average upvotes per post, average upvotes per comment
- **Momentum Indicators:** Daily activity changes, price volatility (rolling 3-day std dev)
- **Sentiment Scores:** Polarity from -1 (negative) to +1 (positive)

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/smyea/vsco.git
   cd vsco
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Reddit API credentials:**
   - Create `.env` file in project root
   - Add your Reddit API credentials (see NB01 for details)
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   ```

## Usage

### Quick Start
1. **Data Collection:** Run `NB01 - Data Gathering.ipynb`
   - Connects to Reddit API
   - Collects posts and comments
   - Stores in SQLite database

2. **Analysis & Visualization:** Run `NB02 - Exploratory Data Analysis.ipynb`
   - Queries the database
   - Computes daily/hourly metrics
   - Generates correlation and regression analyses
   - Creates interactive visualizations

3. **Review Results:** Check `REPORT.md` for key visualizations and findings

### Notebooks

| Notebook | Purpose |
|----------|---------|
| NB01 - Data Gathering | Data collection, cleaning, storage |
| NB02 - Exploratory Data Analysis | Analysis, correlations, visualizations |

## Repository Structure

```
vsco/
├── README.md                    # This file
├── REPORT.md                    # Detailed findings and visualizations
├── requirements.txt             # Python dependencies
├── .env                         # Reddit API credentials (not in repo)
├── notebooks/
│   ├── NB01 - Data Gathering.ipynb
│   ├── NB02 - Exploratory Data Analysis.ipynb
│   └── utils.py                # Helper functions
├── data/
│   └── database.db             # SQLite database (posts, comments, subreddits)
└── figures/
    └── [Generated visualizations]
```

## References

**Reddit API & Data Collection:**
- Baumgartner, J. (2023). PRAW: The Python Reddit API Wrapper. https://praw.readthedocs.io/

**Stock Price Data:**
- Yahoo Finance. (2026). VSCO - Victoria's Secret & Co. Available at: https://finance.yahoo.com/quote/VSCO/

**Statistical Analysis:**
- SciPy Community. (2025). scipy.stats. Available at: https://docs.scipy.org/doc/scipy/reference/stats.html
- scikit-learn Developers. (2025). Preprocessing and Model Selection. https://scikit-learn.org/

**Natural Language Processing:**
- Loria, S. (2024). TextBlob: Simplified Text Processing. https://textblob.readthedocs.io/

**Data Processing:**
- pandas Development Team. (2025). pandas documentation. https://pandas.pydata.org/
- SQLAlchemy Contributors. (2025). SQLAlchemy - The Database Toolkit for Python. https://www.sqlalchemy.org/

**Visualization:**
- JetBrains. (2025). lets-plot: Grammar of Graphics for Python. https://lets-plot.org/

**Python Environment:**
- Python Software Foundation. (2025). Python 3.9+. https://www.python.org/