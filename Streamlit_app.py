import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Expense Tracker Dashboard", page_icon="📊", layout="wide")
st.title("📈 Expense Tracker Dashboard")

# Database Connection
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="EXPENSE_DB"
    )

# SQL Queries
QUERIES = {
    "Total Expenses": "SELECT COUNT(*) AS Total_Expenses FROM expense_data;",
    "Total Amount Spent": "SELECT SUM(Amount) AS Total_Amount FROM expense_data;",
    "Average Expense": "SELECT AVG(Amount) AS Avg_Amount FROM expense_data;",
    "Top 5 Categories by Expense": """
        SELECT Category, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Category
        ORDER BY Total_Amount DESC
        LIMIT 5;
    """,
    "Monthly Spending Trend": """
        SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Month
        ORDER BY Month;
    """,
    "Daily Spending Trend": """
        SELECT DATE(Date) AS Day, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Day
        ORDER BY Day;
    """,
    "Expenses by Payment Mode": """
        SELECT Payment_Mode, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Payment_Mode;
    """,
    "Highest Single Expense": "SELECT * FROM expense_data ORDER BY Amount DESC LIMIT 1;",
    "Lowest Single Expense": "SELECT * FROM expense_data ORDER BY Amount ASC LIMIT 1;",
    "Expenses in the Last 7 Days": """
        SELECT DATE(Date) AS Day, SUM(Amount) AS Total_Amount
        FROM expense_data
        WHERE Date >= DATE(NOW()) - INTERVAL 7 DAY
        GROUP BY Day;
    """,
    "Most Frequent Categories": """
        SELECT Category, COUNT(*) AS Frequency
        FROM expense_data
        GROUP BY Category
        ORDER BY Frequency DESC
        LIMIT 5;
    """,
    "Top Payment Modes by Frequency": """
        SELECT Payment_Mode, COUNT(*) AS Frequency
        FROM expense_data
        GROUP BY Payment_Mode
        ORDER BY Frequency DESC;
    """,
    "Expenses by Description (Top 10)": """
        SELECT Description, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Description
        ORDER BY Total_Amount DESC
        LIMIT 10;
    """,
    "Category-Wise Average Spending": """
        SELECT Category, AVG(Amount) AS Avg_Spending
        FROM expense_data
        GROUP BY Category;
    """,
    "Yearly Spending Summary": """
        SELECT YEAR(Date) AS Year, SUM(Amount) AS Total_Amount
        FROM expense_data
        GROUP BY Year
        ORDER BY Year;
    """,
    "Categories with Cashback": """
        SELECT Category, SUM(Cashback) AS Total_Cashback
        FROM expense_data
        WHERE Cashback > 0
        GROUP BY Category
        ORDER BY Total_Cashback DESC;
    """,
    "Expenses Below Median Amount": """
       SELECT *
       FROM expense_data
       WHERE Amount > (
           SELECT Amount
           FROM (
               SELECT Amount, 
                      ROW_NUMBER() OVER (ORDER BY Amount) AS row_num
               FROM expense_data
           ) AS ranked
           WHERE row_num = (SELECT CEIL(COUNT(Amount) / 2) FROM expense_data)
           LIMIT 1
       )
       ORDER BY Amount ASC;
    """,
    "Expenses Above Median Amount": """
       SELECT *
       FROM expense_data
       WHERE Amount > (
           SELECT Amount
           FROM (
               SELECT Amount, 
                      ROW_NUMBER() OVER (ORDER BY Amount) AS row_num
               FROM expense_data
           ) AS ranked
           WHERE row_num = (SELECT CEIL(COUNT(Amount) / 2) FROM expense_data)
           LIMIT 1
       )
       ORDER BY Amount DESC;
    """,
    "Cashback Utilization by Payment Mode": """
        SELECT Payment_Mode, SUM(Cashback) AS Total_Cashback
        FROM expense_data
        GROUP BY Payment_Mode
        ORDER BY Total_Cashback DESC;
    """,
    "Average Daily Spending": """
        SELECT DATE(Date) AS Day, AVG(Amount) AS Avg_Spending
        FROM expense_data
        GROUP BY Day
        ORDER BY Day;
    """
}

# Query Execution
def execute_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Sidebar Options
st.sidebar.header("Filter Options")
selected_query = st.sidebar.selectbox("Select Options", list(QUERIES.keys()))

# Execute and Display Query Results
if st.sidebar.button("Run Query"):
    try:
        query = QUERIES[selected_query]
        result = execute_query(query)

        st.subheader(f"Results for: {selected_query}")
        st.dataframe(result)

        # Visualizations
        if selected_query in ["Top 5 Categories by Expense", "Expenses by Payment Mode", "Monthly Spending Trend"]:
            if "Category" in result.columns and "Total_Amount" in result.columns:
                # Pie Chart for Top 5 Categories
                plt.figure(figsize=(6, 5))
                plt.pie(result["Total_Amount"], labels=result["Category"], autopct='%1.1f%%', startangle=140)
                plt.title("Expense Breakdown by Category")
                st.pyplot(plt)
            elif "Payment_Mode" in result.columns and "Total_Amount" in result.columns:
                # Bar Chart for Payment Mode
                plt.figure(figsize=(8, 5))
                plt.bar(result["Payment_Mode"], result["Total_Amount"], color='skyblue')
                plt.title("Expenses by Payment Mode")
                plt.xlabel("Payment Mode")
                plt.ylabel("Total Amount")
                st.pyplot(plt)
            elif "Month" in result.columns and "Total_Amount" in result.columns:
                # Line Chart for Monthly Spending Trend
                plt.figure(figsize=(8, 5))
                plt.plot(result["Month"], result["Total_Amount"], marker='o', color='green')
                plt.title("Monthly Spending Trend")
                plt.xlabel("Month")
                plt.ylabel("Total Amount")
                plt.xticks(rotation=45)
                st.pyplot(plt)

        elif selected_query in ["Expenses Above Median Amount", "Expenses Below Median Amount"]:
            if "Amount" in result.columns:
                plt.figure(figsize=(8, 5))
                plt.hist(result["Amount"], bins=20, color='blue', alpha=0.7)
                plt.title(f"Expenses {'Above' if 'Above' in selected_query else 'Below'} Median Amount")
                plt.xlabel("Amount")
                plt.ylabel("Frequency")
                st.pyplot(plt)

        elif selected_query in ["Cashback Utilization by Payment Mode"]:
            if "Payment_Mode" in result.columns and "Total_Cashback" in result.columns:
                plt.figure(figsize=(8, 5))
                plt.bar(result["Payment_Mode"], result["Total_Cashback"], color='orange')
                plt.title("Cashback Utilization by Payment Mode")
                plt.xlabel("Payment Mode")
                plt.ylabel("Total Cashback")
                st.pyplot(plt)

        elif selected_query in ["Yearly Spending Summary", "Daily Spending Trend"]:
            if "Year" in result.columns and "Total_Amount" in result.columns:
                plt.figure(figsize=(8, 5))
                plt.bar(result["Year"], result["Total_Amount"], color='purple')
                plt.title("Yearly Spending Summary")
                plt.xlabel("Year")
                plt.ylabel("Total Amount")
                st.pyplot(plt)
            elif "Day" in result.columns and "Total_Amount" in result.columns:
                plt.figure(figsize=(8, 5))
                plt.plot(result["Day"], result["Total_Amount"], marker='o', color='purple')
                plt.title("Daily Spending Trend")
                plt.xlabel("Day")
                plt.ylabel("Total Amount")
                plt.xticks(rotation=45)
                st.pyplot(plt)

        elif selected_query == "Average Daily Spending":
            if "Day" in result.columns and "Avg_Spending" in result.columns:
                plt.figure(figsize=(8, 5))
                plt.plot(result["Day"], result["Avg_Spending"], marker='o', color='orange')
                plt.title("Average Daily Spending")
                plt.xlabel("Day")
                plt.ylabel("Average Spending")
                plt.xticks(rotation=45)
                st.pyplot(plt)

    except Exception as e:
        st.error(f"An error occurred: {e}")
