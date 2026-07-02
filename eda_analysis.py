"""
EduPro Users - Exploratory Data Analysis (EDA)
------------------------------------------------
This script is written to be BEGINNER FRIENDLY.
It reads the users.csv file, prints some basic stats,
and saves a few simple charts into the "charts" folder.

How to run:
    python eda_analysis.py
"""

# Step 1: Import the libraries we need
import pandas as pd               # for working with tables of data
import matplotlib.pyplot as plt   # for making charts
import os                         # for creating folders

# Step 2: Make sure the "charts" folder exists (to save our images)
if not os.path.exists("charts"):
    os.makedirs("charts")

# Step 3: Load the data from the CSV file into a DataFrame (a table)
df = pd.read_csv("data/users.csv")

# Step 4: Look at the first few rows, just to check everything loaded fine
print("First 5 rows of the data:")
print(df.head())
print("\n")

# Step 5: Basic info about the dataset
print("Number of users:", len(df))
print("Columns in the dataset:", list(df.columns))
print("\n")

# Step 6: Add a new column called "EmailDomain"
# This takes the part after the "@" symbol in the email
# Example: "john@gmail.com" -> "gmail.com"
df["EmailDomain"] = df["Email"].str.split("@").str[1]

# Step 7: Add a new column called "AgeGroup"
# This groups ages into simple buckets, which is easier to understand
# than looking at every single age number.
def get_age_group(age):
    if age < 18:
        return "Under 18"
    elif age <= 24:
        return "18-24"
    elif age <= 30:
        return "25-30"
    else:
        return "31-35"

df["AgeGroup"] = df["Age"].apply(get_age_group)

# ---------------------------------------------------------
# ANALYSIS 1: Gender distribution
# ---------------------------------------------------------
print("Gender counts:")
gender_counts = df["Gender"].value_counts()
print(gender_counts)
print("\n")

# Make a pie chart for gender distribution
plt.figure(figsize=(6, 6))
plt.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
        colors=["#4C9AFF", "#FF7A9C"])
plt.title("User Gender Distribution")
plt.savefig("charts/gender_distribution.png")
plt.close()  # closes the chart so it doesn't pop up / overlap with the next one
print("Saved chart: charts/gender_distribution.png")

# ---------------------------------------------------------
# ANALYSIS 2: Age distribution
# ---------------------------------------------------------
print("\nAge statistics:")
print(df["Age"].describe())

plt.figure(figsize=(8, 5))
plt.hist(df["Age"], bins=15, color="#4C9AFF", edgecolor="white")
plt.title("User Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Users")
plt.savefig("charts/age_distribution.png")
plt.close()
print("Saved chart: charts/age_distribution.png")

# ---------------------------------------------------------
# ANALYSIS 3: Age Group distribution
# ---------------------------------------------------------
age_group_counts = df["AgeGroup"].value_counts().reindex(
    ["Under 18", "18-24", "25-30", "31-35"]
)
print("\nAge group counts:")
print(age_group_counts)

plt.figure(figsize=(8, 5))
plt.bar(age_group_counts.index, age_group_counts.values, color="#5AC8A8")
plt.title("Users by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Users")
plt.savefig("charts/age_group_distribution.png")
plt.close()
print("Saved chart: charts/age_group_distribution.png")

# ---------------------------------------------------------
# ANALYSIS 4: Email provider (domain) distribution
# ---------------------------------------------------------
domain_counts = df["EmailDomain"].value_counts()
print("\nEmail domain counts:")
print(domain_counts)

plt.figure(figsize=(8, 5))
plt.bar(domain_counts.index, domain_counts.values, color="#F4A261")
plt.title("Users by Email Provider")
plt.xlabel("Email Provider")
plt.ylabel("Number of Users")
plt.savefig("charts/email_domain_distribution.png")
plt.close()
print("Saved chart: charts/email_domain_distribution.png")

# ---------------------------------------------------------
# ANALYSIS 5: Gender split within each Age Group
# ---------------------------------------------------------
gender_by_age = df.groupby(["AgeGroup", "Gender"]).size().unstack(fill_value=0)
gender_by_age = gender_by_age.reindex(["Under 18", "18-24", "25-30", "31-35"])
print("\nGender split by age group:")
print(gender_by_age)

gender_by_age.plot(kind="bar", stacked=True, color=["#4C9AFF", "#FF7A9C"], figsize=(8, 5))
plt.title("Gender Split by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Users")
plt.xticks(rotation=0)
plt.savefig("charts/gender_by_age_group.png")
plt.close()
print("Saved chart: charts/gender_by_age_group.png")

print("\nAll done! Check the 'charts' folder for the saved images.")
