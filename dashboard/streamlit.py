import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from babel.numbers import format_currency

sns.set(style='dark')

file_path = 'main_data.csv'
df_combined = pd.read_csv(file_path)

df_combined['date'] = pd.to_datetime(df_combined[['year', 'month', 'day']])

st.title("Dashboard Kualitas Udara")

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
    Dashboard ini memberikan visualisasi mengenai kualitas udara berdasarkan data polutan seperti PM2.5, PM10, NO2, CO, dan faktor cuaca seperti suhu dan kecepatan angin.
    Data yang digunakan mencakup berbagai stasiun pengukuran kualitas udara.
""")


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
st.caption("Fadhil DBS @ 2024 All Rights Reserved")