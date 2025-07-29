import pandas as pd
import random
from datetime import datetime, timedelta

num_rows = 1000
data = []
start_time = datetime.now()

for i in range(num_rows):
    timestamp = start_time - timedelta(minutes=i*5)
    container_id = f"C{random.randint(1, 5)}"
    temperature = round(random.uniform(0, 12), 2)
    location = random.choice(['Bangalore', 'Chennai', 'Mumbai', 'Hyderabad'])
    data.append([timestamp, container_id, temperature, location])

df = pd.DataFrame(data, columns=['timestamp', 'container_id', 'temperature', 'location'])
df.to_csv("data/cold_chain_data.csv", index=False)
print("Data generated.")
