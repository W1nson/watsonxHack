import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine
from models import Base, Service, ServiceTier, User, Subscription
from database import SessionLocal

Base.metadata.create_all(bind=engine)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_csv_to_db():
    db: Session = SessionLocal()

    # Load and insert services
    services_df = pd.read_csv(os.path.join(script_dir, "services.csv"))
    for _, row in services_df.iterrows():
        db.add(Service(id=row["id"], name=row["name"], category=row["category"], website=row["website"]))

    # Load and insert service tiers
    tiers_df = pd.read_csv(os.path.join(script_dir, "service_tiers.csv"))
    for _, row in tiers_df.iterrows():
        db.add(ServiceTier(
            id=row["id"],
            service_id=row["service_id"],
            tier_name=row["tier_name"],
            billing_period=row["billing_period"],
            price_usd=row["price_usd"],
            max_seats=row["max_seats"],
            ads_free=row["ads_free"],
            trial_days=row["trial_days"]
        ))

    # Load and insert users
    users_df = pd.read_csv(os.path.join(script_dir, "users.csv"))
    for _, row in users_df.iterrows():
        db.add(User(id=row["id"], email=row["email"], firstName=row["firstName"], lastName=row["lastName"], phoneNumber=row["phoneNumber"]))

    # Load and insert user subscriptions
    subs_df = pd.read_csv(os.path.join(script_dir, "subscriptions.csv"))
    
    # Function to convert date string to date object
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return None
        return datetime.strptime(str(date_str), '%Y-%m-%d').date()
    
    for _, row in subs_df.iterrows():
        db.add(Subscription(
            id=row["id"],
            user_id=row["user_id"],
            tier_id=row["tier_id"],
            start_date=parse_date(row["start_date"]),
            renewal_frequency=row["renewal_frequency"],
            auto_renew=bool(row["auto_renew"]),
            current_status=row["current_status"],
            last_billed_date=parse_date(row["last_billed_date"]),
            next_renewal_date=parse_date(row["next_renewal_date"]),
            amount_billed=float(row["amount_billed"]),
            currency=row["currency"]
        ))

    db.commit()
    db.close()

if __name__ == "__main__":
    load_csv_to_db()