"""Seed database with sample data for demo purposes"""

import asyncio
from datetime import datetime, date, timedelta
from uuid import uuid4

from app.config.database import SyncSessionLocal
from app.models import *
from app.utils.auth import get_password_hash


def seed_database():
    """Seed the database with sample data"""
    db = SyncSessionLocal()

    try:
        print("Starting database seeding...")

        # Create admin user
        admin = User(
            email="admin@crowe.uz",
            full_name="Admin User",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash("password123")
        )
        db.add(admin)
        db.commit()
        print("✓ Created admin user (admin@crowe.uz / password123)")

        # Create manager user
        manager = User(
            email="manager@crowe.uz",
            full_name="Manager User",
            role=UserRole.MANAGER,
            hashed_password=get_password_hash("password123")
        )
        db.add(manager)
        db.commit()
        print("✓ Created manager user (manager@crowe.uz / password123)")

        # Create viewer user
        viewer = User(
            email="viewer@crowe.uz",
            full_name="Viewer User",
            role=UserRole.VIEWER,
            hashed_password=get_password_hash("password123")
        )
        db.add(viewer)
        db.commit()
        print("✓ Created viewer user (viewer@crowe.uz / password123)")

        # Sample contacts data
        contacts_data = [
            # VIP Clients
            {"name": "Алексей Иванов", "email": "alexey.ivanov@example.com", "phone": "+998901234567",
             "segment": ContactSegment.VIP, "company": "CROWE Uzbekistan", "position": "CEO",
             "language": Language.RU, "birthday": date(1985, 3, 15)},
            {"name": "Мария Петрова", "email": "maria.petrova@example.com", "phone": "+998901234568",
             "segment": ContactSegment.VIP, "company": "Tech Innovations", "position": "CFO",
             "language": Language.RU, "birthday": date(1988, 7, 22)},
            {"name": "Дмитрий Сидоров", "email": "dmitry.sidorov@example.com", "phone": "+998901234569",
             "segment": ContactSegment.VIP, "company": "Global Finance", "position": "Director",
             "language": Language.RU, "birthday": date(1980, 11, 5)},

            # Regular clients
            {"name": "Anna Smith", "email": "anna.smith@example.com", "phone": "+998907654321",
             "segment": ContactSegment.REGULAR, "company": "Smith Consulting", "position": "Manager",
             "language": Language.EN, "birthday": date(1990, 5, 10)},
            {"name": "John Doe", "email": "john.doe@example.com", "phone": "+998907654322",
             "segment": ContactSegment.REGULAR, "company": "Doe Enterprises", "position": "Owner",
             "language": Language.EN, "birthday": date(1987, 9, 18)},
            {"name": "Олег Смирнов", "email": "oleg.smirnov@example.com", "phone": "+998907654323",
             "segment": ContactSegment.REGULAR, "company": "Смирнов и Партнеры", "position": "Партнер",
             "language": Language.RU, "birthday": date(1992, 2, 28)},

            # New clients
            {"name": "Aziza Karimova", "email": "aziza.karimova@example.com", "phone": "+998901111111",
             "segment": ContactSegment.NEW_CLIENT, "company": "Karimova Group", "position": "CEO",
             "language": Language.UZ, "birthday": date(1995, 6, 12)},
            {"name": "Davron Rahimov", "email": "davron.rahimov@example.com", "phone": "+998901111112",
             "segment": ContactSegment.NEW_CLIENT, "company": "Rahimov Trading", "position": "Director",
             "language": Language.UZ, "birthday": date(1991, 8, 25)},
            {"name": "Екатерина Новикова", "email": "ekaterina.novikova@example.com", "phone": "+998901111113",
             "segment": ContactSegment.NEW_CLIENT, "company": "Новикова Консалтинг", "position": "Консультант",
             "language": Language.RU, "birthday": date(1993, 12, 3)},

            # Partners
            {"name": "Michael Johnson", "email": "michael.johnson@example.com", "phone": "+998902222221",
             "segment": ContactSegment.PARTNER, "company": "Johnson & Associates", "position": "Partner",
             "language": Language.EN, "birthday": date(1982, 4, 7)},
            {"name": "Sarah Williams", "email": "sarah.williams@example.com", "phone": "+998902222222",
             "segment": ContactSegment.PARTNER, "company": "Williams Law Firm", "position": "Senior Partner",
             "language": Language.EN, "birthday": date(1979, 10, 14)},
        ]

        # Create contacts
        contacts = []
        for contact_data in contacts_data:
            contact = Contact(**contact_data, created_by=admin.id, tags=["demo", "seed"])
            db.add(contact)
            contacts.append(contact)

        db.commit()
        print(f"✓ Created {len(contacts)} contacts")

        # Create sample messages
        messages_data = [
            # Pending approval messages
            {
                "contact": contacts[0],
                "occasion_type": OccasionType.BIRTHDAY,
                "content": "Уважаемый Алексей! Поздравляем Вас с Днем рождения! Желаем успехов, здоровья и процветания!",
                "status": MessageStatus.PENDING_APPROVAL,
                "generated_by": GeneratedBy.AI,
                "metadata": {"model": "claude-sonnet-4", "tokens": 150, "cost_usd": 0.0023}
            },
            {
                "contact": contacts[1],
                "occasion_type": OccasionType.BIRTHDAY,
                "content": "Дорогая Мария! С Днем рождения! Пусть этот день принесет радость и вдохновение!",
                "status": MessageStatus.PENDING_APPROVAL,
                "generated_by": GeneratedBy.AI,
                "metadata": {"model": "claude-sonnet-4", "tokens": 145, "cost_usd": 0.0022}
            },

            # Approved messages
            {
                "contact": contacts[3],
                "occasion_type": OccasionType.NEW_YEAR,
                "content": "Dear Anna! Happy New Year! May the coming year bring you success and happiness!",
                "status": MessageStatus.APPROVED,
                "generated_by": GeneratedBy.AI,
                "approved_by": admin.id,
                "approved_at": datetime.utcnow() - timedelta(hours=2),
                "metadata": {"model": "claude-sonnet-4", "tokens": 140, "cost_usd": 0.0021}
            },
            {
                "contact": contacts[4],
                "occasion_type": OccasionType.PROMOTION,
                "content": "Dear John! We have a special offer for you this month. Contact us to learn more!",
                "status": MessageStatus.APPROVED,
                "generated_by": GeneratedBy.MANUAL,
                "approved_by": manager.id,
                "approved_at": datetime.utcnow() - timedelta(hours=5),
            },

            # Sent messages
            {
                "contact": contacts[2],
                "occasion_type": OccasionType.BIRTHDAY,
                "content": "Уважаемый Дмитрий! Поздравляем с Днем рождения! Желаем новых достижений и успехов!",
                "status": MessageStatus.SENT,
                "generated_by": GeneratedBy.AI,
                "approved_by": admin.id,
                "approved_at": datetime.utcnow() - timedelta(days=1),
                "sent_at": datetime.utcnow() - timedelta(hours=20),
                "metadata": {"model": "claude-sonnet-4", "tokens": 155, "cost_usd": 0.0024}
            },
            {
                "contact": contacts[5],
                "occasion_type": OccasionType.HOLIDAY,
                "content": "Уважаемый Олег! Поздравляем с праздником! Желаем успехов и благополучия!",
                "status": MessageStatus.SENT,
                "generated_by": GeneratedBy.AI,
                "approved_by": manager.id,
                "approved_at": datetime.utcnow() - timedelta(days=2),
                "sent_at": datetime.utcnow() - timedelta(days=1, hours=15),
                "metadata": {"model": "claude-sonnet-4", "tokens": 148, "cost_usd": 0.0023}
            },

            # Draft messages
            {
                "contact": contacts[6],
                "occasion_type": OccasionType.CUSTOM,
                "content": "Hurmatli Aziza! Sizga katta muvaffaqiyatlar tilaymiz!",
                "status": MessageStatus.DRAFT,
                "generated_by": GeneratedBy.MANUAL,
            },
        ]

        messages = []
        for msg_data in messages_data:
            contact = msg_data.pop("contact")
            approved_by = msg_data.pop("approved_by", None)
            message = Message(
                contact_id=contact.id,
                created_by=admin.id,
                approved_by=approved_by,
                **msg_data
            )
            db.add(message)
            messages.append(message)

            # Create history entry
            history = MessageHistory(
                message_id=message.id,
                action="created",
                user_id=admin.id,
                new_content=message.content
            )
            db.add(history)

        db.commit()
        print(f"✓ Created {len(messages)} messages")

        # Create sample campaigns
        campaigns_data = [
            {
                "name": "Birthday Campaign March 2024",
                "description": "Automated birthday greetings for March",
                "occasion_type": OccasionType.BIRTHDAY,
                "segment_filter": {},
                "schedule_type": ScheduleType.SCHEDULED,
                "scheduled_at": datetime.utcnow() + timedelta(days=7),
                "status": CampaignStatus.ACTIVE,
                "stats": {"generated_count": 15, "sent_count": 10, "failed_count": 0}
            },
            {
                "name": "New Year Greetings 2024",
                "description": "New Year wishes for all VIP clients",
                "occasion_type": OccasionType.NEW_YEAR,
                "segment_filter": {"segment": "VIP"},
                "schedule_type": ScheduleType.SCHEDULED,
                "scheduled_at": datetime(2024, 12, 31, 10, 0),
                "status": CampaignStatus.DRAFT,
                "stats": {"generated_count": 0, "sent_count": 0, "failed_count": 0}
            },
            {
                "name": "Monthly Newsletter",
                "description": "Monthly updates for all clients",
                "occasion_type": OccasionType.CUSTOM,
                "segment_filter": {},
                "schedule_type": ScheduleType.RECURRING,
                "recurrence_rule": "0 10 1 * *",  # First day of month at 10:00
                "status": CampaignStatus.ACTIVE,
                "stats": {"generated_count": 50, "sent_count": 48, "failed_count": 2}
            },
        ]

        campaigns = []
        for campaign_data in campaigns_data:
            campaign = Campaign(**campaign_data, created_by=admin.id)
            db.add(campaign)
            campaigns.append(campaign)

        db.commit()
        print(f"✓ Created {len(campaigns)} campaigns")

        # Create sample templates
        templates_data = [
            {
                "name": "Birthday Template (Russian)",
                "occasion_type": OccasionType.BIRTHDAY,
                "segment": ContactSegment.VIP,
                "content": "Уважаемый(ая) {{name}}! Поздравляем Вас с Днем рождения! Желаем успехов, здоровья и процветания!",
                "language": Language.RU,
                "usage_count": 15
            },
            {
                "name": "Birthday Template (English)",
                "occasion_type": OccasionType.BIRTHDAY,
                "segment": ContactSegment.REGULAR,
                "content": "Dear {{name}}! Happy Birthday! Wishing you success, health and prosperity!",
                "language": Language.EN,
                "usage_count": 8
            },
            {
                "name": "New Year Template (Russian)",
                "occasion_type": OccasionType.NEW_YEAR,
                "segment": None,
                "content": "Уважаемый(ая) {{name}}! Поздравляем с Новым годом! Желаем успехов в новом году!",
                "language": Language.RU,
                "usage_count": 25
            },
            {
                "name": "Promotion Template",
                "occasion_type": OccasionType.PROMOTION,
                "segment": ContactSegment.NEW_CLIENT,
                "content": "Dear {{name}}! We have a special offer for you! Contact us to learn more.",
                "language": Language.EN,
                "usage_count": 12
            },
            {
                "name": "Custom Template (Uzbek)",
                "occasion_type": OccasionType.CUSTOM,
                "segment": None,
                "content": "Hurmatli {{name}}! Sizga katta muvaffaqiyatlar tilaymiz!",
                "language": Language.UZ,
                "usage_count": 5
            },
        ]

        templates = []
        for template_data in templates_data:
            template = Template(**template_data, created_by=admin.id)
            db.add(template)
            templates.append(template)

        db.commit()
        print(f"✓ Created {len(templates)} templates")

        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nLogin credentials:")
        print("  Admin:   admin@crowe.uz / password123")
        print("  Manager: manager@crowe.uz / password123")
        print("  Viewer:  viewer@crowe.uz / password123")
        print("\nStatistics:")
        print(f"  Users:     {len([admin, manager, viewer])}")
        print(f"  Contacts:  {len(contacts)}")
        print(f"  Messages:  {len(messages)}")
        print(f"  Campaigns: {len(campaigns)}")
        print(f"  Templates: {len(templates)}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("AI CRM Messaging System - Database Seeder")
    print("="*50)
    seed_database()
