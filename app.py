"""
EduPro Instructor Performance & Course Quality - Streamlit Dashboard
------------------------------------------------------------------------
Beginner-friendly interactive dashboard covering:
  - Instructor performance leaderboard
  - Experience vs rating scatter plot
  - Course quality heatmap (Category x Level)
  - Expertise-wise performance comparison
Filters: instructor expertise, course category & level, rating range slider

How to run:
    streamlit run app.py
"""

# Step 1: Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Step 2: Page setup
st.set_page_config(page_title="EduPro Instructor & Course Dashboard", layout="wide")
st.title("EduPro - Instructor Performance & Course Quality Dashboard")

# Step 3: Load and merge the data (cached so it only runs once)
@st.cache_data
def load_data():
    teachers = pd.read_csv("EduPro Online Platform.xlsx - Teachers.csv")
    courses = pd.read_csv("EduPro Online Platform.xlsx - Courses.csv")
    transactions = pd.read_csv("EduPro Online Platform.xlsx - Transactions.csv")


  
    # Join everything together, one row per enrollment
    merged = transactions.merge(courses, on="CourseID", how="left")
    merged = merged.merge(teachers, on="TeacherID", how="left")

    # Add a rating tier for teachers (High / Mid / Low)
    def rating_tier(rating):
        if rating >= 4.3:
            return "High"
        elif rating >= 3.5:
            return "Mid"
        else:
            return "Low"

    teachers["RatingTier"] = teachers["TeacherRating"].apply(rating_tier)
    merged = merged.merge(teachers[["TeacherID", "RatingTier"]], on="TeacherID", how="left")

    return teachers, courses, transactions, merged

teachers, courses, transactions, merged = load_data()

# ---------------------------------------------------------
# SIDEBAR: Filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

expertise_options = sorted(teachers["Expertise"].unique().tolist())
selected_expertise = st.sidebar.multiselect(
    "Instructor Expertise", options=expertise_options, default=expertise_options
)

category_options = sorted(courses["CourseCategory"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Course Category", options=category_options, default=category_options
)

level_options = ["Beginner", "Intermediate", "Advanced"]
selected_levels = st.sidebar.multiselect(
    "Course Level", options=level_options, default=level_options
)

rating_range = st.sidebar.slider(
    "Teacher Rating Range", min_value=1.0, max_value=5.0,
    value=(1.0, 5.0), step=0.1
)

# Step 4: Apply filters to the teachers table
filtered_teachers = teachers[
    (teachers["Expertise"].isin(selected_expertise)) &
    (teachers["TeacherRating"] >= rating_range[0]) &
    (teachers["TeacherRating"] <= rating_range[1])
]

# Apply filters to the merged (enrollment-level) table
filtered_merged = merged[
    (merged["Expertise"].isin(selected_expertise)) &
    (merged["CourseCategory"].isin(selected_categories)) &
    (merged["CourseLevel"].isin(selected_levels)) &
    (merged["TeacherRating"] >= rating_range[0]) &
    (merged["TeacherRating"] <= rating_range[1])
]

# ---------------------------------------------------------
# TOP ROW: KPIs
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

avg_teacher_rating = filtered_teachers["TeacherRating"].mean() if len(filtered_teachers) > 0 else 0
avg_course_rating = filtered_merged["CourseRating"].mean() if len(filtered_merged) > 0 else 0

rating_std = filtered_teachers["TeacherRating"].std() if len(filtered_teachers) > 1 else 0
consistency_index = round(1 - (rating_std / avg_teacher_rating), 2) if avg_teacher_rating > 0 else 0

exp_rating_corr = filtered_teachers["YearsOfExperience"].corr(filtered_teachers["TeacherRating"]) \
    if len(filtered_teachers) > 1 else 0

enrollment_counts = filtered_merged.groupby("RatingTier").size()
high_e = enrollment_counts.get("High", 0)
low_e = enrollment_counts.get("Low", 1) or 1
enrollment_ratio = round(high_e / low_e, 2)

col1.metric("Avg Teacher Rating", f"{avg_teacher_rating:.2f}")
col2.metric("Avg Course Rating", f"{avg_course_rating:.2f}")
col3.metric("Rating Consistency Index", f"{consistency_index:.2f}")
col4.metric("Experience Impact Score", f"{exp_rating_corr:.2f}" if pd.notnull(exp_rating_corr) else "N/A")
col5.metric("Enrollment Influence Ratio", f"{enrollment_ratio}")

st.divider()

# ---------------------------------------------------------
# MODULE 1: Instructor Performance Leaderboard
# ---------------------------------------------------------
st.subheader("Instructor Performance Leaderboard")
leaderboard = filtered_teachers.sort_values("TeacherRating", ascending=False)[
    ["TeacherName", "Expertise", "YearsOfExperience", "TeacherRating"]
].reset_index(drop=True)
leaderboard.index += 1  # start ranking at 1
st.dataframe(leaderboard, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# MODULE 2 & 3: Scatter plot + Heatmap side by side
# ---------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Experience vs Rating")
    if len(filtered_teachers) > 0:
        fig1, ax1 = plt.subplots()
        ax1.scatter(filtered_teachers["YearsOfExperience"], filtered_teachers["TeacherRating"],
                    color="#4C9AFF", alpha=0.6)
        ax1.set_xlabel("Years of Experience")
        ax1.set_ylabel("Teacher Rating")
        st.pyplot(fig1)
    else:
        st.write("No data for the selected filters.")

with chart_col2:
    st.subheader("Course Quality Heatmap (Category x Level)")
    if len(filtered_merged) > 0:
        pivot = filtered_merged.pivot_table(
            index="CourseCategory", columns="CourseLevel", values="CourseRating", aggfunc="mean"
        ).reindex(columns=["Beginner", "Intermediate", "Advanced"])

        fig2, ax2 = plt.subplots(figsize=(6, 5))
        im = ax2.imshow(pivot.values, cmap="YlGnBu", aspect="auto", vmin=1, vmax=5)
        ax2.set_xticks(range(len(pivot.columns)))
        ax2.set_xticklabels(pivot.columns)
        ax2.set_yticks(range(len(pivot.index)))
        ax2.set_yticklabels(pivot.index)
        # Write the actual rating number inside each heatmap cell
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                value = pivot.values[i, j]
                if not np.isnan(value):
                    ax2.text(j, i, f"{value:.2f}", ha="center", va="center", color="black")
        fig2.colorbar(im, ax=ax2, label="Average Course Rating")
        st.pyplot(fig2)
    else:
        st.write("No data for the selected filters.")

st.divider()

# ---------------------------------------------------------
# MODULE 4: Expertise-wise Performance Comparison
# ---------------------------------------------------------
st.subheader("Expertise-wise Performance Comparison")
if len(filtered_teachers) > 0:
    expertise_perf = filtered_teachers.groupby("Expertise")["TeacherRating"].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(9, 4))
    ax3.bar(expertise_perf.index, expertise_perf.values, color="#5AC8A8")
    ax3.set_xlabel("Expertise")
    ax3.set_ylabel("Average Teacher Rating")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig3)
else:
    st.write("No data for the selected filters.")

st.divider()

# ---------------------------------------------------------
# Enrollment volume by rating tier
# ---------------------------------------------------------
st.subheader("Enrollment Volume by Instructor Rating Tier")
if len(filtered_merged) > 0:
    tier_counts = filtered_merged.groupby("RatingTier").size().reindex(["High", "Mid", "Low"]).fillna(0)
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ax4.bar(tier_counts.index, tier_counts.values, color="#8E7CC3")
    ax4.set_xlabel("Instructor Rating Tier")
    ax4.set_ylabel("Number of Enrollments")
    st.pyplot(fig4)
else:
    st.write("No data for the selected filters.")

st.divider()

# ---------------------------------------------------------
# Data download
# ---------------------------------------------------------
st.subheader("Download Filtered Data")
csv_data = filtered_merged.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Enrollment Data as CSV",
    data=csv_data,
    file_name="filtered_instructor_course_data.csv",
    mime="text/csv",
)
