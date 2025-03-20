import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from babel.numbers import format_currency
from streamlit.components.v1 import iframe

sns.set(style='dark')

file_path = 'main_data.csv'
df_combined = pd.read_csv(file_path)

df_combined['date'] = pd.to_datetime(df_combined[['year', 'month', 'day']])

st.title("Dashboard Air Pollution Analysis")

min_date = df_combined["date"].min()
max_date = df_combined["date"].max()

with st.sidebar:
    st.image("logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    selected_city = st.multiselect(
        "Pilih Kota/Stasiun:", options=df_combined["station"].unique(), default=df_combined["station"].unique()
    )

filtered_df = df_combined[(df_combined["date"] >= pd.to_datetime(start_date)) & 
                          (df_combined["date"] <= pd.to_datetime(end_date)) & 
                          (df_combined["station"].isin(selected_city))]

st.write("""
    Data yang diolah adalah dua belas data dalam format csv yang berisi informasi terkait kualitas udara di berbagai stasiun pengukuran dari Maret 2013 hingga Februari 2017. Setiap file mewakili data yang dikumpulkan di stasiun pengukuran udara yang berbeda, dengan variabel yang mencakup tingkat polusi udara seperti PM2.5, PM10, SO2, NO2, CO, O3, serta beberapa faktor cuaca seperti suhu (TEMP), kelembaban (DEWP), tekanan udara (PRES), curah hujan (RAIN), dan kecepatan angin (WSPM).

Stasiun-stasiun yang tercatat dalam dataset meliputi area-area dengan tingkat polusi yang bervariasi, yang memungkinkan analisis tentang bagaimana faktor-faktor cuaca dan polutan tertentu berhubungan dengan kualitas udara. Setiap stasiun dilengkapi dengan data tahun, bulan, dan hari yang memungkinkan analisis tren polusi sepanjang waktu.
""")
unique_stations = df_combined['station'].nunique()

min_date = df_combined['date'].min()
max_date = df_combined['date'].max()

col1, col2 = st.columns([1, 1])
col1.write("Data yang diolah terdiri dari:")

rows, cols = df_combined.shape
with col1:
    st.metric("Jumlah Baris", rows)
    st.metric("Jumlah Kolom", cols)
    st.metric("Jumlah Stasiun Pengukuran", unique_stations)

with col2:
    st.metric("Rentang Waktu Data", f"{min_date.strftime('%d %B %Y')}")
    st.metric("Hingga", f"{max_date.strftime('%d %B %Y')}")


st.caption("---")

st.subheader("Ringkasan Data")
st.write(filtered_df.describe())

st.subheader("Tren Polusi Udara dari Waktu ke Waktu (PM2.5 dan PM10)")
monthly_trend = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))[['PM2.5', 'PM10']].mean().reset_index()
fig, ax = plt.subplots(figsize=(14, 6))

sns.lineplot(x=monthly_trend['date'].astype(str), y=monthly_trend['PM2.5'], marker='o', label="PM2.5")
sns.lineplot(x=monthly_trend['date'].astype(str), y=monthly_trend['PM10'], marker='s', label="PM10")

ax.set_title("Tren PM2.5 dan PM10 dari Waktu ke Waktu", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Konsentrasi (µg/m³)", fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
ax.legend()
st.pyplot(fig)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Distribusi PM2.5")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(filtered_df['PM2.5'], kde=True, ax=ax)
    ax.set_title("Distribusi PM2.5")
    ax.set_xlabel("Konsentrasi PM2.5 (µg/m³)")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

with col2:
    st.subheader("Distribusi PM10")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(filtered_df['PM10'], kde=True, ax=ax)
    ax.set_title("Distribusi PM10")
    ax.set_xlabel("Konsentrasi PM10 (µg/m³)")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

st.subheader("Korelasi Antara Polutan dan Cuaca")
correlation_matrix = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Distribusi PM2.5 di Setiap Stasiun")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(x='station', y='PM2.5', data=df_combined, ax=ax)
    ax.set_title("Distribusi PM2.5 di Setiap Stasiun")
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Distribusi PM10 di Setiap Stasiun")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(x='station', y='PM10', data=df_combined, ax=ax)
    ax.set_title("Distribusi PM10 di Setiap Stasiun")
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Konsentrasi PM10 (µg/m³)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.caption("---")

recent_pollution = df_combined.groupby('station').agg({'date': 'max'}).reset_index()
recent_pollution['Recency'] = (df_combined['date'].max() - recent_pollution['date']).dt.days

threshold = 35
high_pollution_frequency = df_combined[df_combined['PM2.5'] > threshold].groupby('station').size().reset_index(name='Frequency')

monetary_pollution = df_combined.groupby('station').agg({'PM2.5': 'mean', 'PM10': 'mean'}).reset_index()
monetary_pollution['Monetary'] = monetary_pollution[['PM2.5', 'PM10']].mean(axis=1)

rfm_df = recent_pollution.merge(high_pollution_frequency, on='station', how='left')
rfm_df = rfm_df.merge(monetary_pollution[['station', 'Monetary']], on='station', how='left')

rfm_df['RFM_Score'] = rfm_df['Recency'] + rfm_df['Frequency'] + rfm_df['Monetary']

rfm_df = rfm_df.sort_values('RFM_Score', ascending=False)

yearly_trend = df_combined.groupby(['year', 'station'])['PM2.5'].mean().reset_index()

plt.figure(figsize=(10, 6))
for city in yearly_trend['station'].unique():
    city_data = yearly_trend[yearly_trend['station'] == city]
    plt.plot(city_data['year'], city_data['PM2.5'], label=city)

plt.title('Yearly Pollution Trend (PM2.5)')
plt.xlabel('Year')
plt.ylabel('Average PM2.5 (µg/m³)')
plt.legend()
plt.show()

st.write("Level Polusi Dari Setiap Station Berdasarkan Analisis RFM")
st.write(yearly_trend)

st.write("Station dengan polusi tertinggi berdasarkan analisis RFM")
st.write(rfm_df.head())

st.caption("---")
st.caption("Fadhillah Rahmad Kurnia || 	MC184D5Y0386 || DBS Cooding Camp @ 2024 All Rights Reserved")
