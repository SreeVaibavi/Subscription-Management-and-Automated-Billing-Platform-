from app.database.connection import SessionLocal
import app.models.core as models

def seed_cloud_plans():
    db = SessionLocal()
    try:
        cloud_plans = [
            {
                "name": "Free Tier",
                "price": 0.0,
                "billing_interval": "monthly",
                "trial_period_days": 0,
                "feature_entitlements": [
                    "1 vCPU Max Allocation",
                    "10GB NVMe Storage",
                    "100GB Monthly Bandwidth",
                    "Community Support"
                ]
            },
            {
                "name": "Starter Tier",
                "price": 29.0,
                "billing_interval": "monthly",
                "trial_period_days": 7,
                "feature_entitlements": [
                    "2 vCPUs Max Allocation",
                    "50GB NVMe Storage",
                    "500GB Monthly Bandwidth",
                    "Basic Deployment Pipeline"
                ]
            },
            {
                "name": "Pro Tier",
                "price": 79.0,
                "billing_interval": "monthly",
                "trial_period_days": 0,
                "feature_entitlements": [
                    "4 vCPUs Max Allocation",
                    "100GB NVMe Storage",
                    "2TB Monthly Bandwidth",
                    "Automated Nightly Backups"
                ]
            },
            {
                "name": "Business Tier",
                "price": 199.0,
                "billing_interval": "monthly",
                "trial_period_days": 0,
                "feature_entitlements": [
                    "10 vCPUs Max Allocation",
                    "500GB NVMe Storage",
                    "10TB Monthly Bandwidth",
                    "Automated Nightly Backups",
                    "Load Balancer & High Availability"
                ]
            },
            {
                "name": "Enterprise Tier",
                "price": 499.0,
                "billing_interval": "monthly",
                "trial_period_days": 0,
                "feature_entitlements": [
                    "Unlimited vCPUs Allocation",
                    "Unlimited NVMe Storage",
                    "Unlimited Monthly Bandwidth",
                    "Automated Nightly Backups",
                    "Load Balancer & High Availability",
                    "Isolated Custom VPC & Dedicated Gateway"
                ]
            }
        ]

        for plan_data in cloud_plans:
            existing = db.query(models.Plan).filter(models.Plan.name == plan_data["name"]).first()
            if existing:
                existing.price = plan_data["price"]
                existing.feature_entitlements = plan_data["feature_entitlements"]
                print(f"Updated plan: {existing.name}")
            else:
                new_plan = models.Plan(**plan_data)
                db.add(new_plan)
                print(f"Created plan: {new_plan.name}")
        
        db.commit()
        print("SUCCESS: 5 Cloud Tiers seeded into database!")
    except Exception as e:
        print(f"Error seeding plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_cloud_plans()
