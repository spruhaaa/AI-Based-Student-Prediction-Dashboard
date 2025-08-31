import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="📊 Student Performance Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("student_data.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- Title & Description ---
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color:#114B8C;'>📊 Student Performance Dashboard</h1>
        <p style='font-size: 16px; color: #444;'>Interactive analytics dashboard to monitor academic performance and generate student reports.</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
gender_filter = st.sidebar.selectbox("Filter by Gender", options=["All"] + df["gender"].unique().tolist())
dept_filter = st.sidebar.selectbox("Filter by Department", options=["All"] + df["department"].unique().tolist())

# --- Apply Filters ---
filtered_df = df.copy()
if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender_filter]
if dept_filter != "All":
    filtered_df = filtered_df[filtered_df["department"] == dept_filter]

# --- KPIs Summary ---
st.markdown("### 📌 Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Students", len(filtered_df))
with col2:
    st.metric("Avg. Attendance (%)", round(filtered_df["attendance_percent"].mean(), 2))
with col3:
    st.metric("Avg. Internal Marks", round(filtered_df["internal_marks"].mean(), 2))

st.markdown("---")

# --- Display Filtered Data ---
st.markdown("### 🧾 Filtered Student Records")
st.dataframe(filtered_df, use_container_width=True, height=300)

# --- Chart 1: Attendance by Final Result (Boxplot) ---
st.markdown("### 📈 Attendance Distribution by Final Result")
fig1 = px.box(
    filtered_df, 
    x="final_result", 
    y="attendance_percent", 
    color="final_result",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    template="simple_white",
    title="Attendance % vs Final Result"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Internal & External Marks Distribution ---
st.markdown("### 📊 Marks Distribution")
col4, col5 = st.columns(2)
with col4:
    fig2 = px.histogram(
        filtered_df, 
        x="internal_marks", 
        nbins=15, 
        color_discrete_sequence=["#3498db"],
        marginal="box",
        title="Internal Marks",
        template="simple_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col5:
    fig3 = px.histogram(
        filtered_df, 
        x="external_marks", 
        nbins=15, 
        color_discrete_sequence=["#e74c3c"],
        marginal="box",
        title="External Marks",
        template="simple_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Report Generation ---
st.markdown("### 📤 Generate Individual Student Report")
selected_student_id = st.selectbox("🎓 Select Student ID", filtered_df["student_id"].unique())

if st.button("📄 Generate PDF Report"):
    student = filtered_df[filtered_df["student_id"] == selected_student_id].iloc[0]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(30, 30, 120)
    pdf.cell(200, 10, txt="Student Performance Report", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    pdf.ln(10)
    for label, value in student.items():
        pdf.cell(200, 10, txt=f"{label.capitalize()}: {value}", ln=True)

    pdf.output("student_report.pdf")

    with open("student_report.pdf", "rb") as file:
        st.download_button(
            label="📥 Download Student Report",
            data=file,
            file_name=f"{selected_student_id}_report.pdf",
            mime="application/pdf"
        )
