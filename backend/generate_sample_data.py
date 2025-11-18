"""
Sample Data Generator for Testing
Creates realistic ARGO float data when Argovis API is not accessible
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db.models import Base, ArgoRecord
from db.session import engine, SessionLocal

load_dotenv()

def generate_sample_data():
    """Generate realistic ARGO float data for Indian Ocean"""
    print("🔄 Generating sample ARGO data for testing...")
    
    # Parameters for Indian Ocean
    base_lat = -10.0  # Indian Ocean latitude
    base_lon = 75.0   # Indian Ocean longitude
    float_id = os.getenv("FLOAT_ID", "2902746")
    
    # Number of profiles (simulating ~30 days, every 10 days = 3 profiles)
    num_profiles = 3
    measurements_per_profile = 50  # Depth levels
    
    rows = []
    
    # Generate profiles over time
    base_date = datetime.now() - timedelta(days=30)
    
    for profile_idx in range(num_profiles):
        # Each profile is ~10 days apart
        profile_date = base_date + timedelta(days=profile_idx * 10)
        
        # Float drifts slightly
        lat = base_lat + np.random.uniform(-0.5, 0.5)
        lon = base_lon + np.random.uniform(-0.5, 0.5)
        
        # Generate depth profile (0 to ~2000 dbar)
        depths = np.linspace(5, 2000, measurements_per_profile)
        
        for depth in depths:
            # Temperature decreases with depth (realistic ocean profile)
            # Surface: ~28°C, Deep: ~2°C
            if depth < 100:
                temp = 28 - (depth / 100) * 3  # Warm mixed layer
            elif depth < 500:
                temp = 25 - (depth - 100) / 400 * 15  # Thermocline
            else:
                temp = 10 - (depth - 500) / 1500 * 8  # Deep water
            
            # Add some random variation
            temp += np.random.normal(0, 0.5)
            
            # Salinity is more stable (34-35 PSU typical)
            if depth < 50:
                sal = 34.5 + np.random.normal(0, 0.2)
            else:
                sal = 34.8 + np.random.normal(0, 0.15)
            
            rows.append({
                "time": profile_date,
                "latitude": lat,
                "longitude": lon,
                "depth": depth,
                "temperature": round(temp, 2),
                "salinity": round(sal, 2),
                "platform": float_id
            })
    
    df = pd.DataFrame(rows)
    print(f"✅ Generated {len(df)} synthetic measurements")
    return df

def ingest_data(df):
    """Ingest data into database"""
    if df.empty:
        print("⚠️ No data to ingest")
        return
    
    print("📥 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("📥 Inserting data into database...")
    with SessionLocal() as session:
        for _, row in df.iterrows():
            session.add(ArgoRecord(
                time=row["time"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                depth=row["depth"],
                temperature=row["temperature"],
                salinity=row["salinity"],
                platform=row["platform"]
            ))
        session.commit()
    
    print(f"✅ Inserted {len(df)} rows into database")

if __name__ == "__main__":
    # Generate and ingest sample data
    df = generate_sample_data()
    
    if not df.empty:
        print("\n📊 Sample data preview:")
        print(df.head(10))
        print(f"\n📈 Statistics:")
        print(f"   Temperature range: {df['temperature'].min():.2f} to {df['temperature'].max():.2f} °C")
        print(f"   Salinity range: {df['salinity'].min():.2f} to {df['salinity'].max():.2f} PSU")
        print(f"   Depth range: {df['depth'].min():.2f} to {df['depth'].max():.2f} dbar")
        
        # Ingest into database
        ingest_data(df)
        
        # Save CSV backup
        os.makedirs("data", exist_ok=True)
        csv_path = f"data/sample_argo_{df['platform'].iloc[0]}.csv"
        df.to_csv(csv_path, index=False)
        print(f"💾 Saved CSV backup: {csv_path}")
        
        print("\n✅ Sample data setup complete!")
        print("🌊 You can now start the Flask server with: python app.py")
    else:
        print("❌ Failed to generate data")
