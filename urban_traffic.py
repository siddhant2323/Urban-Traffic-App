# -*- coding: utf-8 -*-
"""Urban traffic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vOaoysdO29XEwqLMl1qDOJ2boXjPGjC5
"""

from google.colab import drive
drive.mount('/content/drive')

collision_path = '/content/drive/MyDrive/UrbanTraffic/collision-2023.csv'
vehicle_path = '/content/drive/MyDrive/UrbanTraffic/vehicle-2023.csv'
casualty_path = '/content/drive/MyDrive/UrbanTraffic/casualty-2023.csv'
code_list_path = '/content/drive/MyDrive/UrbanTraffic/code list-2023.xlsx'

import pandas as pd

# Load main files
print("Loading Collision Data...")
collision_df = pd.read_csv(collision_path)
print("Collision shape:", collision_df.shape)

print("\nLoading Vehicle Data...")
vehicle_df = pd.read_csv(vehicle_path)
print("Vehicle shape:", vehicle_df.shape)

print("\nLoading Casualty Data...")
casualty_df = pd.read_csv(casualty_path)
print("Casualty shape:", casualty_df.shape)

# Load Code List
print("\nLoading Code List...")
code_list = pd.read_excel(code_list_path, sheet_name=None)  # Load all sheets
print("Code list sheets:", code_list.keys())

print("Collision Columns:", collision_df.columns.tolist())
print("Vehicle Columns:", vehicle_df.columns.tolist())
print("Casualty Columns:", casualty_df.columns.tolist())

# Merge Vehicle & Casualty onto Collision Data
# Merge Vehicle data
merged_df = collision_df.merge(vehicle_df, on='accident_index', how='left')

# Merge Casualty data
merged_df = merged_df.merge(casualty_df, on='accident_index', how='left')


print("\nMerged Data Shape:", merged_df.shape)
print(merged_df.head())

# Save merged dataset
merged_df.to_csv('/content/drive/MyDrive/UrbanTraffic/merged_accident_data_2023.csv', index=False)

print("✅ Merged dataset saved to: /content/drive/MyDrive/UrbanTraffic/merged_accident_data_2023.csv")

# Load ALL sheets from code list
code_lists = pd.read_excel('/content/drive/MyDrive/UrbanTraffic/code list-2023.xlsx', sheet_name=None)

# See available sheets (each sheet = code category)
print(code_lists.keys())

code_df = code_lists['2024_code_list']
print(code_df.head())
print(code_df.columns.tolist())

# Load code list sheet
code_df = code_lists['2024_code_list']
print(code_df.columns.tolist())

# Step 1: Load code list (already done)
code_df = code_lists['2024_code_list']

# Step 2: Clean column names (strip spaces)
code_df.columns = code_df.columns.str.strip()

# --------------------------
# Function to decode any field
def decode_column(merged_df, code_df, field_name, new_label_name):
    # Filter relevant codes
    code_map = code_df[code_df['field name'] == field_name][['code/format', 'label']].dropna()

    # Create mapping dictionary
    mapping = dict(zip(code_map['code/format'], code_map['label']))

    # Apply mapping
    merged_df[new_label_name] = merged_df[field_name].map(mapping)

    print(f"Decoded {field_name} → {new_label_name}")
    return merged_df

# Decode vehicle type
merged_df = decode_column(merged_df, code_df, 'vehicle_type', 'vehicle_type_label')

# Decode weather conditions
merged_df = decode_column(merged_df, code_df, 'weather_conditions', 'weather_label')

# Decode road type
merged_df = decode_column(merged_df, code_df, 'road_type', 'road_type_label')

# Decode light conditions
merged_df = decode_column(merged_df, code_df, 'light_conditions', 'light_conditions_label')

# Decode accident severity
merged_df = decode_column(merged_df, code_df, 'accident_severity', 'accident_severity_label')

merged_df.to_csv('/content/drive/MyDrive/UrbanTraffic/merged_cleaned_decoded_2023.csv', index=False)
print("✅ Saved merged & decoded file!")

print(merged_df.columns.tolist())

"""# ***EDA***"""

# Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Plot styling
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 6)

# Load merged, cleaned, decoded data
data_path = '/content/drive/MyDrive/UrbanTraffic/merged_cleaned_decoded_2023.csv'
df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)
df.head()

# Check for missing/null values
print(df.isnull().sum())

df_vehicle = df.dropna(subset=['vehicle_type_label'])
print("Shape after dropping missing vehicle type:", df_vehicle.shape)

df_geo = df.dropna(subset=['longitude', 'latitude'])

plt.figure()
sns.countplot(data=df, x='accident_severity_label', order=df['accident_severity_label'].value_counts().index)
plt.title("Accident Severity Distribution")
plt.xlabel("Severity")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.countplot(data=df, x='road_type_label', order=df['road_type_label'].value_counts().index)
plt.title("Accidents by Road Type")
plt.xlabel("Road Type")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.countplot(data=df, x='weather_label', order=df['weather_label'].value_counts().index)
plt.title("Accidents by Weather Conditions")
plt.xlabel("Weather Condition")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.countplot(data=df, x='light_conditions_label', order=df['light_conditions_label'].value_counts().index)
plt.title("Accidents by Light Conditions")
plt.xlabel("Light Conditions")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.countplot(data=df, x='vehicle_type_label', order=df['vehicle_type_label'].value_counts().index)
plt.title("Vehicle Types Involved")
plt.xlabel("Vehicle Type")
plt.ylabel("Number of Vehicles")
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.countplot(data=df, x='day_of_week', order=df['day_of_week'].value_counts().index)
plt.title("Accidents by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.show()

# Clean Time Column
df['time_cleaned'] = pd.to_datetime(df['time'], errors='coerce').dt.hour

plt.figure()
sns.histplot(df['time_cleaned'], bins=24, kde=False)
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Accidents")
plt.show()

import folium
from folium.plugins import HeatMap

# Drop rows with missing location data
df_geo = df.dropna(subset=['longitude', 'latitude'])

# Create base map
m = folium.Map(location=[51.5, -0.1], zoom_start=6)  # UK Center

# Prepare data
heat_data = list(zip(df_geo['latitude'], df_geo['longitude']))

# Add heatmap
HeatMap(heat_data, radius=6).add_to(m)

# Display
m

import pandas as pd
!pip install plotly
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Plot settings
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 6)

fig = px.pie(df, names='accident_severity_label', title='Accident Severity Distribution (Interactive)', hole=0.4)
fig.show()

pivot = df.pivot_table(index='road_type_label', columns='weather_label', values='accident_index', aggfunc='count')

plt.figure(figsize=(16, 8))
sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt='g')
plt.title('Accident Count Heatmap: Road Type vs Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Road Type')
plt.xticks(rotation=45)
plt.show()

import numpy as np

# Create synthetic counties (you can customize this list!)
county_names = ['Greater London', 'West Midlands', 'Greater Manchester', 'West Yorkshire',
                'Kent', 'Essex', 'Merseyside', 'South Yorkshire', 'Hampshire', 'Lancashire']

# Assign random county for demonstration
merged_df['county'] = np.random.choice(county_names, len(merged_df))

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
merged_df['county_encoded'] = le.fit_transform(merged_df['county'])

# Categorical columns to encode
cat_cols = [
    'road_type_label',
    'weather_label',
    'light_conditions_label',
    'vehicle_type_label',
    'day_of_week'
]

for col in cat_cols:
    df[col + '_encoded'] = le.fit_transform(df[col].astype(str))  # Convert to string (for NaNs/Unknown)
    print(f"Encoded {col}")

df['accident_severity_label_encoded'] = le.fit_transform(df['accident_severity_label'])

"""# ***Model***"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

label_cols = ['road_type_label', 'weather_label', 'light_conditions_label', 'vehicle_type_label']

for col in label_cols:
    le = LabelEncoder()
    merged_df[col + '_encoded'] = le.fit_transform(merged_df[col])

merged_df['time_cleaned'] = merged_df['time'].str[:2].fillna('00').astype(int)

from sklearn.cluster import KMeans
import numpy as np

# Filter valid lat/lon
df_geo = df.dropna(subset=['latitude', 'longitude'])

# Apply KMeans Clustering
kmeans = KMeans(n_clusters=10, random_state=42)
df_geo['location_cluster'] = kmeans.fit_predict(df_geo[['latitude', 'longitude']])

# Merge cluster back to main df (if needed)
df = df.merge(df_geo[['accident_index', 'location_cluster']], how='left', on='accident_index')

# Fill missing cluster IDs (for rows with NaNs)
df['location_cluster'] = df['location_cluster'].fillna(-1)

print(merged_df.columns.tolist())

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- Load data ---
merged_df = pd.read_csv('/content/drive/MyDrive/UrbanTraffic/merged_cleaned_decoded_2023.csv')

# --- Encode categorical columns ---
label_cols = ['road_type_label', 'weather_label', 'light_conditions_label', 'vehicle_type_label', 'day_of_week']

for col in label_cols:
    le = LabelEncoder()
    merged_df[col + '_encoded'] = le.fit_transform(merged_df[col])

# --- Clean 'time' column ---
merged_df['time_cleaned'] = merged_df['time'].str[:2].fillna('00').astype(int)

# --- Create Location Cluster ---
geo_df = merged_df.dropna(subset=['latitude', 'longitude'])

# Perform KMeans clustering
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=9, random_state=42)
clusters = kmeans.fit_predict(geo_df[['latitude', 'longitude']])

# Assign back to original DataFrame safely
merged_df.loc[geo_df.index, 'location_cluster'] = clusters
merged_df['location_cluster'] = merged_df['location_cluster'].fillna(-1).astype(int)

from imblearn.combine import SMOTEENN
from sklearn.model_selection import train_test_split

# Define feature columns (including location_cluster now!)
feature_cols = [
    'road_type_label_encoded',
    'weather_label_encoded',
    'light_conditions_label_encoded',
    'vehicle_type_label_encoded',
    'day_of_week_encoded',
    'time_cleaned',
    'location_cluster'
]

target_col = 'accident_severity_label'

X = merged_df[feature_cols]
y = merged_df[target_col]

# Apply SMOTE-ENN
sme = SMOTEENN(random_state=42)
X_resampled, y_resampled = sme.fit_resample(X, y)

print("Class distribution after SMOTE-ENN:\n", y_resampled.value_counts())

# Split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42, stratify=y_resampled)

from lightgbm import LGBMClassifier
from sklearn.model_selection import RandomizedSearchCV

# LightGBM Model
lgb = LGBMClassifier(random_state=42, class_weight='balanced')

# Param Grid (simplified for speed)
param_dist = {
    'n_estimators': [350],
    'max_depth': [-1],
    'learning_rate': [0.4]
}

random_search = RandomizedSearchCV(
    estimator=lgb,
    param_distributions=param_dist,
    n_iter=10,
    cv=3,
    verbose=2,
    n_jobs=-1
)

# Fit
random_search.fit(X_train, y_train)

print("Best Params:", random_search.best_params_)
print("Best CV Score:", random_search.best_score_)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

y_pred = random_search.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='g', cmap='YlGnBu')
plt.title("Confusion Matrix - LightGBM")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

import joblib
joblib.dump(random_search.best_estimator_, '/content/drive/MyDrive/UrbanTraffic/final_lightgbm_model.pkl')
print("✅ Final LightGBM model saved!")

# After applying KMeans and assigning clusters:
merged_df.to_csv('/content/drive/MyDrive/UrbanTraffic/merged_cleaned_decoded_2023.csv', index=False)