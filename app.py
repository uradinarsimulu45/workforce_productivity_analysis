import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Workforce Productivity Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/workforce_productivity_data.csv"
    )

    df["period_date"] = pd.to_datetime(
        df["period_date"]
    )

    df["date_joined"] = pd.to_datetime(
        df["date_joined"],
        errors="coerce"
    )

    df["date_left"] = pd.to_datetime(
        df["date_left"],
        errors="coerce"
    )

    return df


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📊 Workforce Productivity Analytics")

st.write(
    "Interactive dashboard for analyzing workforce productivity, "
    "working hours, output, quality, overtime, absenteeism and attrition."
)


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{len(df):,}"
)

col2.metric(
    "Employees",
    f"{df['employee_id'].nunique():,}"
)

col3.metric(
    "Departments",
    f"{df['department'].nunique():,}"
)

col4.metric(
    "Average Quality",
    f"{df['quality_score'].mean():.2f}"
)


st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Filters")

departments = ["All"] + sorted(
    df["department"].dropna().unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)

if selected_department != "All":

    filtered_df = df[
        df["department"] == selected_department
    ]

else:

    filtered_df = df.copy()


# ============================================================
# DEPARTMENT SUMMARY
# ============================================================

st.header("🏢 Department Productivity")

dept_summary = (
    filtered_df
    .groupby("department")
    .agg(
        avg_hours_worked=("hours_worked", "mean"),
        avg_output=("output_units", "mean"),
        avg_quality=("quality_score", "mean"),
        avg_overtime=("overtime_hours", "mean")
    )
    .reset_index()
)


# ============================================================
# OUTPUT BY DEPARTMENT
# ============================================================

fig = px.bar(
    dept_summary,
    x="department",
    y="avg_output",
    color="department",
    text_auto=".2f",
    title="Average Output by Department"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# HOURS VS OUTPUT
# ============================================================

st.header("⏱️ Hours Worked vs Output")

fig = px.scatter(
    dept_summary,
    x="avg_hours_worked",
    y="avg_output",
    size="avg_quality",
    color="department",
    text="department",
    title="Average Hours Worked vs Average Output",
    labels={
        "avg_hours_worked": "Average Hours Worked",
        "avg_output": "Average Output",
        "avg_quality": "Average Quality"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# OVERTIME
# ============================================================

st.header("🕐 Overtime Analysis")

overtime = (
    filtered_df
    .groupby("department")["overtime_hours"]
    .sum()
    .reset_index()
    .sort_values(
        "overtime_hours",
        ascending=False
    )
)

fig = px.bar(
    overtime,
    x="department",
    y="overtime_hours",
    color="department",
    text_auto=".2f",
    title="Total Overtime Hours by Department"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# QUALITY
# ============================================================

st.header("⭐ Quality Analysis")

fig = px.bar(
    dept_summary,
    x="department",
    y="avg_quality",
    color="department",
    text_auto=".2f",
    title="Average Quality Score by Department"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MONTHLY PRODUCTIVITY
# ============================================================

st.header("📈 Monthly Productivity Trend")

monthly = (
    filtered_df
    .groupby(
        filtered_df["period_date"].dt.to_period("M")
    )
    .agg(
        avg_output=("output_units", "mean"),
        avg_hours=("hours_worked", "mean"),
        avg_quality=("quality_score", "mean"),
        avg_overtime=("overtime_hours", "mean")
    )
    .reset_index()
)

monthly["month"] = (
    monthly["period_date"]
    .astype(str)
)


fig = px.line(
    monthly,
    x="month",
    y="avg_output",
    markers=True,
    title="Monthly Average Output",
    labels={
        "month": "Month",
        "avg_output": "Average Output Units"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# ABSENCE VS OUTPUT
# ============================================================

st.header("🏥 Absenteeism vs Productivity")

absence = (
    filtered_df
    .groupby("department")
    .agg(
        avg_absence_days=("absence_days", "mean"),
        avg_output=("output_units", "mean"),
        avg_quality=("quality_score", "mean")
    )
    .reset_index()
)

fig = px.scatter(
    absence,
    x="avg_absence_days",
    y="avg_output",
    size="avg_quality",
    color="department",
    text="department",
    title="Absenteeism vs Average Output",
    labels={
        "avg_absence_days": "Average Absence Days",
        "avg_output": "Average Output"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# ATTRITION
# ============================================================

st.header("👥 Attrition Analysis")

attrition = (
    filtered_df
    .groupby("department")
    .agg(
        employees=("employee_id", "nunique"),
        attrition_rate=("attrition_flag", "mean")
    )
    .reset_index()
)

attrition["attrition_rate"] = (
    attrition["attrition_rate"] * 100
)

fig = px.bar(
    attrition,
    x="department",
    y="attrition_rate",
    color="department",
    text_auto=".2f",
    title="Attrition Rate by Department",
    labels={
        "attrition_rate": "Attrition Rate (%)"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# LABOR COST
# ============================================================

st.header("💰 Labor Cost Analysis")

labor_cost = (
    filtered_df
    .groupby("department")["total_labor_cost"]
    .sum()
    .reset_index()
    .sort_values(
        "total_labor_cost",
        ascending=False
    )
)

fig = px.bar(
    labor_cost,
    x="department",
    y="total_labor_cost",
    color="department",
    text_auto=".2f",
    title="Total Labor Cost by Department"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.success(
    "Workforce Productivity Dashboard loaded successfully!"
)