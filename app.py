import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import date

# ---------- Sample Prediction Data (replace with your real data or CSV) ----------
data = {
    "Date": ["2025-08-01", "2025-08-01", "2025-08-02", "2025-08-03", "2025-08-03"],
    "League": ["Premier League", "La Liga", "Premier League", "Serie A", "La Liga"],
    "Outcome": ["✅ Correct", "❌ Wrong", "✅ Correct", "❌ Wrong", "✅ Correct"]
}
df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])
df["Correct"] = df["Outcome"] == "✅ Correct"

# ---------- Data Preparation ----------
accuracy_over_time = df.groupby("Date")["Correct"].mean() * 100
outcome_counts = df["Outcome"].value_counts()
league_counts = df["League"].value_counts()

# ---------- Streamlit App ----------
st.set_page_config(page_title="Soccer Prediction App", layout="centered")
st.title("⚽ Soccer Prediction Dashboard")
st.subheader("📊 Analytics Overview")

# ---------- Line Chart: Accuracy Over Time ----------
st.markdown("### 📈 Accuracy Over Time")
st.line_chart(accuracy_over_time)

# ---------- Pie Chart: Outcome Distribution ----------
st.markdown("### 🥧 Outcome Distribution")
fig_pie = px.pie(
    values=outcome_counts.values,
    names=outcome_counts.index,
    title="Prediction Outcome Distribution"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---------- Bar Chart: Predictions per League ----------
st.markdown("### 📊 Predictions per League")
fig_bar = px.bar(
    x=league_counts.index,
    y=league_counts.values,
    labels={"x": "League", "y": "Predictions"},
    title="Predictions by League"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------- Excel Export ----------
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Predictions')
    return output.getvalue()

st.markdown("### 📥 Download as Excel")
excel_data = convert_df_to_excel(df)
today = date.today().strftime("%Y-%m-%d")
st.download_button(
    label="📤 Download Predictions Excel",
    data=excel_data,
    file_name=f"predictions_{today}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ---------- Show Raw Data (Optional) ----------
with st.expander("📂 Show Prediction Data"):
    st.dataframe(df)
