import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

def total_rent_by_hours(df):
    rent_by_hour = df.groupby(by="hour").agg({"total_count":["sum"]})
    return rent_by_hour

def analysis_rent_by_hours(df):
    avg_rent = df.groupby("hour").total_count.mean().sort_values(ascending=False).reset_index()
    return avg_rent
def rent_by_season(df):
    rent_by_season = df.groupby("season").total_count.sum().sort_values(ascending=False).reset_index()
    return rent_by_season

def rent_by_weather(df):
    rent_by_weather = df.groupby("weather").total_count.nunique().sort_values(ascending=False).reset_index()
    return rent_by_weather

#Load cleaned data
dataset_bike = pd.read_csv("dataset_bike.csv")

datetime_columns = ['date']
dataset_bike.sort_values(by="date", inplace=True)
dataset_bike.reset_index(inplace=True)

for column in datetime_columns:
    dataset_bike[column] = pd.to_datetime(dataset_bike['date'])

min_date = dataset_bike['date'].min()
max_date = dataset_bike['date'].max()

with st.sidebar:
    #logo company
    st.image("https://miro.medium.com/v2/resize:fit:4096/1*GJ45uUnc49T-D5LdYn7CfQ.jpeg")
    #Mengambil start date dan end date
    start_date, end_date = st.date_input(
        label='Rentang tanggal',
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )
    df_by_days = dataset_bike[(dataset_bike['date'] >= str(start_date)) & 
                              (dataset_bike['date'] <= str(end_date))]
    df_rent_by_hours = total_rent_by_hours(df_by_days)
    df_analysis_rent_hours = analysis_rent_by_hours(df_by_days)
    df_rent_by_season = rent_by_season(df_by_days)
    df_rent_by_weather = rent_by_weather(df_by_days)
    
st.header('Bike Sharing')
st.subheader("Penyewaan Sepeda Berdasarkan musim")
colors = ['#FFBE98', '#FEECE2', '#F7DED0', '#E2BFB3']
plt.figure(figsize=(10, 5))

sns.barplot(
    y="total_count",
    x="season",
    data=df_rent_by_season.sort_values(by="total_count", ascending=False),
    palette=colors
)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
st.pyplot(plt)

st.subheader("Registered vs Casual")

plt.figure(figsize=(10, 5))
casual = sum(dataset_bike['casual'])
registered = sum(dataset_bike['registered'])

plt.title("Registered vs Casual", loc="center", fontsize=15)
data = [casual, registered]
labels = ['Casual', 'Registered']
plt.pie(data, labels=labels, autopct='%1.1f%%', colors=["#A5DD9B", "#F2C18D"])
st.pyplot(plt)