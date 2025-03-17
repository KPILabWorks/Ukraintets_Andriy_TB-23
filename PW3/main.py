# Практична робота 3
# Реалізуйте ефективний механізм кешування проміжних результатів обробки даних енергетичних споживань у файли Parquet. Порівняйте ефективність кешування за допомогою Parquet з іншими форматами.

import pandas as pd
import numpy as np
import time
import os


np.random.seed(int(time.time()))
num_records = 10_000_000


locations = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "San Francisco", "Denver", "Boston"]
num_devices = 1000  # amount of unique devices

data = pd.DataFrame({
    "timestamp": pd.date_range(start=pd.Timestamp(time.mktime(time.localtime())), periods=num_records, freq="min"),
    "energy_consumption": np.random.rand(num_records) * 100,
    "temperature": np.random.uniform(-10, 35, num_records),
    "humidity": np.random.uniform(20, 90, num_records),
    "device_id": np.random.randint(1, num_devices + 1, num_records),
    "location": np.random.choice(locations, num_records)
})


cache_dir = "./cache"
os.makedirs(cache_dir, exist_ok=True)


def measure_time(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    return result, time.time() - start


parquet_path = os.path.join(cache_dir, "energy_data.parquet")
csv_path = os.path.join(cache_dir, "energy_data.csv")
pickle_path = os.path.join(cache_dir, "energy_data.pkl")


_, parquet_write_time = measure_time(data.to_parquet, parquet_path, engine="pyarrow")
_, csv_write_time = measure_time(data.to_csv, csv_path, index=False)
_, pickle_write_time = measure_time(data.to_pickle, pickle_path)


_, parquet_read_time = measure_time(pd.read_parquet, parquet_path)
_, csv_read_time = measure_time(pd.read_csv, csv_path)
_, pickle_read_time = measure_time(pd.read_pickle, pickle_path)


parquet_size = os.path.getsize(parquet_path) / (1024 * 1024)  # in MegaBytes
csv_size = os.path.getsize(csv_path) / (1024 * 1024)
pickle_size = os.path.getsize(pickle_path) / (1024 * 1024)


{
    "write_time": {
        "parquet": parquet_write_time,
        "csv": csv_write_time,
        "pickle": pickle_write_time
    },
    "read_time": {
        "parquet": parquet_read_time,
        "csv": csv_read_time,
        "pickle": pickle_read_time
    },
    "file_size_MB": {
        "parquet": parquet_size,
        "csv": csv_size,
        "pickle": pickle_size
    }
}
