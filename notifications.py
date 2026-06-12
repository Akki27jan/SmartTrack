# notifications.py

from datetime import datetime
from pydantic import BaseModel
from database import cursor, conn


class EmployeeNotification(BaseModel):
    employee_id: str
    type: str
    subject: str
    message: str


class CompanyNotification(BaseModel):
    company_id: str
    type: str
    subject: str
    message: str


def create_notification_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_notifications (
            notif_id SERIAL PRIMARY KEY,
            employee_id VARCHAR(100),
            type VARCHAR(100),
            subject VARCHAR(255),
            message TEXT,
            status BOOLEAN DEFAULT TRUE,
            sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_notifications (
            notif_id SERIAL PRIMARY KEY,
            company_id VARCHAR(100),
            type VARCHAR(100),
            subject VARCHAR(255),
            message TEXT,
            status VARCHAR(20) DEFAULT 'sent',
            sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()