import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# helper function
def create_monthly_rentals_df(df):
    monthly_rentals_df = df.groupby(by=["yr", "mnth"]).cnt.sum().reset_index()
    # Ubah angka bulan menjadi nama bulan
    months_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    monthly_rentals_df["mnth"] = monthly_rentals_df["mnth"].map(months_map)
    return monthly_rentals_df

def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby(by="hr").cnt.sum().reset_index()
    return hourly_rentals_df

def create_seasonal_rentals_df(df):
    season_rentals_df = df.groupby(by=["yr", "season"]).cnt.sum().reset_index()
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_rentals_df["season"] = season_rentals_df["season"].map(season_mapping)
    return season_rentals_df
# Load cleaned data
all_df = pd.read_csv("data/hour.csv")

# Pastikan 'dteday' dalam format datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/family-riding-bikes-city-park_74855-5243.jpg?t=st=1742129893~exp=1742133493~hmac=c50fa4e23914b9f366da3f8f6e7492875f6e6aa81154dcd4fb64eeed5e2e2285&w=1800")
    
    
    # Pilihan tahun (2011 atau 2012)
    selected_year = st.selectbox("Pilih Tahun", options=[2011, 2012])

# Filter berdasarkan tahun yang dipilih
filtered_df = all_df[all_df["yr"] == (selected_year - 2011)]

# Buat DataFrame bulanan
monthly_rentals_df = create_monthly_rentals_df(filtered_df)
yearly_rentals_df = create_monthly_rentals_df(all_df)

# Buat DataFrame hourly rentals (tidak dipengaruhi filter tahun)
hourly_rentals_df = create_hourly_rentals_df(all_df)
seasonal_rentals_df = create_seasonal_rentals_df(all_df)

st.header('Bike Sharing Dashboard :sparkles:')

# Monthly rentals
st.subheader('Total Rentals per Tahun')
total_rentals_year = filtered_df["cnt"].sum()
st.metric(f"Total Rentals Tahun {selected_year}", value=total_rentals_year)

# Membuat grafik monthly rentals
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=monthly_rentals_df, x="mnth", y="cnt", hue="yr", marker="o", ax=ax)
ax.set_xlabel("Bulan", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.legend(title="Tahun")
ax.grid(True)
st.pyplot(fig)

# Progress rentals
st.subheader('Progress Bisnis (Seluruh Tahun)')
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=seasonal_rentals_df, x="season", y="cnt", hue="yr", palette=["blue", "red"], ax=ax)

# Customisasi tampilan
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Total Penyewaan Sepeda per Musim (2011 vs 2012)")
ax.legend(title="Tahun")
ax.grid(axis="y")

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=yearly_rentals_df, x="mnth", y="cnt", hue="yr", marker="o", ax=ax)

# Customisasi tampilan
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda per Bulan (2011-2012)")
ax.legend(title="Tahun")
ax.grid(True)

st.pyplot(fig)

# Hourly rentals
st.subheader('Hourly Rentals (Seluruh Tahun)')

# Lineplot untuk tren penyewaan berdasarkan jam
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=hourly_rentals_df, x="hr", y="cnt", marker="o", color="blue", ax=ax)
ax.set_xlabel("Jam dalam Sehari", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
ax.grid(True)
st.pyplot(fig)

st.caption('Copyright © Dicoding 2025')