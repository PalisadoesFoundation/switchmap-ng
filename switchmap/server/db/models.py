"""Define SQLalchemy database table models."""

# Standard imports
import datetime

# SQLalchemy imports
from sqlalchemy import Column, DateTime, ForeignKey, text, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, VARBINARY, BIT
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import Null
from sqlalchemy.orm import Session

# Project imports
from switchmap.server.db import SCOPED_SESSION, ENGINE

###############################################################################
# Create BASE SQLAlchemy class. This must be in the same file as the database
# definitions or else the database won't be created on install. Learned via
# trial and error.

# Default
BASE = declarative_base()

# GraphQL: Bind engine to metadata of the base class
BASE.metadata.bind = SCOPED_SESSION

# GraphQL: Used by graphql to execute queries
BASE.query = SCOPED_SESSION.query_property()

_METADATA = BASE.metadata

###############################################################################


class Oui(BASE):
    """Database table definition."""

    __tablename__ = "smap_oui"
    __table_args__ = {"mysql_engine": "InnoDB"}

    idx_oui = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    oui = Column(VARBINARY(256), unique=True, nullable=True)
    organization = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # macs = relationship(
    #     "Mac",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class Event(BASE):
    """Database table definition."""

    __tablename__ = "smap_event"
    __table_args__ = {"mysql_engine": "InnoDB"}

    idx_event = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    name = Column(VARBINARY(256), unique=True)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # zones = relationship(
    #     "Zone",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # roots = relationship(
    #     "Root",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class Root(BASE):
    """Database table definition."""

    __tablename__ = "smap_root"
    __table_args__ = {"mysql_engine": "InnoDB"}

    idx_root = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_event = Column(
        ForeignKey(Event.idx_event, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    name = Column(VARBINARY(256), unique=True)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    event = relationship(
        "Event",
        backref=backref(
            "roots",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )


class Zone(BASE):
    """Database table definition."""

    __tablename__ = "smap_zone"
    __table_args__ = {"mysql_engine": "InnoDB"}

    idx_zone = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_event = Column(
        ForeignKey(Event.idx_event, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    name = Column(VARBINARY(256))
    company_name = Column(VARBINARY(256), nullable=True, default=Null)
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
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    event = relationship(
        "Event",
        backref=backref(
            "zones",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # devices = relationship(
    #     "Device",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # macs = relationship(
    #     "Mac",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class Device(BASE):
    """Database table definition."""

    __tablename__ = "smap_device"
    __table_args__ = {"mysql_engine": "InnoDB"}

    idx_device = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    idx_zone = Column(
        ForeignKey(Zone.idx_zone, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    sys_name = Column(VARBINARY(256), nullable=True, default=Null)
    hostname = Column(VARBINARY(256), nullable=True, default=Null)
    name = Column(VARBINARY(256), nullable=True, default=Null)
    sys_description = Column(VARBINARY(1024), nullable=True, default=Null)
    sys_objectid = Column(VARBINARY(256), nullable=True, default=Null)
    sys_uptime = Column(BIGINT(20, unsigned=True))
    last_polled = Column(BIGINT(20, unsigned=True))
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    device = relationship(
        "Zone",
        backref=backref(
            "devices",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # l1interfaces = relationship(
    #     "L1Interface",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # vlans = relationship(
    #     "Vlan",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # macips = relationship(
    #     "MacIp",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class L1Interface(BASE):
    """Database table definition."""

    __tablename__ = "smap_l1interface"
    __table_args__ = (
        UniqueConstraint("ifindex", "idx_device"),
        {"mysql_engine": "InnoDB"},
    )

    idx_l1interface = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    idx_device = Column(
        ForeignKey(Device.idx_device, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
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
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    device = relationship(
        "Device",
        backref=backref(
            "l1interfaces",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # vlanports = relationship(
    #     "VlanPort",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # macports = relationship(
    #     "MacPort",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class Vlan(BASE):
    """Database table definition."""

    __tablename__ = "smap_vlan"
    __table_args__ = (
        UniqueConstraint("vlan", "idx_device"),
        {"mysql_engine": "InnoDB"},
    )

    idx_vlan = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_device = Column(
        ForeignKey(Device.idx_device, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    vlan = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    name = Column(VARBINARY(256), nullable=True, default=Null)
    state = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    device = relationship(
        "Device",
        backref=backref(
            "vlans",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # vlanports = relationship(
    #     "VlanPort",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class VlanPort(BASE):
    """Database table definition."""

    __tablename__ = "smap_vlanport"
    __table_args__ = (
        UniqueConstraint("idx_l1interface", "idx_vlan"),
        {"mysql_engine": "InnoDB"},
    )

    idx_vlanport = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    idx_l1interface = Column(
        ForeignKey(L1Interface.idx_l1interface, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    idx_vlan = Column(
        ForeignKey(Vlan.idx_vlan, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    vlan = relationship(
        "Vlan",
        backref=backref(
            "vlanports",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    l1interfaces = relationship(
        "L1Interface",
        backref=backref(
            "vlanports",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )


class Mac(BASE):
    """Database table definition."""

    __tablename__ = "smap_mac"
    __table_args__ = (
        UniqueConstraint("mac", "idx_zone"),
        {"mysql_engine": "InnoDB"},
    )

    idx_mac = Column(BIGINT(20, unsigned=True), primary_key=True, unique=True)
    idx_oui = Column(
        ForeignKey(Oui.idx_oui),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    idx_zone = Column(
        ForeignKey(Zone.idx_zone, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    mac = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    oui = relationship(
        "Oui",
        backref=backref(
            "macs", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )
    zone = relationship(
        "Zone",
        backref=backref(
            "macs", cascade="all, delete, delete-orphan", passive_deletes=True
        ),
    )

    # Define relationships from parent to child
    # Note: (no backref, variable name pluralization)
    # macports = relationship(
    #     "MacPort",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )
    # macips = relationship(
    #     "MacIp",
    #     cascade="all, delete, delete-orphan",
    #     passive_deletes=True,
    # )


class MacIp(BASE):
    """Database table definition."""

    __tablename__ = "smap_macip"
    __table_args__ = (
        UniqueConstraint("idx_device", "ip_", "idx_mac"),
        {"mysql_engine": "InnoDB"},
    )

    idx_macip = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    idx_device = Column(
        ForeignKey(Device.idx_device, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    idx_mac = Column(
        ForeignKey(Mac.idx_mac, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    ip_ = Column(VARBINARY(256), nullable=True, default=Null)
    version = Column(BIGINT(unsigned=True), nullable=True, default=Null)
    hostname = Column(VARBINARY(256), nullable=True, default=Null)
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    device = relationship(
        "Device",
        backref=backref(
            "macips",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    mac = relationship(
        "Mac",
        backref=backref(
            "macips",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )


class MacPort(BASE):
    """Database table definition."""

    __tablename__ = "smap_macport"
    __table_args__ = (
        UniqueConstraint("idx_l1interface", "idx_mac"),
        {"mysql_engine": "InnoDB"},
    )

    idx_macport = Column(
        BIGINT(20, unsigned=True), primary_key=True, unique=True
    )
    idx_l1interface = Column(
        ForeignKey(L1Interface.idx_l1interface, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    idx_mac = Column(
        ForeignKey(Mac.idx_mac, ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=1,
        server_default=text("1"),
    )
    enabled = Column(BIT(1), default=1)
    ts_modified = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.now,
    )
    ts_created = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    # Define relationships from child to parent
    # (with backref to plural variable in parent table definition)
    mac = relationship(
        "Mac",
        backref=backref(
            "macports",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )

    l1interfaces = relationship(
        "L1Interface",
        backref=backref(
            "macports",
            cascade="all, delete, delete-orphan",
            passive_deletes=True,
        ),
    )


def create_all_tables():
    """Ensure all tables are created."""
    # Process transaction
    with ENGINE.connect() as connection:
        with Session(bind=connection) as session:
            BASE.metadata.create_all(session.get_bind(), checkfirst=True)
