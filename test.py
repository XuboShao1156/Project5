import pandas as pd

df = pd.read_csv('./pageviews.csv')


path = "Main_Page"

var = df.loc[df['path'] == path]

if var.empty:
    print('no such page')
else :
    hits = int(var['hits'])
    print(hits)
path = var['path']
#print(hits)
#print(str(path))