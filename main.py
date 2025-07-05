# 📦 Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# 📂 Load a sample of the dataset (update path as needed)
file_path = '/Users/shyamsanogar/Documents/SkillCraft/TASK_04/US_Accidents_Dec21_updated.csv'

# 🧹 Load only essential columns and first 100,000 rows
cols = ['Start_Time', 'Severity', 'City', 'State', 'Start_Lat', 'Start_Lng', 'Weather_Condition']
df = pd.read_csv(file_path, usecols=cols, nrows=100000)

# 🕒 Parse datetime & extract hour, month, weekday
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['Hour'] = df['Start_Time'].dt.hour
df['Month'] = df['Start_Time'].dt.month
df['Day'] = df['Start_Time'].dt.day_name()

# ✅ Print basic info
print("Dataset Preview:")
print(df.head())
print("\nData Summary:")
print(df.info())

# ----------------------------------------
# 📊 1. Accidents by Hour of Day
plt.figure(figsize=(10,6))
sns.countplot(x='Hour', data=df, palette='viridis')
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 📊 2. Accidents by Month
plt.figure(figsize=(10,6))
sns.countplot(x='Month', data=df, palette='plasma')
plt.title("Accidents by Month")
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 📊 3. Accidents by Day of Week
plt.figure(figsize=(10,6))
sns.countplot(x='Day', data=df, order=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
], palette='magma')
plt.title("Accidents by Day of Week")
plt.xlabel("Day")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 🌦️ 4. Top 10 Weather Conditions
plt.figure(figsize=(12,6))
top_weather = df['Weather_Condition'].value_counts().head(10)
sns.barplot(x=top_weather.index, y=top_weather.values, palette='cubehelix')
plt.title("Top 10 Weather Conditions During Accidents")
plt.xticks(rotation=45)
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# ----------------------------------------
# 🗺️ 5. Accident Hotspot Heatmap (Sampled)
# Create base map centered around average location
m = folium.Map(location=[df['Start_Lat'].mean(), df['Start_Lng'].mean()], zoom_start=5)

# Sample 5,000 rows to avoid lag
heat_df = df[['Start_Lat', 'Start_Lng']].dropna().sample(5000)
heat_data = list(zip(heat_df['Start_Lat'], heat_df['Start_Lng']))

# Add heatmap to the map
HeatMap(heat_data).add_to(m)

# Save heatmap to an HTML file
m.save("accident_heatmap.html")
print("✅ Heatmap saved as 'accident_heatmap.html' — open it in your browser.")

