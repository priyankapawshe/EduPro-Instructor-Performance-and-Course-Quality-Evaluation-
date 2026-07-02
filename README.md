# EduPro User Demographics & Engagement Analysis

## About this project

This project analyzes the **EduPro Users dataset** (3,000 users) to understand
who is using the platform — their age, gender, and email provider — using
simple, beginner-friendly Python code.

> **Note on scope:** The original brief ("Instructor Performance and Course
> Quality Evaluation on EduPro") asked for Teachers, Courses, and Transactions
> data. Only the **Users** sheet (UserID, UserName, Age, Gender, Email) was
> available, so this project was adapted to a **User Demographics &
> Engagement Analysis** instead, using the same structure: EDA script +
> Streamlit dashboard + summary of insights. If you later get the
> Teachers/Courses/Transactions sheets, the original instructor-evaluation
> project can be built the same way.

## Project structure

```
EduPro_User_Analysis/
├── data/
│   └── users.csv              # the raw dataset
├── charts/                    # charts saved by eda_analysis.py
├── eda_analysis.py            # step-by-step EDA script (run first)
├── app.py                     # Streamlit interactive dashboard
├── requirements.txt           # Python packages needed
├── research_summary.md        # written insights & recommendations
└── README.md                  # this file
```

## How to run it

### 1. Install the requirements
```bash
pip install -r requirements.txt
```

### 2. Run the EDA script (generates charts + prints stats)
```bash
python eda_analysis.py
```
This creates PNG chart images inside the `charts/` folder and prints
summary statistics to the terminal.

### 3. Launch the interactive dashboard
```bash
streamlit run app.py
```
This opens a browser window where you can:
- Filter by **Gender**
- Filter by **Age range** (slider)
- Filter by **Email provider**
- See live-updating charts and key numbers (KPIs)
- Download the filtered data as a CSV

## Key Performance Indicators (KPIs) tracked

| KPI | Description |
|---|---|
| Total Users | Overall platform user base size |
| Average Age | Central tendency of the user base |
| Gender Split | Male vs Female proportion |
| Age Group Distribution | Under 18 / 18-24 / 25-30 / 31-35 |
| Email Provider Split | Gmail / Yahoo / Hotmail / Outlook share |

## Key questions this project answers

- What does the age distribution of EduPro's user base look like?
- Is the platform gender-balanced overall and within each age group?
- Which email providers are most common among users (useful for
  email-deliverability and marketing decisions)?
- Are certain age groups over- or under-represented?

See `research_summary.md` for the written findings and recommendations.
