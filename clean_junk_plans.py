from app.database.connection import SessionLocal
import app.models.core as models

def clean_database_plans():
    db = SessionLocal()
    try:
        valid_plan_names = [
            "Free Tier",
            "Starter Tier",
            "Pro Tier",
            "Business Tier",
            "Enterprise Tier"
        ]

        # 1. Fetch valid plans map
        valid_plans = db.query(models.Plan).filter(models.Plan.name.in_(valid_plan_names)).all()
        valid_plan_map = {p.name: p for p in valid_plans}

        # Fallback default plan (Free Tier or Starter Tier)
        default_plan = valid_plan_map.get("Free Tier") or valid_plan_map.get("Starter Tier") or valid_plans[0]

        # 2. Fetch all plans
        all_plans = db.query(models.Plan).all()
        junk_plans = [p for p in all_plans if p.name not in valid_plan_names]

        print(f"Found {len(all_plans)} total plans in database.")
        print(f"Junk/Unnecessary plans to remove: {[p.name for p in junk_plans]}")

        for junk in junk_plans:
            # Reassign any subscriptions referencing this junk plan to a valid default plan
            subs = db.query(models.Subscription).filter(models.Subscription.plan_id == junk.id).all()
            for sub in subs:
                print(f"Reassigning subscription '{sub.id}' from '{junk.name}' to '{default_plan.name}'")
                sub.plan_id = default_plan.id
            
            db.commit()

            # Now delete the junk plan
            db.delete(junk)
            db.commit()
            print(f"Deleted junk plan: {junk.name} ({junk.id})")

        print("SUCCESS: Cleaned database! Only the 5 official Cloud Tiers remain.")

    except Exception as e:
        print(f"Error cleaning plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database_plans()
