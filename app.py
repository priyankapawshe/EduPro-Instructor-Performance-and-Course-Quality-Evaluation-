"""
EduPro Users - Streamlit Dashboard
------------------------------------
This is a simple, beginner-friendly dashboard.
It lets you filter the users data and see live charts update.

How to run:
    streamlit run app.py
"""

# Step 1: Import the libraries we need
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Step 2: Basic page setup (title, layout)
st.set_page_config(page_title="EduPro User Dashboard", layout="wide")
st.title("EduPro Platform - User Demographics Dashboard")
st.write(
    "This dashboard explores the EduPro Users dataset "
    "(3,000 users) — age, gender, and email provider."
)


# Step 3: Load the data
# @st.cache_data means Streamlit will remember the data
# instead of reloading the file every time you move a slider.
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\SANDEEP\OneDrive\Desktop\Unified_Mentor_projects\project5\EduPro Online Platform.xlsx - Users.csv")
    df["EmailDomain"] = df["Email"].str.split("@").str[1]

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
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR: Filters the user can control
# ---------------------------------------------------------
st.sidebar.header("Filters")

# Gender filter (checkboxes / multiselect)
gender_options = df["Gender"].unique().tolist()
selected_genders = st.sidebar.multiselect(
    "Select Gender", options=gender_options, default=gender_options
)

# Age range filter (slider)
min_age = int(df["Age"].min())
max_age = int(df["Age"].max())
age_range = st.sidebar.slider(
    "Select Age Range", min_value=min_age, max_value=max_age,
    value=(min_age, max_age)
)

# Email provider filter
domain_options = df["EmailDomain"].unique().tolist()
selected_domains = st.sidebar.multiselect(
    "Select Email Provider", options=domain_options, default=domain_options
)

# Step 4: Apply the filters to the data
filtered_df = df[
    (df["Gender"].isin(selected_genders)) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1]) &
    (df["EmailDomain"].isin(selected_domains))
]

# ---------------------------------------------------------
# TOP ROW: Key numbers (KPIs)
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Users (filtered)", len(filtered_df))
col2.metric("Average Age", round(filtered_df["Age"].mean(), 1) if len(filtered_df) > 0 else 0)
col3.metric("Unique Email Providers", filtered_df["EmailDomain"].nunique())

st.divider()

# ---------------------------------------------------------
# CHART ROW 1: Gender pie chart + Age histogram
# ---------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Gender Distribution")
    if len(filtered_df) > 0:
        gender_counts = filtered_df["Gender"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
                colors=["#4C9AFF", "#FF7A9C"])
        ax1.set_title("Gender Split")
        st.pyplot(fig1)
    else:
        st.write("No data for the selected filters.")

with chart_col2:
    st.subheader("Age Distribution")
    if len(filtered_df) > 0:
        fig2, ax2 = plt.subplots()
        ax2.hist(filtered_df["Age"], bins=15, color="#4C9AFF", edgecolor="white")
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Number of Users")
        st.pyplot(fig2)
    else:
        st.write("No data for the selected filters.")

# ---------------------------------------------------------
# CHART ROW 2: Age group bar chart + Email domain bar chart
# ---------------------------------------------------------
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Users by Age Group")
    if len(filtered_df) > 0:
        age_group_counts = filtered_df["AgeGroup"].value_counts().reindex(
            ["Under 18", "18-24", "25-30", "31-35"]
        ).fillna(0)
        fig3, ax3 = plt.subplots()
        ax3.bar(age_group_counts.index, age_group_counts.values, color="#5AC8A8")
        ax3.set_xlabel("Age Group")
        ax3.set_ylabel("Number of Users")
        st.pyplot(fig3)
    else:
        st.write("No data for the selected filters.")

with chart_col4:
    st.subheader("Users by Email Provider")
    if len(filtered_df) > 0:
        domain_counts = filtered_df["EmailDomain"].value_counts()
        fig4, ax4 = plt.subplots()
        ax4.bar(domain_counts.index, domain_counts.values, color="#F4A261")
        ax4.set_xlabel("Email Provider")
        ax4.set_ylabel("Number of Users")
        st.pyplot(fig4)
    else:
        st.write("No data for the selected filters.")

st.divider()

# ---------------------------------------------------------
# DATA TABLE: Let the user see (and download) the raw filtered rows
# ---------------------------------------------------------
st.subheader("Filtered Data Table")
st.dataframe(filtered_df[["UserID", "UserName", "Age", "Gender", "Email"]])

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_users.csv",
    mime="text/csv",
)
