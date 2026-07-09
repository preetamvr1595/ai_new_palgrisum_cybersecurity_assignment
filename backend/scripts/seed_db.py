import uuid
import sys
import os
from datetime import datetime, timezone

# Add backend to path so we can import properly when run as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.session import SessionLocal
from backend.db.models.subscription import Plan
from backend.db.models.user import User

def seed():
    db = SessionLocal()
    try:
        # Seed Plans
        plans = db.query(Plan).all()
        if not plans:
            print("Seeding plans...")
            free_plan = Plan(
                name="Free",
                monthly_price=0.00,
                yearly_price=0.00,
                features_json={"ai_detection": True, "humanizer": False},
                request_limit=100
            )
            pro_plan = Plan(
                name="Pro",
                monthly_price=15.00,
                yearly_price=150.00,
                features_json={"ai_detection": True, "humanizer": True, "grammar": True},
                request_limit=10000
            )
            db.add(free_plan)
            db.add(pro_plan)
            db.commit()
            print("Plans seeded successfully.")
        else:
            print("Plans already exist.")

        # Seed Admin User
        admin_user = db.query(User).filter(User.email == "admin@schoolarshild.com").first()
        if not admin_user:
            print("Seeding admin user...")
            admin = User(
                email="admin@schoolarshild.com",
                username="admin",
                full_name="System Admin",
                password_hash="hashed_password_here", # Should use passlib to hash a real password
                role="admin",
                is_active=True,
                email_verified=True
            )
            db.add(admin)
            db.commit()
            print("Admin user seeded successfully.")
        else:
            print("Admin user already exists.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
