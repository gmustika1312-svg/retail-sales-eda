import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://drive.google.com/uc?export=download&id=1QCJfqvNRfG2KsAgCG0pqdixvozvrsD9R"
data_ecommerce = pd.read_csv(url)

## DATA CHECKING AND CLEANING
# Melihat 5 data teratas
data_ecommerce.head(5)
# Melihat sample data
data_ecommerce.sample(5, random_state=42)
data_ecommerce.info()
data_ecommerce.describe()
# Data overview
print("Shape               :", data_ecommerce.shape)
print("Jumlah Baris        :", data_ecommerce.shape[0])
print("Jumlah Kolom        :", data_ecommerce.shape[1])
print("Jumlah Missing Value:")
print(data_ecommerce.isnull().sum())
print("Jumlah Duplicated   :", data_ecommerce.duplicated().sum())

## FEATURE ENGINEERING
# Membuat salinan dataset
df = data_ecommerce.copy()
# Ekstraksi komponen Datetime dari InvoiceDate
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['DayName'] = df['InvoiceDate'].dt.day_name()
df['Hour'] = df['InvoiceDate'].dt.hour
# Membuat kolom Total Sales (Revenue)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

## OUTLIER ANALYSIS
# Mengecek distribusi
kolom_ecommerce = ['Quantity', 'UnitPrice', 'TotalPrice']
for kolom in kolom_ecommerce:
    plt.figure(figsize=(12,5))
    # Histogram
    plt.subplot(1,2,1)
    sns.histplot(df[kolom], kde=True)
    plt.title(f'Distribusi Data {kolom}')
    # Boxplot
    plt.subplot(1,2,2)
    sns.boxplot(x=df[kolom])
    plt.title(f'Boxplot {kolom}')
    plt.show()
# Pengecekan outlier
kolom_ecommerce = ['Quantity', 'UnitPrice', 'TotalPrice']
for kolom in kolom_ecommerce:
  Q1 = df[kolom].quantile(0.25)
  Q3 = df[kolom].quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR
  outlier_df = df[
      (df[kolom] < lower_bound) |
      (df[kolom] > upper_bound)
  ]
  print(f"{kolom}")
  print(f"Jumlah Outlier : {len(outlier_df)}")

## TRANSACTION SEGMENTATION
# Segmentasi Transaksi berdasarkan quartil
df['SegmentTransaction'] = pd.cut(
    df['TotalPrice'],
    bins=[
    df['TotalPrice'].min(),
    Q1,
    Q3,
    upper_bound,
    df['TotalPrice'].max()
    ],
    labels=['Low', 'Medium', 'High', 'Premium'],
    include_lowest=True
)

## PATTERN EXPLORATION
# Q1: Segmen transaksi mana yang memberikan kontribusi terbesar terhadap revenue (TotalPrice)?
# Total revenue per segment
segment_revenue = (
    df.groupby('SegmentTransaction')['TotalPrice']
      .sum()
      .reset_index()
      .sort_values(by='TotalPrice', ascending=False)
)
# Menghitung persentase kontribusi
segment_revenue['Contribution (%)'] = (
    segment_revenue['TotalPrice'] /
    segment_revenue['TotalPrice'].sum() * 100
)
segment_revenue
# Visualisasi
plt.figure(figsize=(8,5))
# Bar Chart
ax = sns.barplot(
    data=segment_revenue,
    x='SegmentTransaction',
    y='TotalPrice',
    hue='SegmentTransaction',
    palette='Set2',
    legend=False
)
plt.title('Kontribusi Revenue per Segmen Transaksi')
plt.xlabel('Segmen Transaksi')
plt.ylabel('Total Revenue')
plt.tight_layout()
plt.show()

# Q2: Produk apa yang paling berkontribusi terhadap revenue pada segmen tersebut?
# Filter segmen Premium
premium_df = df[df['SegmentTransaction'] == 'Premium']
# Revenue per product pada segmen Premium
product_revenue = (
    premium_df.groupby('Description')['TotalPrice']
              .sum()
              .reset_index()
              .sort_values(by='TotalPrice', ascending=False)
)
# Hitung kontribusi (%)
product_revenue['Contribution (%)'] = (
    product_revenue['TotalPrice'] /
    product_revenue['TotalPrice'].sum() * 100
)
product_revenue.head(10)
# Visualisasi
top10_product = product_revenue.head(10)
plt.figure(figsize=(10,6))
# Bar Chart
sns.barplot(
    data=top10_product,
    x='TotalPrice',
    y='Description',
    hue='Description',
    palette='Set2',
    legend=False
)
plt.title('Top 10 Produk Berdasarkan Revenue pada Segmen Premium')
plt.xlabel('Revenue')
plt.ylabel('Produk')
plt.tight_layout()
plt.show()

# Q3: Revenue yang tinggi pada segmen premium lebih dipengaruhi oleh banyaknya transaksi atau tingginya nilai transaksi?
# Agregasi nilai transaksi per invoice
invoice_summary = (
    df.groupby('InvoiceNo')
      .agg(
          SegmentTransaction=('SegmentTransaction', 'first'),
          TransactionValue=('TotalPrice', 'sum')
      )
      .reset_index()
)
invoice_summary.head()
# Mengelompokkan data berdasarkan segmen transaksi
segment_summary = (
    invoice_summary.groupby('SegmentTransaction')
    .agg(
        Total_Transaction=('InvoiceNo', 'count'),
        Median_Transaction_Value=('TransactionValue', 'median'),
        Average_Transaction_Value=('TransactionValue', 'mean'),
        Total_Revenue=('TransactionValue', 'sum')
    )
    .reset_index()
    .sort_values(by='Total_Revenue', ascending=False)
)
segment_summary
# Visualisasi
fig, ax = plt.subplots(1, 2, figsize=(10,5))

# Plot 1: Jumlah transaksi
sns.barplot(
    data=segment_summary,
    x='SegmentTransaction',
    y='Total_Transaction',
    hue='SegmentTransaction',
    palette='Set2',
    legend=False,
    ax=ax[0]
)

ax[0].set_title('Jumlah Transaksi per Segmen')
ax[0].set_xlabel('Segmen Transaksi')
ax[0].set_ylabel('Jumlah Transaksi')
# Plot 2: Median nilai transaksi
sns.barplot(
    data=segment_summary,
    x='SegmentTransaction',
    y='Median_Transaction_Value',
    hue='SegmentTransaction',
    palette='Set3',
    legend=False,
    ax=ax[1]
)
ax[1].set_title('Median Nilai Transaksi per Segmen')
ax[1].set_xlabel('Segmen Transaksi')
ax[1].set_ylabel('Median Nilai Transaksi')
plt.suptitle(
    'Perbandingan Jumlah Transaksi dan Nilai Transaksi Antar Segmen',
    fontsize=14
)
plt.tight_layout()
plt.show()

# Q4: Negara mana yang memberikan kontribusi revenue terbesar pada segmen Premium?
# Filter segmen Premium
premium_df = df[df['SegmentTransaction'] == 'Premium']
# Revenue per country
country_revenue = (
    premium_df.groupby('Country')['TotalPrice']
    .sum()
    .reset_index()
    .sort_values(by='TotalPrice', ascending=False)
)
# Persentase kontribusi
country_revenue['Contribution (%)'] = (
    country_revenue['TotalPrice'] /
    country_revenue['TotalPrice'].sum() * 100
).round(2)
country_revenue.head(10)
# Visualisasi
top10_country = country_revenue.head(10)
plt.figure(figsize=(10,6))
# Bar Chart
sns.barplot(
    data=top10_country,
    x='Contribution (%)',
    y='Country',
    hue='Country',
    palette='Set2',
    legend=False
)
plt.title('Kontribusi Revenue Segmen Premium Berdasarkan Negara')
plt.xlabel('Contribution (%)')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

# Q5: Bagaimana tren revenue pada segmen Premium sepanjang tahun 2011?
# Filter segmen Premium dan tahun 2011
premium_2011 = df[
    (df['SegmentTransaction'] == 'Premium') &
    (df['Year'] == 2011)
]
# Revenue bulanan tahun 2011
monthly_revenue = (
    premium_2011.groupby('Month')['TotalPrice']
    .sum()
    .reset_index()
    .sort_values('Month')
)
monthly_revenue
# Visualisasi
plt.figure(figsize=(10,5))
# Line Chart
sns.lineplot(
    data=monthly_revenue,
    x='Month',
    y='TotalPrice',
    marker='o'
)
plt.title('Tren Revenue Bulanan Segmen Premium Tahun 2011')
plt.xlabel('Bulan')
plt.ylabel('Revenue')
plt.xticks(range(1,13))
plt.tight_layout()
plt.show()
