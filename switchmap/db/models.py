"""Define SQLalchemy database table models."""

# Standard imports
import datetime

# SQLalchemy imports
from sqlalchemy import (
    Column, DateTime, ForeignKey, text, UniqueConstraint,
    PrimaryKeyConstraint, ForeignKeyConstraint)
from sqlalchemy.dialects.mysql import BIGINT, VARBINARY, BIT
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import Null
from sqlalchemy.orm import Session

# Project imports
from switchmap.db import SCOPED_SESSION, ENGINE

###############################################################################
# Create BASE SQLAlchemy class. This must be in the same file as the database
# definitions or else the database won't be created on install. Learned via
# trial and error.
BASE = declarative_base()

# GraphQL: Bind engine to metadata of the base class
BASE.metadata.bind = SCOPED_SESSION

# GraphQL: Used by graphql to execute queries
BASE.query = SCOPED_SESSION.query_property()

_METADATA = BASE.metadata

###############################################################################


class Location(BASE):
    """Database table definition."""

    __tablename__ = 'smap_location'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_location = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    name = Column(VARBINARY(256))
    company_name = Column(
        VARBINARY(256), nullable=True, default=Null)
    address_0 = Column(VARBINARY(256), nullable=True, default=Null)
    address_1 = Column(VARBINARY(256), nullable=True, default=Null)
    address_2 = Column(VARBINARY(256), nullable=True, default=Null)
    city = Column(VARBINARY(128), nullable=True, default=Null)
    state = Column(VARBINARY(128), nullable=True, default=Null)
    country = Column(VARBINARY(128), nullable=True, default=Null)
    postal_code = Column(VARBINARY(64), nullable=True, default=Null)
    phone = Column(VARBINARY(128), nullable=True, default=Null)
    notes = Column(VARBINARY(2048), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)


class Oui(BASE):
    """Database table definition."""

    __tablename__ = 'smap_oui'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_oui = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    oui = Column(VARBINARY(256), unique=True)
    organization = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)


class Event(BASE):
    """Database table definition."""

    __tablename__ = 'smap_event'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_event = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    event = Column(VARBINARY(256), unique=True)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)


class Device(BASE):
    """Database table definition."""

    __tablename__ = 'smap_device'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_device = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_location = Column(
        ForeignKey('smap_location.idx_location'),
        nullable=False, index=True, default=1, server_default=text('1'))
    idx_event = Column(
        ForeignKey('smap_event.idx_event'),
        nullable=False, index=True, default=1, server_default=text('1'))
    sys_name = Column(
        VARBINARY(256), nullable=True, default=Null)
    hostname = Column(
        VARBINARY(256), nullable=True, default=Null)
    sys_description = Column(
        VARBINARY(1024), nullable=True, default=Null)
    sys_objectid = Column(
        VARBINARY(256), nullable=True, default=Null)
    sys_uptime = Column(BIGINT(20, unsigned=True))
    last_polled = Column(BIGINT(20, unsigned=True))
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Uses cascade='delete,all' to propagate the deletion of an entry
    device_to_location = relationship(
        Location,
        backref=backref(
            'device_to_location', uselist=True, cascade='delete,all'))

    device_to_event = relationship(
        Event,
        backref=backref(
            'device_to_event', uselist=True, cascade='delete,all'))


class L1Interface(BASE):
    """Database table definition."""

    __tablename__ = 'smap_l1interface'
    __table_args__ = (
        UniqueConstraint('ifindex', 'idx_device'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_l1interface = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_device = Column(
        ForeignKey('smap_device.idx_device'),
        nullable=False, index=True, default=1, server_default=text('1'))
    ifindex = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    duplex = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    ethernet = Column(BIT(1), default=0)
    nativevlan = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    trunk = Column(BIT(1), default=0)
    ifspeed = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    ifalias = Column(VARBINARY(256), nullable=True, default=Null)
    ifdescr = Column(VARBINARY(256), nullable=True, default=Null)
    ifadminstatus = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    ifoperstatus = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    ts_idle = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    cdpcachedeviceid = Column(VARBINARY(256), nullable=True, default=Null)
    cdpcachedeviceport = Column(VARBINARY(256), nullable=True, default=Null)
    cdpcacheplatform = Column(VARBINARY(256), nullable=True, default=Null)
    lldpremportdesc = Column(VARBINARY(256), nullable=True, default=Null)
    lldpremsyscapenabled = Column(VARBINARY(256), nullable=True, default=Null)
    lldpremsysdesc = Column(VARBINARY(2048), nullable=True, default=Null)
    lldpremsysname = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Uses cascade='delete,all' to propagate the deletion of an entry
    l1interface_to_device = relationship(
        Device,
        backref=backref(
            'l1interface_to_device', uselist=True, cascade='delete,all'))


class Vlan(BASE):
    """Database table definition."""

    __tablename__ = 'smap_vlan'
    __table_args__ = (
        UniqueConstraint('vlan', 'idx_device'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_vlan = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_device = Column(
        ForeignKey('smap_device.idx_device'),
        nullable=False, index=True, default=1, server_default=text('1'))
    vlan = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    name = Column(VARBINARY(256), nullable=True, default=Null)
    state = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Uses cascade='delete,all' to propagate the deletion of an entry
    vlan_to_device = relationship(
        Device,
        backref=backref(
            'vlan_to_device', uselist=True, cascade='delete,all'))


class Mac(BASE):
    """Database table definition."""

    __tablename__ = 'smap_mac'
    __table_args__ = (
        UniqueConstraint('mac'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_mac = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_oui = Column(
        ForeignKey('smap_oui.idx_oui'),
        nullable=False, index=True, default=1, server_default=text('1'))
    idx_event = Column(
        ForeignKey('smap_event.idx_event'),
        nullable=False, index=True, default=1, server_default=text('1'))
    mac = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    mac_to_oui = relationship(
        Oui,
        backref=backref(
            'mac_to_oui', uselist=True, cascade='delete,all'))

    mac_to_event = relationship(
        Event,
        backref=backref(
            'mac_to_event', uselist=True, cascade='delete,all'))


class MacIp(BASE):
    """Database table definition."""

    __tablename__ = 'smap_macip'
    __table_args__ = (
        UniqueConstraint('idx_device', 'ip_', 'idx_mac'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_macip = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_device = Column(
        ForeignKey('smap_device.idx_device'),
        nullable=False, index=True, default=1, server_default=text('1'))
    idx_mac = Column(
        ForeignKey('smap_mac.idx_mac'),
        nullable=False, index=True, default=1, server_default=text('1'))
    ip_ = Column(VARBINARY(256), nullable=True, default=Null)
    hostname = Column(VARBINARY(256), nullable=True, default=Null)
    type = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Uses cascade='delete,all' to propagate the deletion of an entry
    macip_to_device = relationship(
        Device,
        backref=backref(
            'macip_to_device', uselist=True, cascade='delete,all'))

    macip_to_mac = relationship(
        Mac,
        backref=backref(
            'macip_to_mac', uselist=True, cascade='delete,all'))


class MacPort(BASE):
    """Database table definition."""

    __tablename__ = 'smap_macport'
    __table_args__ = (
        UniqueConstraint('idx_l1interface', 'idx_mac'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_macport = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_l1interface = Column(
        ForeignKey('smap_l1interface.idx_l1interface'),
        nullable=False, index=True, default=1, server_default=text('1'))
    idx_mac = Column(
        ForeignKey('smap_mac.idx_mac'),
        nullable=False, index=True, default=1, server_default=text('1'))
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime, nullable=False,
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Uses cascade='delete,all' to propagate the deletion of an entry
    macport_to_l1interface = relationship(
        L1Interface,
        backref=backref(
            'macport_to_l1interface', uselist=True, cascade='delete,all'))

    macport_to_mac = relationship(
        Mac,
        backref=backref(
            'macport_to_mac', uselist=True, cascade='delete,all'))


def create_all_tables():
    """Ensure all tables are created."""
    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection) as session:
            BASE.metadata.create_all(session.get_bind(), checkfirst=True)
