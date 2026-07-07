# Online Retail Transaction — Exploratory Data Analysis

<p align="center">
  <img src="src/Cover.png" width="100%">
</p>


## Project Context

Online retail transaction data provides valuable information about purchasing activity, product performance, and revenue contribution. This project explores e-commerce transaction data to understand the patterns behind revenue performance and identify key factors that contribute to higher transaction value.

## Problem

A high number of transactions does not necessarily generate the highest revenue. This analysis examines which transaction segments contribute the most revenue and explores the products, transaction values, geographic markets, and monthly trends behind their performance.

## Project Resources

- **Dataset:** [View Dataset]([LINK_SPREADSHEET](https://docs.google.com/spreadsheets/d/1wkqIxc3xv4Rb7xQdmwAtKumzo6iLyIn15zIbfLA46zk/edit?usp=sharing))
- **Analysis Notebook:** [View Analysis in Google Colab]([LINK_COLAB](https://colab.research.google.com/gist/gmustika1312-svg/5192aff4fc9d6d66b04577ae76d1f043/assignment_day_20_advanced_exploratory_data_analysis_ggmu.ipynb))
- **Python Source Code:** [`online_retail_eda.py`](src/online_retail_eda.py)

## Analysis Workflow

The analysis was conducted through six stages:

**01 — Data Understanding**  
Review the dataset structure, data types, and summary statistics.

**02 — Data Quality Check**  
Check missing values and duplicate records.

**03 — Feature Engineering**  
Create time and revenue features to support further analysis.

**04 — Outlier Analysis**  
Identify unusual values using the IQR method.

**05 — Transaction Segmentation**  
Group transactions based on transaction value.

**06 — Business Questions**  
Answer five analytical questions through data manipulation and visualization.

## Key Findings

- The **Premium segment contributes 52.79% of total revenue**, making it the largest revenue contributor.
- Premium revenue is driven by **higher transaction value rather than transaction frequency**.
- **WHITE HANGING HEART T-LIGHT HOLDER** contributes the highest revenue within the Premium segment at **6.42%**.
- The **United Kingdom contributes 81.15% of Premium revenue**, indicating a high geographic concentration.
- Premium revenue shows stronger performance from **August to November**, reaching its highest level in November.

## Recommendations

The analysis indicates that Premium customers should be prioritized through targeted retention and personalized offers. Product availability should be maintained for high-revenue products, while High-segment customers can be encouraged to increase transaction value through bundling and targeted promotions.

The concentration of Premium revenue in the United Kingdom also highlights an opportunity to expand customer engagement in other markets. Inventory and promotional planning should be strengthened before the August–November period.

## Tools

Python · Pandas · NumPy · Matplotlib · Seaborn · Google Colab
