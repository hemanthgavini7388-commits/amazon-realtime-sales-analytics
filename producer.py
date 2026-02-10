import time
import pandas as pd
import queue
import threading

def producer(csv_path: str, q: queue.Queue, rate_per_sec: int = 20):
    df = pd.read_csv(csv_path)

    if "data_collected_at" in df.columns:
        df["data_collected_at"] = pd.to_datetime(df["data_collected_at"], errors="coerce")
    if "delivery_date" in df.columns:
        df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")

    delay = 1.0 / rate_per_sec
    produced = 0

    for _, row in df.iterrows():
        q.put(row.to_dict())
        produced += 1
        if produced % 500 == 0:
            print(f"[PRODUCER] Produced {produced} events")
        time.sleep(delay)

    q.put(None)
    print("[PRODUCER] Done.")

def start_producer(csv_path, q, rate_per_sec):
    t = threading.Thread(target=producer, args=(csv_path, q, rate_per_sec), daemon=True)
    t.start()
    return t
