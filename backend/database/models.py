from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True) # Service ID
    name = Column(String, unique=True, nullable=False) # Service Name
    category = Column(String) # Service Type
    website = Column(String) # Link to the website

    tiers = relationship("ServiceTier", back_populates="service")


class ServiceTier(Base):
    __tablename__ = "service_tiers"

    id = Column(Integer, primary_key=True, index=True) # Tier ID
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False) # Service ID
    tier_name = Column(String) # Tier Name
    billing_period = Column(String)  # monthly / yearly
    price_usd = Column(Float) # Price in USD
    max_seats = Column(Integer) # Maximum number of seats ?
    ads_free = Column(Boolean, default=True) # Whether the tier is ad free
    trial_days = Column(Integer) # Number of days for the trial

    service = relationship("Service", back_populates="tiers")
    subscriptions = relationship("Subscription", back_populates="tier")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # User ID
    email = Column(String, unique=True, nullable=False) # User Email
    firstName = Column(String) # User First Name
    lastName = Column(String) # User Last Name
    phoneNumber = Column(String) # User Phone Number
    
    subscriptions = relationship("Subscription", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True) # Subscription ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # User ID
    tier_id = Column(Integer, ForeignKey("service_tiers.id"), nullable=False) # Tier ID
    start_date = Column(Date) # date when the subscription started
    renewal_frequency = Column(String)  # e.g., monthly, annuelly
    auto_renew = Column(Boolean) # whether the subscription will auto renew
    current_status = Column(String) # active, cancelled, expired
    last_billed_date = Column(Date) # date when the subscription was last billed
    next_renewal_date = Column(Date) # date when the subscription will renew
    amount_billed = Column(Float) # amount billed for the subscription
    currency = Column(String, default="USD") # currency of the subscription

    user = relationship("User", back_populates="subscriptions")
    tier = relationship("ServiceTier", back_populates="subscriptions")