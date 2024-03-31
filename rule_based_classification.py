import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
pd.set_option("display.max_rows", None)
df = pd.read_csv("gitProject/rule_based_classification-main/persona.csv")
df.head()
df.shape
df.info()

def check_df(df, head=5):
    print("##################### Shape #####################")
    print(df.shape)
    print("##################### Types #####################")
    print(df.dtypes)
    print("##################### Head #####################")
    print(df.head(head))
    print("##################### Tail #####################")
    print(df.tail(head))
    print("##################### NA #####################")
    print(df.isnull().sum())
    print("##################### Summary #####################")
    print(df.describe().T)

check_df(df)

def grab_columns(df, categorical_th=10, cardinal_th=20):

    cat_col = [col for col in df.columns if str(df[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat_col = [col for col in df.columns if df[col].nunique() < categorical_th and df[col].dtypes in ["int64", "float64"]]
    cat_but_car_col = [col for col in df.columns if df[col].nunique() > cardinal_th and str(df[col].dtypes) in ["category", "object"]]
    cat_col = cat_col + num_but_cat_col
    cat_col = [col for col in cat_col if col not in cat_but_car_col]

    num_col = [col for col in df.columns if df[col].dtypes in ["int64", "float64"]]
    num_col = [col for col in num_col if col not in cat_col]

    print('Types of Columns in Dataset')
    print(f'No. of Categorical Columns: {len(cat_col)}')
    print(f'No. of Numerical Columns: {len(num_col)}')
    print(f'No. of Cardinal Columns: {len(cat_but_car_col)}')

    return cat_col, num_col, cat_but_car_col


cat_cols, num_cols, cat_but_car = grab_columns(df)

print("Categorical Variable Analysis")
print("Country")
fig = px.histogram(df, x="COUNTRY", color="COUNTRY", nbins=20)
fig.show()
print("Source (OS)")
fig = px.histogram(df, x="SOURCE", color="SOURCE", nbins=20)
fig.show()
print("Sex")
fig = px.histogram(df, x="SEX", color="SEX", nbins=20)
fig.show()


fig = px.histogram(df, x="AGE", nbins=20, title="Age Distribution")
fig.show()

fig = px.scatter(df, x="AGE", y="PRICE", color="SEX",title="Age and Price Distribution")
fig.show()

df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()
df.head()

agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()

agg_df = agg_df.reset_index()
agg_df.head()


bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

agg_df['customers_level_based'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_cat']].agg(lambda x: '_'.join(x).upper(), axis=1)

agg_df.columns

for row in agg_df.values:
    print(row)
    
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
    
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))
    
agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()
agg_df.head()

agg_df["customers_level_based"].value_counts()
agg_df.head()

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]



