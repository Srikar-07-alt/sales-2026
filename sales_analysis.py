import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare data
data = pd.read_csv('sales_data.csv')
data['Revenue'] = data['Quantity'] * data['Price']
# Convert Date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

print("--- Sales Analysis Summary ---")

# 1. Revenue by Product
product_revenue = data.groupby('Product')['Revenue'].sum()
print("\nRevenue by Product:")
print(product_revenue)

plt.figure(figsize=(8, 5))
product_revenue.plot(kind='bar', color='skyblue')
plt.title('Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.tight_layout()

# 2. Revenue by Region
region_revenue = data.groupby('Region')['Revenue'].sum()
print("\nRevenue by Region:")
print(region_revenue)

plt.figure(figsize=(8, 5))
region_revenue.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Revenue by Region')
plt.ylabel('') # Hide the ylabel for pie chart
plt.tight_layout()

# 3. Revenue by Category
category_revenue = data.groupby('Category')['Revenue'].sum()
print("\nRevenue by Category:")
print(category_revenue)

# 4. Monthly Revenue Trend
monthly_revenue = data.set_index('Date').resample('ME')['Revenue'].sum()
print("\nMonthly Revenue Trend:")
print(monthly_revenue)

plt.figure(figsize=(10, 5))
monthly_revenue.plot(kind='line', marker='o', color='green')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid(True)
plt.tight_layout()

print("\nShowing plots...")
plt.show()
