import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

df = pd.read_csv("data/cold_chain_data.csv")
df["EXCURSION"] = ((df["temperature"] < 2) | (df["temperature"] > 8)).astype(int)
df["HOUR"] = pd.to_datetime(df["timestamp"]).dt.hour
df["WEEKDAY"] = pd.to_datetime(df["timestamp"]).dt.weekday
df = pd.get_dummies(df, columns=["location", "container_id"])

X = df.drop(columns=["timestamp", "temperature", "EXCURSION"])
y = df["EXCURSION"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/risk_model.pkl", "wb"))
pickle.dump(X.columns.tolist(), open("model/feature_columns.pkl", "wb"))
print("✅ Model trained and saved.")
