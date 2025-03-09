import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# helper function
def create_daily_rentals_df(df):
    df["dteday"] = pd.to_datetime(df["dteday"])  # Pastikan dteday dalam format datetime
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    
    # Ubah nama kolom agar lebih deskriptif
    daily_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return daily_rentals_df

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.groupby(by="mnth").cnt.sum().sort_values(ascending=False).reset_index()
    
    # Ubah nama kolom agar lebih deskriptif
    monthly_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    
    return monthly_rentals_df

def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby(by="hr").cnt.sum().sort_values(ascending=False).reset_index()

    # Ubah nama kolom agar lebih deskriptif
    hourly_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

    return hourly_rentals_df

# Load cleaned data
all_df = pd.read_csv("hour.csv")

# Pastikan 'dteday' dalam format datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Filter Data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
    
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
daily_rentals_df = create_daily_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df)
hourly_rentals_df = create_hourly_rentals_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

# Daily rentals
st.subheader('Daily Rentals')

col1 = st.columns(1)[0]

with col1:
    total_rentals = daily_rentals_df["total_rentals"].sum()  # Perbaikan di sini!
    st.metric("Total rentals", value=total_rentals)

# Membuat grafik daily rentals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],  # Pastikan ini dalam format datetime
    daily_rentals_df["total_rentals"],  # Perbaikan di sini!
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Monthly rentals
st.subheader('Monthly Rentals')

col2 = st.columns(1)[0]  # Menggunakan col2 agar tidak bentrok dengan daily rentals

with col2:
    total_monthly_rentals = monthly_rentals_df["total_rentals"].sum()
    st.metric("Total rentals", value=total_monthly_rentals)

# Membuat grafik monthly rentals
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=monthly_rentals_df, 
    x="mnth",  # Pastikan ini dalam format angka atau nama bulan
    y="total_rentals",
    palette="Blues_r"
)
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# Hourly rentals
st.subheader('Hourly Rentals')

col3 = st.columns(1)[0]  # Menggunakan col3 agar tidak bentrok dengan daily & monthly rentals

with col3:
    total_hourly_rentals = hourly_rentals_df["total_rentals"].sum()
    st.metric("Total rentals", value=total_hourly_rentals)

# Membuat grafik hourly rentals
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=hourly_rentals_df, 
    x="hr",  # Pastikan ini dalam format jam (0–23)
    y="total_rentals",
    palette="Oranges_r"
)
ax.set_xlabel("Hour", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

st.caption('Copyright © Dicoding 2023')