import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# helper function
def create_monthly_rentals_df(df):
    monthly_rentals_df = df.groupby(by="mnth").cnt.sum().reset_index()
    monthly_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

    # Ubah angka bulan menjadi nama bulan
    months_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    monthly_rentals_df["mnth"] = monthly_rentals_df["mnth"].map(months_map)

    # Pastikan urutan bulan tetap sesuai kalender
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_rentals_df["mnth"] = pd.Categorical(
        monthly_rentals_df["mnth"], categories=month_order, ordered=True
    )
    return monthly_rentals_df.sort_values("mnth")

def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby(by="hr").cnt.sum().reset_index()
    hourly_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return hourly_rentals_df

# Load cleaned data
all_df = pd.read_csv("hour.csv")

# Pastikan 'dteday' dalam format datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Pilihan tahun (2011 atau 2012)
    selected_year = st.selectbox("Pilih Tahun", options=[2011, 2012])

# Filter berdasarkan tahun yang dipilih
filtered_df = all_df[all_df["yr"] == (selected_year - 2011)]

# Buat DataFrame bulanan
monthly_rentals_df = create_monthly_rentals_df(filtered_df)

# Buat DataFrame hourly rentals (tidak dipengaruhi filter tahun)
hourly_rentals_df = create_hourly_rentals_df(all_df)

st.header('Bike Sharing Dashboard :sparkles:')

# Monthly rentals
st.subheader('Total Rentals per Tahun')
total_rentals_year = filtered_df["cnt"].sum()
st.metric(f"Total Rentals Tahun {selected_year}", value=total_rentals_year)

# Membuat grafik monthly rentals
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=monthly_rentals_df, 
    x="mnth",  
    y="total_rentals",
    color="royalblue"
)
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# Hourly rentals
st.subheader('Hourly Rentals (Seluruh Tahun)')

# Warna gradasi: jam dengan rentals tertinggi lebih mencolok
max_rentals = hourly_rentals_df["total_rentals"].max()
colors = ["darkorange" if val == max_rentals else "sandybrown" for val in hourly_rentals_df["total_rentals"]]

# Membuat grafik hourly rentals
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=hourly_rentals_df, 
    x="hr",  
    y="total_rentals",
    palette=colors
)
ax.set_xlabel("Hour", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

st.caption('Copyright © Dicoding 2023')