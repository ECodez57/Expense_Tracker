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
