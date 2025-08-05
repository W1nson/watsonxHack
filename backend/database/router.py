from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

db_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new user
# Input: User Schema (schemas.py)
# Output: User (schemas.py)
@db_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, firstName=user.firstName, lastName=user.lastName, phoneNumber=user.phoneNumber)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get all users
# Input: None
# Output: List of Users (schemas.py)
@db_router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


# Get a user by ID
# Input: User ID (using path parameter)
# Output: User (schemas.py)
@db_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update a user by ID
# Input: User ID (using path parameter), User Schema (schemas.py)
# Output: User (schemas.py)
@db_router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.firstName = user.firstName
    db_user.lastName = user.lastName
    db_user.phoneNumber = user.phoneNumber
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete a user by ID
# Input: User ID (using path parameter)
# Output: User (schemas.py)
@db_router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


# ------------------ Service Endpoints ------------------
# Create a new service
# Input: Service Schema (schemas.py)
# Output: Service (schemas.py)
@db_router.post("/services/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


# Get all services
# Input: None
# Output: List of Services (schemas.py)
@db_router.get("/services/", response_model=list[schemas.Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

# Get a service by ID
# Input: Service ID (using path parameter)
# Output: Service (schemas.py)
@db_router.get("/services/{service_id}", response_model=schemas.Service)
def read_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

# Update a service by ID
# Input: Service ID (using path parameter), Service Schema (schemas.py)
# Output: Service (schemas.py)
@db_router.put("/services/{service_id}", response_model=schemas.Service)
def update_service(service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    update_data = service.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

# Delete a service by ID
# Input: Service ID (using path parameter)
# Output: Service (schemas.py)
@db_router.delete("/services/{service_id}", response_model=schemas.Service)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return db_service

# ------------------ ServiceTier Endpoints ------------------

# Create a new service tier
# Input: Service Tier Schema (schemas.py)
# Output: Service Tier (schemas.py)
@db_router.post("/service_tiers/", response_model=schemas.ServiceTier)
def create_service_tier(tier: schemas.ServiceTierCreate, db: Session = Depends(get_db)):
    db_tier = models.ServiceTier(**tier.dict())
    db.add(db_tier)
    db.commit()
    db.refresh(db_tier)
    return db_tier

# Get all service tiers
# Input: None
# Output: List of Service Tiers (schemas.py)
@db_router.get("/service_tiers/", response_model=list[schemas.ServiceTier])
def read_service_tiers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tiers = db.query(models.ServiceTier).offset(skip).limit(limit).all()
    return tiers

# Get a service tier by ID
# Input: Service Tier ID (using path parameter)
# Output: Service Tier (schemas.py)
@db_router.get("/service_tiers/{tier_id}", response_model=schemas.ServiceTier)
def read_service_tier(tier_id: int, db: Session = Depends(get_db)):
    db_tier = db.query(models.ServiceTier).filter(models.ServiceTier.id == tier_id).first()
    if db_tier is None:
        raise HTTPException(status_code=404, detail="Service tier not found")
    return db_tier

# Update a service tier by ID
# Input: Service Tier ID (using path parameter), Service Tier Schema (schemas.py)
# Output: Service Tier (schemas.py)
@db_router.put("/service_tiers/{tier_id}", response_model=schemas.ServiceTier)
def update_service_tier(tier_id: int, tier: schemas.ServiceTierCreate, db: Session = Depends(get_db)):
    db_tier = db.query(models.ServiceTier).filter(models.ServiceTier.id == tier_id).first()
    if db_tier is None:
        raise HTTPException(status_code=404, detail="Service tier not found")
    update_data = tier.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tier, key, value)
    db.commit()
    db.refresh(db_tier)
    return db_tier

# Delete a service tier by ID
# Input: Service Tier ID (using path parameter)
# Output: Service Tier (schemas.py)
@db_router.delete("/service_tiers/{tier_id}", response_model=schemas.ServiceTier)
def delete_service_tier(tier_id: int, db: Session = Depends(get_db)):
    db_tier = db.query(models.ServiceTier).filter(models.ServiceTier.id == tier_id).first()
    if db_tier is None:
        raise HTTPException(status_code=404, detail="Service tier not found")
    db.delete(db_tier)
    db.commit()
    return db_tier

# ------------------ Subscription Endpoints ------------------

# Create a new subscription
# Input: Subscription Schema (schemas.py)
# Output: Subscription (schemas.py)
@db_router.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = models.Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# Get all subscriptions
# Input: None
# Output: List of Subscriptions (schemas.py)
@db_router.get("/subscriptions/", response_model=list[schemas.Subscription])
def read_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subscriptions = db.query(models.Subscription).offset(skip).limit(limit).all()
    for subscription in subscriptions:
        subscription.start_date = subscription.start_date.strftime("%Y-%m-%d")
        subscription.last_billed_date = subscription.last_billed_date.strftime("%Y-%m-%d")
        subscription.next_renewal_date = subscription.next_renewal_date.strftime("%Y-%m-%d")
    return subscriptions

# Get a subscription by ID
# Input: Subscription ID (using path parameter)
# Output: Subscription (schemas.py)
@db_router.get("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db_subscription.start_date = db_subscription.start_date.strftime("%Y-%m-%d")
    db_subscription.last_billed_date = db_subscription.last_billed_date.strftime("%Y-%m-%d")
    db_subscription.next_renewal_date = db_subscription.next_renewal_date.strftime("%Y-%m-%d")
    return db_subscription

# Update a subscription by ID
# Input: Subscription ID (using path parameter), Subscription Schema (schemas.py)
# Output: Subscription (schemas.py)
@db_router.put("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def update_subscription(subscription_id: int, subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    update_data = subscription.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subscription, key, value)
    db.commit()
    db.refresh(db_subscription)
    db_subscription.start_date = db_subscription.start_date.strftime("%Y-%m-%d")
    db_subscription.last_billed_date = db_subscription.last_billed_date.strftime("%Y-%m-%d")
    db_subscription.next_renewal_date = db_subscription.next_renewal_date.strftime("%Y-%m-%d")
    return db_subscription

# Delete a subscription by ID
# Input: Subscription ID (using path parameter)
# Output: Subscription (schemas.py)
@db_router.delete("/subscriptions/{subscription_id}", response_model=schemas.Subscription)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db.delete(db_subscription)
    db.commit()
    return db_subscription
