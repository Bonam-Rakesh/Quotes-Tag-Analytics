# 📊 Quotes Tag Analytics

It is a data analytics project based on Python which involves collecting, cleaning, analysing and visualising quote data by means of web scraping and by using publicly available quote data.

The project is about identifying patterns in **quotes, authors, tags, quote length, word count, and the relationships between tags**.

---

## 📌 Project Overview

There are interesting patterns in quotes concerning authors, topics, and writing style.

**Quotes Tag Analytics** demonstrates an end-to-end data analysis workflow using Python:

**Data Collection → Data Cleaning → Feature Engineering → Exploratory Data Analysis → Visualization → Insights**

The end result includes **250 distinct quotes** together with details regarding their authors and their tags.

---

## 🎯 Objectives

The main objectives of this project are to:

- Gather quote data with code.
- Create an organized quote dataset.
- Eliminate the duplicate and invalid records.
- Normalize tag information.
- Make helpful analytical features.
- Examine the authorship and tag patterns.
- Look at the distribution of quotes and the distribution of word lengths.
- Find out which combinations of tags occur most often.
- Use visualizations to present the findings.

---

## ✨ Features

- 🌐 Web scraping using BeautifulSoup
- 📦 Public quote dataset integration
- 🧹 Data cleaning and normalization
- 🔎 Exploratory data analysis
- 👤 Author frequency analysis
- 🏷️ Tag frequency analysis
- 🔗 Tag combination analysis
- 📏 Quote length analysis
- 📝 Word count analysis
- 📊 Data visualization
- 📓 Interactive Jupyter Notebook
- 📁 Organized project structure

---

## 📊 Dataset

The final cleaned dataset contains:

| Metric | Value |
|---|---:|
| Total Quotes | 250 |
| Unique Authors | 156 |
| Unique Tags | 146 |
| The average number of words per quote is 18.85. |
The average quote length is 99.98 characters.
| Average Tags per Quote | 1.71 |

### Dataset Columns

| Column | Description |
|---|---|
| `quote` | Text of the quote |
| `author` | Author of the quote |
| `tags` | Associated tags |
| `tag_count` | Number of tags assigned to the quote |
| `quote_length` | Number of characters in the quote |
| `word_count` | Number of words in the quote |

---

## 🔄 Project Pipeline

```text
                 ┌─────────────────────┐
                 │   Data Collection   │
                 │ Web Scraping + Data  │
                 │      Sources        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Data Cleaning     │
                 │ Remove Duplicates   │
                 │ Normalize Tags      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Feature Engineering │
                 │ Tag Count           │
                 │ Quote Length        │
                 │ Word Count          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Exploratory         │
                 │ Data Analysis       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Visualization       │
                 │ Charts & Distributions│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Insights & Findings │
                 └─────────────────────┘