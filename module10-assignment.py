# Module 10 Assignment: Data Manipulation and Cleaning with Pandas
# UrbanStyle Customer Data Cleaning

# Import required libraries
import pandas as pd


# Welcome message
print("=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO SIMULATE A CSV FILE (DO NOT MODIFY) -----
from io import StringIO

# Simulated CSV content with intentional data issues
csv_content = """customer_id,first_name,last_name,email,phone,join_date,last_purchase,total_purchases,total_spent,preferred_category,satisfaction_rating,age,city,state,loyalty_status
CS001,John,Smith,johnsmith@email.com,(555) 123-4567,2023-01-15,2023-12-01,12,"1,250.99",Menswear,4.5,35,Tampa,FL,Gold
CS002,Emily,Johnson,emily.j@email.com,555.987.6543,01/25/2023,10/15/2023,8,$875.50,Womenswear,4,28,Miami,FL,Silver
CS003,Michael,Williams,mw@email.com,(555)456-7890,2023-02-10,2023-11-20,15,"2,100.75",Footwear,5,42,Orlando,FL,Gold
CS004,JESSICA,BROWN,jess.brown@email.com,5551234567,2023-03-05,2023-12-10,6,659.25,Womenswear,3.5,31,Tampa,FL,Bronze
CS005,David,jones,djones@email.com,555-789-1234,2023-03-20,2023-09-18,4,350.00,Menswear,,45,Jacksonville,FL,Bronze
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS007,Robert,Davis,robert.davis@email.com,555.444.7777,04/30/2023,11/25/2023,7,$725.80,Footwear,4.5,38,Miami,FL,Silver
CS008,Jennifer,Garcia,jen.garcia@email.com,(555)876-5432,2023-05-15,2023-10-30,3,280.50,ACCESSORIES,3,25,Orlando,FL,Bronze
CS009,Michael,Williams,m.williams@email.com,5558889999,2023-06-01,2023-12-07,9,1100.00,Menswear,4,39,Jacksonville,FL,Silver
CS010,Emily,Johnson,emilyjohnson@email.com,555-321-6547,2023-06-15,2023-12-15,14,"1,875.25",Womenswear,4.5,27,Miami,FL,Gold
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS011,Amanda,,amanda.p@email.com,(555) 741-8529,2023-07-10,,2,180.00,womenswear,3,32,Tampa,FL,Bronze
CS012,Thomas,Wilson,thomas.w@email.com,,2023-07-25,2023-11-02,5,450.75,menswear,4,44,Orlando,FL,Bronze
CS013,Lisa,Anderson,lisa.a@email.com,555.159.7530,08/05/2023,,0,0.00,Womenswear,,30,Miami,FL,
CS014,James,Taylor,jtaylor@email.com,555-951-7530,2023-08-20,2023-10-10,11,"1,520.65",Footwear,4.5,,Jacksonville,FL,Gold
CS015,Karen,Thomas,karen.t@email.com,(555) 357-9512,2023-09-05,2023-12-12,6,685.30,Womenswear,4,36,Tampa,FL,Silver
"""

# Create a StringIO object (simulates a file)
customer_data_csv = StringIO(csv_content)


# TODO 1: Load and Explore the Dataset
raw_df = pd.read_csv(customer_data_csv)
initial_missing_counts = raw_df.isnull().sum()
initial_duplicate_count = raw_df.duplicated().sum()


# TODO 2: Handle Missing Values
missing_value_report = raw_df.isnull().sum()


# 2.2 Fill missing satisfaction_rating with the median value
satisfaction_median = raw_df['satisfaction_rating'].median()
raw_df['satisfaction_rating'].fillna(satisfaction_median, inplace=True)


# 2.3 Fill missing last_purchase dates appropriately
date_fill_strategy = 'forward_fill'
raw_df['last_purchase'].fillna(method='ffill', inplace=True)


# 2.4 Handle other missing values as needed
raw_df['last_name'].fillna("Unknown", inplace=True)
raw_df['phone'].fillna("0000000000", inplace=True)
raw_df['loyalty_status'].fillna("Bronze", inplace=True)
raw_df['age'].fillna(raw_df['age'].median(), inplace=True)
df_no_missing = raw_df.copy()


# TODO 3: Correct Data Types
# 3.1 Convert join_date and last_purchase to datetime
df_typed = df_no_missing.copy()
df_typed['join_date'] = pd.to_datetime(df_typed['join_date'], errors='coerce')
df_typed['last_purchase'] = pd.to_datetime(df_typed['last_purchase'], errors='coerce')


# 3.2 Convert total_spent to numeric (handle currency symbols and commas)
df_typed['total_spent'] = df_typed['total_spent'].replace(r'[\$,]', '', regex=True).astype(float)


# 3.3 Ensure other numeric fields (total_purchases, age) are correct types
df_typed['total_purchases'] = df_typed['total_purchases'].astype(int)
df_typed['age'] = df_typed['age'].astype(int)


# TODO 4: Clean and Standardize Text Data
# 4.1 Standardize case for first_name and last_name (proper case)
df_text_cleaned = df_typed.copy()
df_text_cleaned['first_name'] = df_text_cleaned['first_name'].str.title()
df_text_cleaned['last_name'] = df_text_cleaned['last_name'].str.title()
# 4.2 Standardize category names (consistent capitalization)
df_text_cleaned['preferred_category'] = df_text_cleaned['preferred_category'].str.title()


# 4.3 Standardize phone numbers to a consistent format
phone_format = "(XXX) XXX-XXXX"
df_text_cleaned['phone'] = df_text_cleaned['phone'].str.replace(r'\D', '', regex=True)
df_text_cleaned['phone'] = df_text_cleaned['phone'].apply(
    lambda x: f"({x[:3]}) {x[3:6]}-{x[6:]}" if len(x) == 10 else x
)


# TODO 5: Remove Duplicates
# 5.1 Identify duplicate records
duplicate_count = df_text_cleaned.duplicated().sum()


# 5.2 Remove duplicates while keeping the appropriate record
df_no_duplicates = df_text_cleaned.drop_duplicates()


# TODO 6: Add Derived Features
# 6.1 Calculate days_since_last_purchase
df_no_duplicates['days_since_last_purchase'] = (
    pd.Timestamp.today() - df_no_duplicates['last_purchase']
).dt.days


# 6.2 Calculate average_purchase_value (total_spent / total_purchases)
df_no_duplicates['average_purchase_value'] = (
    df_no_duplicates['total_spent'] / df_no_duplicates['total_purchases']
)


# 6.3 Create a purchase_frequency_category (High, Medium, Low)
def categorize(p):
    if p >= 10:
        return "High"
    elif p >= 5:
        return "Medium"
    else:
        return "Low"
df_no_duplicates['purchase_frquency_category'] = df_no_duplicates['total_purchases'].apply(categorize)


# TODO 7: Clean Up the DataFrame
df_renamed = df_no_duplicates.rename(columns={
    'customer_id': 'CustomerID',
    'first_name': 'FirstName',
    'last_name': 'LastName',
    'total_spent': 'TotalSpent'
})


# 7.2 Remove any unnecessary columns
df_final = df_renamed.drop(columns=['email'])


# 7.3 Sort the data by a meaningful attribute
df_final = df_final.sort_values(by='TotalSpent', ascending=False)


# TODO 8: Generate Insights from Cleaned Data
# 8.1 Calculate average spent by loyalty_status
avg_spent_by_loyalty = df_final.groupby('loyalty_status')['TotalSpent'].mean()


# 8.2 Find top preferred categories by total_spent
category_revenue = df_final.groupby('preferred_category')['TotalSpent'].sum().sort_values(ascending=False)


# 8.3 Calculate correlation between satisfaction_rating and total_spent
satisfaction_spend_corr = df_final['satisfaction_rating'].corr(df_final['TotalSpent'])


# TODO 9: Generate Final Report
print("\n" + "=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING REPORT")
print("=" * 60)

# 9.1 Report on data quality issues found and how they were addressed
print("\nData Quality Issues:")
print(f"- Missing Values: {initial_missing_counts.sum()} total missing entries")
print(f"- Duplicates: {initial_duplicate_count} duplicate records found")
print("- Data Type Issues: Dates, currency formatting, inconsistent text")


# 9.2 Describe the changes made to standardize the dataset
print("\nStandardization Changes:")
print("- Names: Converted to proper case")
print("- Categories: Standardized capitalization")
print(f"- Phone Numbers: Formatted as {phone_format}")


# 9.3 Present key business insights from the cleaned data
print("\nKey Business Insights:")
print(f"- Customer Base: {df_final.shape[0]} total customers")
print("- Revenge by Loyalty:")
print(avg_spent_by_loyalty)
print(f"- Top Category: {category_revenue.idxmax()} with ${category_revenue.max():.2f} revenue")


# 9.4 Display the first few rows of the clean, analysis-ready dataset
print("\nSample Cleaned Data:")
print(df_final.head())
