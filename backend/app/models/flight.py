"""Database models for airports and flight offers."""

from datetime import date, datetime
import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarative class for ORM models."""


class Airport(Base):
    """Airport master table keyed by IATA code."""

    __tablename__ = "airports"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    city: Mapped[str] = mapped_column(String(80))
    country: Mapped[str] = mapped_column(String(80))


class FlightOffer(Base):
    """Flight offer table used by recommendation and alert features."""

    __tablename__ = "flight_offers"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(30), index=True)
    external_offer_id: Mapped[str] = mapped_column(String(120), index=True)
    origin_airport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("airports.id"))
    destination_airport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("airports.id"))
    departure_date: Mapped[date] = mapped_column(Date)
    return_date: Mapped[date] = mapped_column(Date, nullable=True)
    cabin_class: Mapped[str] = mapped_column(String(20), default="ECONOMY")
    price_total: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    seats_remaining: Mapped[int] = mapped_column(Integer, default=9)
    raw_payload: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(3072), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    origin = relationship("Airport", foreign_keys=[origin_airport_id])
    destination = relationship("Airport", foreign_keys=[destination_airport_id])
