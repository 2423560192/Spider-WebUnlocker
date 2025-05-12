import pandas as pd

df = pd.read_excel('企业基础信息(2).xlsx')

for v, k in df.iterrows():
    if '市' in k['省级']:
        k['市级'] = k['省级']
        k['省级'] = '-'
df.to_excel('基础信息2.xlsx')
