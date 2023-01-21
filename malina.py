from __future__ import annotations

from dcs import dataclass, field
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Column, DECIMAL, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Crm:
    __tablename__ = 'crm'
    __sa_dataclass_metadata_key__ = 'sa'

    lot_id: int = field(metadata={'sa': Column(BIGINT(20), primary_key=True, unique=True)})
    title: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    deal_type: Optional[str] = field(default=None, metadata={'sa': Column(Enum('sale', 'rent', ''))})
    city: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    street: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    subway: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    minutes_to_subway_walk: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    minutes_to_subway_bus: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    yardage: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    floor: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    one_level: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    furnish: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    layout: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    ceiling_height: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    parking: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    draught: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    power: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(10, 0))})
    description: Optional[str] = field(default=None, metadata={'sa': Column(Text)})
    price_per_m2_per_year: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_per_m2: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_per_month: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    taxes: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    utility_payments: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    commission: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    full_name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    phone: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    email: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    agency_commission: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    additional_info: Optional[str] = field(default=None, metadata={'sa': Column(Text)})
    tenant: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    lease_term_from: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    lease_term_up_to: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    monthly_rent: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    annual_rental_flow: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    payback: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    profitability: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    annual_indexation: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    parking_price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    seats_number: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    official_deal: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    source_file: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})

    images: List[Images] = field(default_factory=list, metadata={'sa': relationship('Images', back_populates='lot')})


@mapper_registry.mapped
@dataclass
class Images:
    __tablename__ = 'images'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(BIGINT(20), primary_key=True, unique=True)})
    lot_id: int = field(metadata={'sa': Column(ForeignKey('crm.lot_id'), nullable=False, index=True)})
    filename: str = field(metadata={'sa': Column(String(255), nullable=False)})

    lot: Crm = field(metadata={'sa': relationship('Crm', back_populates='images')})
