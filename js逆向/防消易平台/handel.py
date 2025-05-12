import pandas as pd

# Read the first Excel file
df = pd.read_excel('所有企业.xlsx')
ids = df['creditCode']

# Read the second Excel file (待整改)
df2 = pd.read_excel('待整改.xlsx')
ids2 = df2['ID']

# Filter rows from df where creditCode exists in ids2
filtered_df = df[df['creditCode'].isin(ids2)]

# Save the filtered dataframe to a new Excel file
filtered_df.to_excel('待整改的企业-终.xlsx', index=False)

print(f"筛选的企业已保存到 '符合要求的企业.xlsx' 文件中，包含 {len(filtered_df)} 条记录。")
