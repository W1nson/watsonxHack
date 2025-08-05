from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phoneNumber: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Service Schemas
class ServiceBase(BaseModel):
    name: str
    category: Optional[str] = None
    website: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True

# ServiceTier Schemas
class ServiceTierBase(BaseModel):
    service_id: int
    tier_name: str
    billing_period: Optional[str] = None
    price_usd: Optional[float] = None
    max_seats: Optional[int] = None
    ads_free: Optional[bool] = True
    trial_days: Optional[int] = None

class ServiceTierCreate(ServiceTierBase):
    pass

class ServiceTier(ServiceTierBase):
    id: int

    class Config:
        orm_mode = True

# Subscription Schemas
class SubscriptionBase(BaseModel):
    user_id: int
    tier_id: int
    start_date: Optional[str] = None
    renewal_frequency: Optional[str] = None
    auto_renew: Optional[bool] = True
    current_status: Optional[str] = None
    last_billed_date: Optional[str] = None
    next_renewal_date: Optional[str] = None
    amount_billed: Optional[float] = None
    currency: Optional[str] = "USD"

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True

