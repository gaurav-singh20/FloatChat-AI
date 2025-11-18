import os, datetime as dt, requests, pandas as pd
from dotenv import load_dotenv
from db.models import Base, ArgoRecord
from db.session import engine, SessionLocal

load_dotenv()

# One known float operating in Indian Ocean
FLOAT_ID = os.getenv("FLOAT_ID", "2902746")  # you can change this later

def fetch_profiles():
    print(f"🔄 Fetching Argo data for float {FLOAT_ID} (Indian Ocean)...")

    base_url = "https://argovis2.colorado.edu/api/v2"
    headers = {'Accept': 'application/json'}
    
    # Get platform data
    platform_url = f"{base_url}/platforms/ARGO/{FLOAT_ID}"
    r = requests.get(platform_url, headers=headers, timeout=60)
    print(f"🔗 URL: {r.url}")

    if r.status_code != 200:
        print(f"❌ Failed to fetch: {r.status_code} - {r.text}")
        return pd.DataFrame()

    data = r.json()
    if not data or not isinstance(data, list) or len(data) == 0:
        print("⚠️ No profiles found.")
        return pd.DataFrame()

    print(f"✅ Received {len(data)} profiles for float {FLOAT_ID}.")

    rows = []
    for profile in data:
        lat = profile.get("lat")
        lon = profile.get("lon")
        date = profile.get("date")
        plat = FLOAT_ID

        measurements = profile.get("measurements", [])
        for m in measurements:
            rows.append({
                "time": pd.to_datetime(date, utc=True),
                "latitude": lat,
                "longitude": lon,
                "depth": m.get("pres"),
                "temperature": m.get("temp"),
                "salinity": m.get("psal"),
                "platform": plat
            })

    df = pd.DataFrame(rows)
    print(f"📊 Flattened {len(df)} measurement rows.")
    return df

def ingest(df):
    if df.empty:
        print("⚠️ Nothing to ingest.")
        return
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as s:
        for _, r in df.iterrows():
            s.add(ArgoRecord(
                time=r["time"].to_pydatetime(),
                latitude=r["latitude"],
                longitude=r["longitude"],
                depth=r["depth"],
                temperature=r["temperature"],
                salinity=r["salinity"],
                platform=r["platform"]
            ))
        s.commit()
    print(f"✅ Inserted {len(df)} rows into DB.")

if __name__ == "__main__":
    df = fetch_profiles()
    if not df.empty:
        print(df.head(3))
        ingest(df)
        os.makedirs("data", exist_ok=True)
        df.to_csv(f"data/argo_float_{FLOAT_ID}.csv", index=False)
        print(f"💾 Saved CSV: data/argo_float_{FLOAT_ID}.csv")
    else:
        print("❌ No data returned for this float.")
