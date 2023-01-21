from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Column, DECIMAL, Date, DateTime, Enum, ForeignKey, Integer, SmallInteger, String, text, Boolean
from sqlalchemy.orm import relationship

from dcs import mapper_registry


@mapper_registry.mapped
@dataclass
class Locations:
    __tablename__ = 'locations'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    name: str | None = field(default=None, metadata={'sa': Column(String(255))})

    buildings: [Buildings] = field(default_factory=list, metadata={'sa': relationship('Buildings', back_populates='location')})


@mapper_registry.mapped
@dataclass
class Buildings:
    __tablename__ = 'buildings'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(Integer, primary_key=True)})
    cian_address: str | None = field(default=None, metadata={'sa': Column(String(255))})
    dadata_address: str | None = field(default=None, metadata={'sa': Column(String(255))})
    fias: str | None = field(default=None, metadata={'sa': Column(String(255))})
    latitude: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    longitude: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    build_year: int | None = field(default=None, metadata={'sa': Column(Integer)})
    building_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    cargo_lifts_count: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    passenger_lifts_count: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    access_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    deadline: str | None = field(default=None, metadata={'sa': Column(String(255))})
    material_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    heating_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    floors_count: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    land_area: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(7, 2))})
    land_area_unit_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    land_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    land_status: str | None = field(default=None, metadata={'sa': Column(String(255))})
    is_apartments: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    location_id: int | None = field(default=None, metadata={'sa': Column(Integer)})
    location_name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    raion_id: int | None = field(default=None, metadata={'sa': Column(Integer)})
    raion_name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    street_id: int | None = field(default=None, metadata={'sa': Column(Integer)})
    street_name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    house_name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    updated: datetime | None = field(default=None, metadata={'sa': Column(DateTime)})

    location: Locations = field(default=1, metadata={'sa': relationship('Locations', back_populates='buildings')})
    offers: [Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='building')})


@mapper_registry.mapped
@dataclass
class Phones:
    __tablename__ = 'phones'
    __sa_dataclass_metadata_key__ = 'sa'

    user_id: int = field(metadata={'sa': Column(ForeignKey('users.id'), primary_key=True, nullable=False)})
    phone: int = field(metadata={'sa': Column(BigInteger, primary_key=True, nullable=False)})

    user: Users = field(metadata={'sa': relationship('Users', back_populates='phones')})


@mapper_registry.mapped
@dataclass
class Users:
    __tablename__ = 'users'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    user_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    isCianPartner: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    isSubAgent: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    cianProfileStatus: str | None = field(default=None, metadata={'sa': Column(String(255))})
    isPassportVerified: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    isHidden: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    account_type: str | None = field(default=None, metadata={'sa': Column(Enum('realtor', 'agency', 'uk', 'owner', 'specialist', 'managementCompany', 'rentDepartment', 'anunimus-dolboebus', name='acc_type'))})
    trust: str | None = field(default=None, metadata={'sa': Column(Enum('involved', 'notInvolved', 'new', 'excluded', 'danger', name='trust'))})

    phones: [Phones] = field(default_factory=list, metadata={'sa': relationship('Phones', back_populates='user')})
    offers: [Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='users')})


@mapper_registry.mapped
@dataclass
class Offers:
    __tablename__ = 'offers'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    cianUserId: int | None = field(default=None, metadata={'sa': Column(ForeignKey('users.id'), index=True)})
    building_id: int | None = field(default=None, metadata={'sa': Column(ForeignKey('buildings.id'), index=True)})
    description: str | None = field(default=None, metadata={'sa': Column(String(4095))})
    creationDate: date | None = field(default=None, metadata={'sa': Column(Date)})
    editDate: date | None = field(default=None, metadata={'sa': Column(Date)})
    added: str | None = field(default=None, metadata={'sa': Column(String(255))})
    category: str | None = field(default=None, metadata={'sa': Column(Enum('office', 'shoppingArea', 'flat', 'freeAppointmentObject', 'newBuildingFlat', 'dailyFlat', 'business', 'building', name='block_type'))})
    dealType: str | None = field(default=None, metadata={'sa': Column(Enum('rent', 'sale', name='deal_type'))})
    status: str | None = field(default=None, metadata={'sa': Column(String(255))})
    is_status_set: int | None = field(default=None, metadata={'sa': Column(Boolean, index=True)})
    currency: str | None = field(default=None, metadata={'sa': Column(Enum('rur', 'usd', 'eur', name='cur'))})
    paymentPeriod: str | None = field(default=None, metadata={'sa': Column(Enum('monthly', 'annual', name='payment_period'))})
    floorNumber: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    floorsCount: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    roomsCount: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    totalArea: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(9, 2))})
    fairplay: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    isPro: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    isAuction: int | None = field(default=None, metadata={'sa': Column(Boolean)})
    isInResults: int | None = field(default=None, metadata={'sa': Column(Boolean, server_default=text("'1'"))})
    priceType: str | None = field(default=None, metadata={'sa': Column(Enum('squareMeter', 'all', name='price_type'))})
    price: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    priceRur: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    vatPrice: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    minArea: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(7, 2))})
    auction_currentBet: int | None = field(default=None, metadata={'sa': Column(Integer)})
    created_at: datetime | None = field(default=None, metadata={'sa': Column(DateTime)})
    updated_at: datetime | None = field(default=None, metadata={'sa': Column(DateTime)})
    address_string: str | None = field(default=None, metadata={'sa': Column(String(255))})
    latitude: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    longitude: Decimal | None = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})

    building: Buildings | None = field(default=None, metadata={'sa': relationship('Buildings', back_populates='offers')})
    users: Users | None = field(default=None, metadata={'sa': relationship('Users', back_populates='offers')})
    bets: [Bets] = field(default_factory=list, metadata={'sa': relationship('Bets', back_populates='offer')})
    history_price: [HistoryPrice] = field(default_factory=list, metadata={'sa': relationship('HistoryPrice', back_populates='offers')})
    history_promo: [HistoryPromo] = field(default_factory=list, metadata={'sa': relationship('HistoryPromo', back_populates='offers')})
    prices: [Prices] = field(default_factory=list, metadata={'sa': relationship('Prices', back_populates='offer')})
    stats_daily: [StatsDaily] = field(default_factory=list, metadata={'sa': relationship('StatsDaily', back_populates='offers')})


@mapper_registry.mapped
@dataclass
class Bets:
    __tablename__ = 'bets'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    offer_id: int | None = field(default=None, metadata={'sa': Column(ForeignKey('offers.id'), index=True)})
    auction_curentBet: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    timestamp: datetime | None = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Offers | None = field(default=None, metadata={'sa': relationship('Offers', back_populates='bets')})


@mapper_registry.mapped
@dataclass
class HistoryPrice:
    __tablename__ = 'history_price'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    time: datetime = field(init=False, metadata={'sa': Column(DateTime, primary_key=True, nullable=False)})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='history_price')})

    price: int | None = field(default=None, metadata={'sa': Column(BigInteger)})


@mapper_registry.mapped
@dataclass
class HistoryPromo:
    __tablename__ = 'history_promo'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    date_: date = field(init=False, metadata={'sa': Column('date', Date, primary_key=True, nullable=False)})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='history_promo')})

    services: str | None = field(default=None, metadata={'sa': Column(Enum('free', 'paid', 'colorized', 'premium', 'top3', name='promo'))})


@mapper_registry.mapped
@dataclass
class Prices:
    __tablename__ = 'prices'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    offer_id: int | None = field(default=None, metadata={'sa': Column(ForeignKey('offers.id'), index=True)})
    price: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    price_rur: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    price_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    vat_price: int | None = field(default=None, metadata={'sa': Column(BigInteger)})
    timestamp: datetime | None = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Offers | None = field(default=None, metadata={'sa': relationship('Offers', back_populates='prices')})


@mapper_registry.mapped
@dataclass
class StatsDaily:
    __tablename__ = 'stats_daily'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    date_: date = field(init=False, metadata={'sa': Column('date', Date, primary_key=True, nullable=False)})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='stats_daily')})

    stats_total: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
    stats_daily: int | None = field(default=None, metadata={'sa': Column(SmallInteger)})
