import pandas as pd

data = pd.read_csv("startup_funding.csv")


# Sample DataFrame

df = pd.DataFrame(data)

df['Amount in USD'] = df['Amount in USD'].str.replace(',', '')

# Convert column to numeric, setting errors='coerce' to convert invalid parsing to NaN
df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')

# Drop rows where 'Amount' is NaN (i.e., where conversion failed)
df = df.dropna(subset=['Amount in USD'])

# Convert 'Amount' back to integer
df['Amount'] = df['Amount in USD'].astype(int)

df = df.drop(columns = ["SubVertical", "Sr No", "Date dd/mm/yyyy", "InvestmentnType", "Investors Name", "Remarks"])
print(df.head(10))


df.to_csv('starups.csv', index=False)

