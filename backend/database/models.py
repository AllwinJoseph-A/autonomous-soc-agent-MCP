from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

# This is the base class all our tables will inherit from
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    location = Column(String)
    is_active = Column(Boolean, default=True)

class LoginHistory(Base):
    __tablename__ = "login_history"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    ip_address = Column(String)
    location = Column(String)
    timestamp = Column(String)
    status = Column(String) # e.g., "SUCCESS" or "FAILED"

class ThreatIntel(Base):
    __tablename__ = "threat_intel"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    risk_level = Column(String) # e.g., "HIGH", "MEDIUM", "LOW"
    known_botnet = Column(Boolean, default=False)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    severity = Column(String)
    resolved = Column(Boolean, default=False)