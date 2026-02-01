# **“How has retail investor activity changed in the recent days of market uncertainty under the Trump Administration?”**
### **Author:** Smyan Kapoor  
### **Project:** Mini-Project II  
### **Submission Date:** April 2, 2025  

## Table of Contents
- [Structure](#structure)
- [Scope](#scope)
- [Methodology](#methodology)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [References](#references)

## Structure

This repository is organized into the following sections:

- The `README.md` file (this document) provides background information and guidance for navigating the project.

- The `notebooks/` directory contains:
  - `NB01 - Data Gathering.ipynb`: for data collection, cleaning, and storage.
  - `NB02 - Exploratory Data Analysis.ipynb`: for querying and analyzing the data to answer the central research 
  question.
  - The `utils.py` file which contains functions used in the project, particularly for data gathering in NBO1
- The `figures/` directory includes two figures generated during analysis.
- The `data/` folder holds three tables for the comments, posts and subreddits in `database.db`, the SQLite database.
- The `REPORT.md` contains a report that analyses and evaluates our data including two graphs and comes to conclusions about the research question
- The `requirements.txt` lists all the dependencies the project needs to run

## Scope

 Using Reddit data from several finance-focused subreddits, we analyze post and comment activity, normalized by subscriber counts, to track shifts in participation and engagement over time.

The focus is on **quantifiable metrics** like upvotes, comments, and posting frequency, aggregated both daily and hourly.

## Methodology

### **Data Gathering**
- **Subreddit Selection:** We chose r/wallstreetbets (18M), r/investing (3M), r/stocks (8.5M) and r/stockmarket(3.5M)
- **API Access:** Used the `requests` library with proper OAuth2 authentication. Credentials are kept secret using a `.env` file and excluded via `.gitignore`.

- **Data Extraction & Transformation:**
  - Pulled posts and comments in JSON format.
  - Normalized into flat tables using and stored data in 3 tables: `subreddits`, `posts`, `comments`.
  - Ensured relational consistency and integrity in an SQLite database.

### **Exploratory Analysis**

- Queried the database using `pandas.read_sql()`.
- Applied aggregation and reshaping to compute dataframes segmented by daily and hourly groupings
- Visualised using `lets-plot`

## Installation

1. **Clone this repository** to your local machine:
   ```bash
   git clone "https://github.com/lse-ds105/mini-project-2-ds105w-2025-smyea.git"
2. **Install** the required packages from [`requirements.txt`](./requirements.txt):
    ```bash
    pip install -r requirements.txt
    
## Usage

1. Begin with the [Data Gathering notebook](./notebooks/NB01%20-%20Data%20Gathering.ipynb), where you'll extract, clean, and store Reddit data in an SQLite database.

2. Then proceed to the [Exploratory Data Analysis notebook](./notebooks/NB02%20-%20Exploratory%20Data%20Analysis.ipynb), which queries the database, reshapes the data, and generates visualisations to explore the research question.

3. Finally, review the findings and insights in [`REPORT.md`](./REPORT.md), which includes key visualisations and interpretations.

## Results

The study suggests that retail investor activity on finance-focused subreddits correlates with significant market events and periods of uncertainty, particularly during the Trump Administration. Spikes in activity were observed during events such as tariff announcements and market downturns, indicating a potential link between political and economic news and retail investor engagement. Hourly analysis further reveals that retail investor activity peaks during market hours, particularly between 9 AM and 5 PM New York time, highlighting connections between market operations and subreddit activity.

## References

Reddit. Best of Reddit. Reddit. Available at: https://www.reddit.com/best/communities/1/#t5_2qjuv (Accessed: 2 April 2025).

CNBC, 2025a. *Stock Market Today: Live Updates – February 2, 2025*. [online] CNBC. Available at: <https://www.cnbc.com/2025/02/02/stock-market-today-live-updates.html> [Accessed 1 Apr. 2025].

The Guardian, 2025. *US stocks dip amid concerns over tariffs and consumer belt-tightening*. [online] The Guardian. Available at: <https://www.theguardian.com/us-news/2025/feb/21/stocks-tariffs-prices> [Accessed 1 Apr. 2025].

CNBC, 2025b. *Stock Market Today: Live Updates – February 28, 2025*. [online] CNBC. Available at: <https://www.cnbc.com/2025/02/26/stock-market-today-live-updates.html> [Accessed 1 Apr. 2025].

MarketWatch, 2025. *Dow, S&P, and Nasdaq to Hold Latest Rally After Bitcoin Surge*. [online] MarketWatch. Available at: <https://www.marketwatch.com/livecoverage/stock-market-today-dow-s-p-and-nasdaq-to-hold-latest-rally-after-bitcoin-surge> [Accessed 1 Apr. 2025].

Yahoo Finance, 2025. *Nasdaq Enters Correction, S&P 500 Sinks on Trump Tariff Whiplash*. [online] Yahoo! Finance. Available at: <https://finance.yahoo.com/news/live/stock-market-today-nasdaq-enters-correction-sp-500-sinks-to-lowest-since-november-as-stocks-get-clobbered-on-trump-tariff-whiplash-210544344.html> [Accessed 1 Apr. 2025].

Reuters, 2025a. *Investors Flee Equities as Trump-Driven Uncertainty Sparks Economic Worry*. [online] Reuters. Available at: <https://www.reuters.com/markets/us/investors-flee-equities-trump-driven-uncertainty-sparks-economic-worry-2025-03-10/> [Accessed 1 Apr. 2025].

Wall Street Journal, 2025. *Stock Market Today – March 21, 2025*. [online] WSJ. Available at: <https://www.wsj.com/livecoverage/stock-market-today-dow-nasdaq-sp500-03-21-2025> [Accessed 1 Apr. 2025].

Reuters, 2025b. *Wall Street Futures Slip As Trump-Led Rally Loses Steam*. [online] Reuters. Available at: <https://www.reuters.com/markets/us/wall-st-futures-slip-trump-led-rally-loses-steam-2025-03-25/> [Accessed 1 Apr. 2025].

Investopedia, 2025a. *Dow Jones Today – March 28, 2025*. [online] Investopedia. Available at: <https://www.investopedia.com/dow-jones-today-03282025-11704900> [Accessed 1 Apr. 2025].

Investopedia, 2025b. *Dow Jones Today – March 31, 2025*. [online] Investopedia. Available at: <https://www.investopedia.com/dow-jones-today-03312025-11705913> [Accessed 1 Apr. 2025].