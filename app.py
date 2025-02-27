# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f5lrkDUUwZGqv0rMgRY2s2FArU1ToxQH

#Step 1: Install and Set Up Environment
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

#Step 2: Load and Explore Sales Data

# Load CSV file
df = pd.read_csv("apple_sales_2024.csv")  # Change filename as needed

# Display first few rows
df.head()

# Get data summary
df.info()

# Check for missing values
print(df.isnull().sum())

#Step 3: Preprocess Data and Compute KPIs

# Compute Total Sales
df["Total Sales (in million units)"] = (
    df["iPhone Sales (in million units)"] +
    df["iPad Sales (in million units)"] +
    df["Mac Sales (in million units)"] +
    df["Wearables (in million units)"]
)

# Define Target Sales (10% higher than actual sales)
df["Target Sales (in million units)"] = df["Total Sales (in million units)"] * 1.10

# Calculate Sales Performance
df["Performance (%)"] = (df["Total Sales (in million units)"] / df["Target Sales (in million units)"]) * 100
df["Performance_Status"] = df["Performance (%)"].apply(lambda x: "Above Target" if x >= 100 else "Below Target")

# Show processed data
df.head()

#Step 4: Implement AI-Powered Sales Analysis

#Step 4.1: Set Up AI- Powered Sales Insights Using LangChain


# Set OpenAI API Key
openai_api_key = "OPENAI_API_KEY" 

import streamlit as st
from langchain_openai import ChatOpenAI

# Load OpenAI API Key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Debugging: Print API key length
st.write(f"API Key Length: {len(openai_api_key)} characters")

# Check if API key is loaded
if not openai_api_key or len(openai_api_key) < 30:
    st.error("🚨 OpenAI API Key is missing or incorrect! Please update in Streamlit Secrets.")
else:
    st.success("✅ OpenAI API Key Loaded Successfully!")

# Initialize OpenAI Model
llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=openai_api_key)

#Step 4.2: Define AI Functions as LangChain Tools

# Tool 1: Analyze Sales Data
def load_sales_data(*args, **kwargs):
    return df.describe().to_string()

# Tool 2: AI-Powered Sales Insights
def interpret_sales_results(*args, **kwargs):
    prompt = f"""
    Analyze the following sales data trends and provide strategic recommendations for CXOs:

    {df.describe()}

    1. Identify key trends in sales.
    2. Highlight strengths in the current sales strategy.
    3. Identify underperforming areas and provide **specific strategies to improve them**.
    4. Recommend actions for optimizing sales performance.

    Your insights should be actionable and useful for executives to make **data-driven decisions**.
    """

    response = llm.invoke(prompt)
    return response.content  # Correct indentation

# Define LangChain Tools
tools = [
    Tool(name="Sales Data Analysis", func=load_sales_data, description="Provides key sales statistics."),
    Tool(name="Sales Insights", func=interpret_sales_results, description="Generates insights for CXOs.")
]

#Step 4.3: Initialize AI Agent and Run Analysis

# Create the AI Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask AI Agent to analyze sales data and provide insights
response = agent.invoke("Analyze the sales data and provide key insights for business executives.")

# Print AI-generated insights
print(response)

# Run the Updated AI Agent

# AI Agent Execution
response = agent.invoke("Analyze the sales data and provide key recommendations for CXOs.")

# Print the AI-generated insights
print(response)

#Step 5 : Implement Sales Forecasting with Machine Learning- CXOs predict future sales

from prophet import Prophet

# Convert dataset to a time-series format
df["Date"] = pd.date_range(start="2023-01-01", periods=len(df), freq="ME")

df_forecast = df[["Date", "Total Sales (in million units)"]].copy()
df_forecast.rename(columns={"Date": "ds", "Total Sales (in million units)": "y"}, inplace=True)

# Train-Test Split
train = df_forecast.iloc[:-12]  # Use all but the last 12 months for training
test = df_forecast.iloc[-12:]   # Last 12 months for testing

# Train the Prophet Model
model = Prophet()
model.fit(train)

# Make future predictions
future = model.make_future_dataframe(periods=12, freq="M")
forecast = model.predict(future)

# Plot Forecast
fig = model.plot(forecast)
plt.title("Sales Forecast for Next 12 Months")
plt.show()

#Step 6: Visualize KPI Dashboards

#Chart 1: Actual vs. Target Sales by Region


plt.figure(figsize=(10, 6))

# Plot bars without error bars
sns.barplot(data=df, x="Region", y="Total Sales (in million units)", color="skyblue", label="Actual Sales", errorbar=None)
sns.barplot(data=df, x="Region", y="Target Sales (in million units)", color="salmon", alpha=0.6, label="Target Sales", errorbar=None)

plt.title("Actual vs. Target Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales (in million units)")

# Move legend outside
plt.legend(loc="upper left", bbox_to_anchor=(1,1))

# Show values on bars
for index, value in enumerate(df["Total Sales (in million units)"]):
    plt.text(index, value + 1, f"{value:.1f}", ha='center', fontsize=10, color='black')

plt.xticks(rotation=45)
plt.gcf().set_constrained_layout(True)
plt.show()

#Chart 2: Performance Status Distribution

plt.figure(figsize=(6, 6))

# Count occurrences of performance status
performance_counts = df["Performance_Status"].value_counts()

# Plot pie chart
performance_counts.plot.pie(autopct="%1.1f%%", startangle=140, colors=["lightcoral", "lightgreen"])

# Improve title
plt.title(f"Sales Performance Status \n(Total Records: {len(df)})", fontsize=14, fontweight="bold")

plt.ylabel('')
plt.show()

#Step 7: Deploy an AI-Powered KPI Dashboard

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py

 
# Streamlit App

import streamlit as st  # ✅ Streamlit must be imported first

# ✅ `st.set_page_config()` must be the very first Streamlit command
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

# Now you can add other Streamlit elements
st.title("📊 AI-Powered Sales Insights Dashboard")
st.write("Welcome to the AI-powered sales dashboard for CXOs.")


# Data Overview
st.subheader("🔍 Sales Data Overview")
st.dataframe(df)

# AI-Generated Insights
st.subheader("🤖 AI-Generated Sales Insights")
if st.button("Generate AI Insights"):
    with st.spinner("Processing AI Insights..."):
        response = llm.invoke("Analyze the sales data and provide key recommendations for CXOs.")
    st.write(response)  

# Data
df["Sales Difference"] = df["Total Sales (in million units)"] - df["Target Sales (in million units)"]

st.subheader("📊 Actual vs. Target Sales by Region")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=df["Region"], y=df["Sales Difference"], ax=ax, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Difference Between Actual and Target Sales by Region")
st.pyplot(fig)  # ✅ Ensure this line is present

st.subheader("📈 Performance Status Distribution")
fig, ax = plt.subplots(figsize=(8, 5))
df["Performance_Status"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
plt.ylabel("")
plt.title("Performance Status Breakdown")
st.pyplot(fig)  # ✅ Ensure this line is present


