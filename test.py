from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Column, DECIMAL, Date, DateTime, Enum, ForeignKey, Index, JSON, String, TIMESTAMP, Table, Text, text, Integer
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYINT
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()
metadata = mapper_registry.metadata


@mapper_registry.mapped
@dataclass
class Bcs:
    __tablename__ = 'bcs'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    typ: Optional[str] = field(default=None, metadata={'sa': Column(Enum('БЦ', 'ТЦ', 'businessCenter', 'shoppingCenter', 'warehouse'))})
    name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    parent_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('bcs.id'), index=True)})
    address: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    editDate: Optional[date] = field(default=None, metadata={'sa': Column(Date)})
    created_at: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})
    updated_at: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    parent: Optional[Bcs] = field(default=None, metadata={'sa': relationship('Bcs', remote_side=[id], back_populates='parent_reverse')})
    parent_reverse: List[Bcs] = field(default_factory=list, metadata={'sa': relationship('Bcs', remote_side=[parent_id], back_populates='parent')})
    buildings: List[Buildings] = field(default_factory=list, metadata={'sa': relationship('Buildings', back_populates='bc')})
    offers: List[Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='bc')})


t_history_price_with_max_time_view = Table(
    'history_price_with_max_time_view', metadata,
    Column('history_price_id', INTEGER(11)),
    Column('time', DateTime),
    Column('price', BIGINT(20))
)


t_history_promo_with_max_date_view = Table(
    'history_promo_with_max_date_view', metadata,
    Column('services', Enum('free', 'paid', 'colorized', 'premium', 'top3')),
    Column('history_promo_id', INTEGER(11)),
    Column('date', Date)
)


@mapper_registry.mapped
@dataclass
class Locations:
    __tablename__ = 'locations'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})

    newbuildings: List[Newbuildings] = field(default_factory=list, metadata={'sa': relationship('Newbuildings', back_populates='region')})


@mapper_registry.mapped
@dataclass
class Log:
    __tablename__ = 'log'
    __sa_dataclass_metadata_key__ = 'sa'

    stamp: datetime = field(init=False, metadata={'sa': Column(DateTime, primary_key=True)})
    deal_type: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    offer_type: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    page: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    code: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})


@mapper_registry.mapped
@dataclass
class Proxy:
    __tablename__ = 'proxy'
    __sa_dataclass_metadata_key__ = 'sa'

    ipp: str = field(init=False, metadata={'sa': Column(String(22), primary_key=True)})
    reason: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})


@mapper_registry.mapped
@dataclass
class SearchResults:
    __tablename__ = 'search_results'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(INTEGER(11), primary_key=True, unique=True)})
    ranking: int = field(metadata={'sa': Column(INTEGER(11), nullable=False)})
    link: str = field(metadata={'sa': Column(Text, nullable=False)})
    account_type: Optional[str] = field(default=None, metadata={'sa': Column(Text)})
    price: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    promo_type: Optional[str] = field(default=None, metadata={'sa': Column(Enum('top3', 'premium', 'paid', 'colorized', 'free'))})
    auction_bet: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    last_updated: Optional[datetime] = field(default=None, metadata={'sa': Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))})

    search_pivots: List[SearchPivots] = field(default_factory=list, metadata={'sa': relationship('SearchPivots', back_populates='offer')})


@mapper_registry.mapped
@dataclass
class SearchSources:
    __tablename__ = 'search_sources'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True, unique=True)})
    req_name: str = field(metadata={'sa': Column(Text, nullable=False)})
    category: str = field(metadata={'sa': Column(Enum('office', 'shoppingArea', 'apartments'), nullable=False)})
    dealType: str = field(metadata={'sa': Column(Enum('rent', 'sale'), nullable=False)})
    params: dict = field(metadata={'sa': Column(JSON, nullable=False)})
    last_upd: Optional[datetime] = field(default=None, metadata={'sa': Column(TIMESTAMP)})

    search_pivots: List[SearchPivots] = field(default_factory=list, metadata={'sa': relationship('SearchPivots', back_populates='req')})


@mapper_registry.mapped
@dataclass
class Users:
    __tablename__ = 'users'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    user_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    isCianPartner: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isSubAgent: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    cianProfileStatus: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    isPassportVerified: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isHidden: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    account_type: Optional[str] = field(default=None, metadata={'sa': Column(Enum('realtor', 'agency', 'uk', 'owner', 'specialist', 'managementCompany', 'rentDepartment', 'anunimus-dolboebus'))})
    trust: Optional[str] = field(default=None, metadata={'sa': Column(Enum('involved', 'notInvolved', 'new', 'excluded', 'danger'))})

    phones: List[Phones] = field(default_factory=list, metadata={'sa': relationship('Phones', back_populates='user')})
    offers: List[Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='users')})


@mapper_registry.mapped
@dataclass
class Newbuildings:
    __tablename__ = 'newbuildings'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    region_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('locations.id'), index=True)})
    address: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})

    region: Optional[Locations] = field(default=None, metadata={'sa': relationship('Locations', back_populates='newbuildings')})
    houses: List[Houses] = field(default_factory=list, metadata={'sa': relationship('Houses', back_populates='newbuilding')})
    buildings: List[Buildings] = field(default_factory=list, metadata={'sa': relationship('Buildings', back_populates='newbuilding')})
    offers: List[Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='newbuilding')})


@mapper_registry.mapped
@dataclass
class Phones:
    __tablename__ = 'phones'
    __sa_dataclass_metadata_key__ = 'sa'

    user_id: int = field(metadata={'sa': Column(ForeignKey('users.id'), primary_key=True, nullable=False)})
    phone: int = field(metadata={'sa': Column(BIGINT(20), primary_key=True, nullable=False)})

    user: Users = field(metadata={'sa': relationship('Users', back_populates='phones')})


@mapper_registry.mapped
@dataclass
class SearchPivots:
    __tablename__ = 'search_pivots'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    req_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('search_sources.id'), index=True)})
    offer_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('search_results.id'), index=True)})
    created_at: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Optional[SearchResults] = field(default=None, metadata={'sa': relationship('SearchResults', back_populates='search_pivots')})
    req: Optional[SearchSources] = field(default=None, metadata={'sa': relationship('SearchSources', back_populates='search_pivots')})


@mapper_registry.mapped
@dataclass
class Houses:
    __tablename__ = 'houses'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    newbuilding_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('newbuildings.id'), index=True)})
    name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    address: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})

    newbuilding: Optional[Newbuildings] = field(default=None, metadata={'sa': relationship('Newbuildings', back_populates='houses')})
    offers: List[Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='house')})


@mapper_registry.mapped
@dataclass
class Buildings(Houses):
    __tablename__ = 'buildings'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('houses.id'), primary_key=True)})
    newbuilding_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('newbuildings.id'), index=True)})
    bc_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('bcs.id'), index=True)})
    cian_address: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    dadata_address: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    fias: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    latitude: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    longitude: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    build_year: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    building_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    cargo_lifts_count: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    passenger_lifts_count: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    access_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    deadline: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    material_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    heating_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    floors_count: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    land_area: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(7, 2))})
    land_area_unit_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    land_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    land_status: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    is_apartments: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    location_id: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    location_name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    raion_id: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    raion_name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    street_id: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    street_name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    house_id: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    house_name: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    updated: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    bc: Optional[Bcs] = field(default=None, metadata={'sa': relationship('Bcs', back_populates='buildings')})
    newbuilding: Optional[Newbuildings] = field(default=None, metadata={'sa': relationship('Newbuildings', back_populates='buildings')})
    offers: List[Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='building')})


@mapper_registry.mapped
@dataclass
class Offers:
    __tablename__ = 'offers'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    cianUserId: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('users.id'), index=True)})
    bc_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('bcs.id'), index=True)})
    house_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('houses.id'), index=True)})
    newbuilding_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('newbuildings.id'), index=True)})
    building_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('buildings.id'), index=True)})
    description: Optional[str] = field(default=None, metadata={'sa': Column(String(4095))})
    creationDate: Optional[date] = field(default=None, metadata={'sa': Column(Date)})
    editDate: Optional[date] = field(default=None, metadata={'sa': Column(Date)})
    added: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    category: Optional[str] = field(default=None, metadata={'sa': Column(Enum('office', 'shoppingArea', 'flat', 'freeAppointmentObject', 'newBuildingFlat', 'dailyFlat', 'business', 'building'))})
    dealType: Optional[str] = field(default=None, metadata={'sa': Column(Enum('rent', 'sale'))})
    status: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    is_status_set: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1), index=True)})
    currency: Optional[str] = field(default=None, metadata={'sa': Column(Enum('rur', 'usd', 'eur'))})
    paymentPeriod: Optional[str] = field(default=None, metadata={'sa': Column(Enum('monthly', 'annual'))})
    floorNumber: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    floorsCount: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    roomsCount: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    totalArea: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(9, 2))})
    fairplay: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isPro: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isAuction: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isInResults: Optional[int] = field(default=None, metadata={'sa': Column(TINYINT(1), server_default=text("'1'"))})
    priceType: Optional[str] = field(default=None, metadata={'sa': Column(Enum('squareMeter', 'all'))})
    price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    priceRur: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    vatPrice: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    minArea: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(7, 2))})
    auction_currentBet: Optional[int] = field(default=None, metadata={'sa': Column(INTEGER(11))})
    created_at: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})
    updated_at: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})
    address_string: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    latitude: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})
    longitude: Optional[Decimal] = field(default=None, metadata={'sa': Column(DECIMAL(10, 6))})

    bc: Optional[Bcs] = field(default=None, metadata={'sa': relationship('Bcs', back_populates='offers')})
    building: Optional[Buildings] = field(default=None, metadata={'sa': relationship('Buildings', back_populates='offers')})
    users: Optional[Users] = field(default=None, metadata={'sa': relationship('Users', back_populates='offers')})
    house: Optional[Houses] = field(default=None, metadata={'sa': relationship('Houses', back_populates='offers')})
    newbuilding: Optional[Newbuildings] = field(default=None, metadata={'sa': relationship('Newbuildings', back_populates='offers')})
    bets: List[Bets] = field(default_factory=list, metadata={'sa': relationship('Bets', back_populates='offer')})
    history_price: List[HistoryPrice] = field(default_factory=list, metadata={'sa': relationship('HistoryPrice', back_populates='offers')})
    history_promo: List[HistoryPromo] = field(default_factory=list, metadata={'sa': relationship('HistoryPromo', back_populates='offers')})
    prices: List[Prices] = field(default_factory=list, metadata={'sa': relationship('Prices', back_populates='offer')})
    prices_old: List[PricesOld] = field(default_factory=list, metadata={'sa': relationship('PricesOld', back_populates='offer')})
    stats_daily: List[StatsDaily] = field(default_factory=list, metadata={'sa': relationship('StatsDaily', back_populates='offers')})


@mapper_registry.mapped
@dataclass
class Bets:
    __tablename__ = 'bets'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    offer_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('offers.id'), index=True)})
    auction_curentBet: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    timestamp: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Optional[Offers] = field(default=None, metadata={'sa': relationship('Offers', back_populates='bets')})


@mapper_registry.mapped
@dataclass
class HistoryPrice:
    __tablename__ = 'history_price'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    time: datetime = field(init=False, metadata={'sa': Column(DateTime, primary_key=True, nullable=False)})
    price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='history_price')})


@mapper_registry.mapped
@dataclass
class HistoryPromo:
    __tablename__ = 'history_promo'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    date_: date = field(init=False, metadata={'sa': Column('date', Date, primary_key=True, nullable=False)})
    services: Optional[str] = field(default=None, metadata={'sa': Column(Enum('free', 'paid', 'colorized', 'premium', 'top3'))})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='history_promo')})


@mapper_registry.mapped
@dataclass
class Prices:
    __tablename__ = 'prices'
    __table_args__ = (
        Index('prices_offer_id_price_uindex', 'offer_id', 'price', unique=True),
    )
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    offer_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('offers.id'), index=True)})
    price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_rur: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    vat_price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    timestamp: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Optional[Offers] = field(default=None, metadata={'sa': relationship('Offers', back_populates='prices')})


@mapper_registry.mapped
@dataclass
class PricesOld:
    __tablename__ = 'prices_old'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(INTEGER(11), primary_key=True)})
    offer_id: Optional[int] = field(default=None, metadata={'sa': Column(ForeignKey('offers.id'), index=True)})
    price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_rur: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    price_type: Optional[str] = field(default=None, metadata={'sa': Column(String(255))})
    vat_price: Optional[int] = field(default=None, metadata={'sa': Column(BIGINT(20))})
    timestamp: Optional[datetime] = field(default=None, metadata={'sa': Column(DateTime)})

    offer: Optional[Offers] = field(default=None, metadata={'sa': relationship('Offers', back_populates='prices_old')})


@mapper_registry.mapped
@dataclass
class StatsDaily:
    __tablename__ = 'stats_daily'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(metadata={'sa': Column(ForeignKey('offers.id'), primary_key=True, nullable=False)})
    date_: date = field(init=False, metadata={'sa': Column('date', Date, primary_key=True, nullable=False)})
    stats_total: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})
    stats_daily: Optional[int] = field(default=None, metadata={'sa': Column(SMALLINT(6))})

    offers: Offers = field(metadata={'sa': relationship('Offers', back_populates='stats_daily')})


@mapper_registry.mapped
@dataclass
class Users:
    __tablename__ = 'users'
    __sa_dataclass_metadata_key__ = 'sa'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})
    name: str | None = field(default=None, metadata={'sa': Column(String(255))})
    user_type: str | None = field(default=None, metadata={'sa': Column(String(255))})
    isCianPartner: int | None = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isSubAgent: int | None = field(default=None, metadata={'sa': Column(TINYINT(1))})
    cianProfileStatus: str | None = field(default=None, metadata={'sa': Column(String(255))})
    isPassportVerified: int | None = field(default=None, metadata={'sa': Column(TINYINT(1))})
    isHidden: int | None = field(default=None, metadata={'sa': Column(TINYINT(1))})
    account_type: str | None = field(default=None, metadata={'sa': Column(Enum('realtor', 'agency', 'uk', 'owner', 'specialist', 'managementCompany', 'rentDepartment', 'anunimus-dolboebus'))})
    trust: str | None = field(default=None, metadata={'sa': Column(Enum('involved', 'notInvolved', 'new', 'excluded', 'danger'))})

    phones: [Phones] = field(default_factory=list, metadata={'sa': relationship('Phones', back_populates='user')})
    offers: [Offers] = field(default_factory=list, metadata={'sa': relationship('Offers', back_populates='users')})
