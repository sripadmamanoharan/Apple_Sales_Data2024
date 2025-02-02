import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data  # Cache data for faster loading
def load_data():
    return pd.read_csv("apple_sales_2024.csv")  # Ensure this filename matches GitHub

df = load_data()  # Load the dataset

# Streamlit App UI
st.title("📊 AI-Powered Sales Performance Dashboard")

# Show Data
st.subheader("🔍 Sales Data Overview")
st.dataframe(df)


# Calculate KPIs
df["Total Sales (in million units)"] = (
    df["iPhone Sales (in million units)"] +
    df["iPad Sales (in million units)"] +
    df["Mac Sales (in million units)"] +
    df["Wearables (in million units)"]
)
df["Target Sales (in million units)"] = df["Total Sales (in million units)"] * 1.10
df["Performance (%)"] = (df["Total Sales (in million units)"] / df["Target Sales (in million units)"]) * 100
df["Performance_Status"] = df["Performance (%)"].apply(lambda x: "Above Target" if x >= 100 else "Below Target")

# Streamlit App Design
st.title("📊 AI-Driven Sales Performance Dashboard")

st.subheader("Sales Data Overview")
st.dataframe(df)

st.subheader("Performance Distribution")
performance_counts = df["Performance_Status"].value_counts()
st.bar_chart(performance_counts)

st.subheader("Total Sales by Product Type")
product_sales = df[["iPhone Sales (in million units)", "iPad Sales (in million units)",
                    "Mac Sales (in million units)", "Wearables (in million units)"]].sum().sort_values()
st.bar_chart(product_sales)

st.subheader("AI-Generated Sales Insights")
prompt = f"Analyze sales trends:\n{df.describe()}"
response = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key="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").invoke(prompt)
st.text(response.content)
