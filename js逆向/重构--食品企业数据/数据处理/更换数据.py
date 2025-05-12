# import pandas as pd
#
# df = pd.read_excel('企业基础信息(2).xlsx')
# df2 = pd.read_excel('企业股东信息(1).xlsx')
# dic = {}
# for k,v in df.iterrows():
#     dic[v['ids']] = v['统一社会信用代码']
# print(dic)
#
# for k, v in df2.iterrows():
#     if v['企业统一社会信用代码'] in dic.keys():
#         v['企业统一社会信用代码'] = dic[v['企业统一社会信用代码']]
#         df2.to_excel('股东信息2.xlsx', index=False)

import pandas as pd

df = pd.read_excel('企业基础信息1.xlsx')
df2 = pd.read_excel('企业经营信息.xlsx')
dic = {}
for k, v in df.iterrows():
    dic[v['ids']] = v['统一社会信用代码']

# print(dic)
for k, v in df2.iterrows():
    print(v['企业统一社会信用代码'])

# Filter out rows in df2 where '企业统一社会信用代码' is not present in dic
df2 = df2[df2['企业统一社会信用代码'].isin(dic.keys())]

# Update the '企业统一社会信用代码' column in df2 based on the mapping with dic
df2['企业统一社会信用代码'] = df2['企业统一社会信用代码'].map(dic)

# Save the updated DataFrame to a new Excel file
df2.to_excel('经营信息2.xlsx', index=False)