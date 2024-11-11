import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Setup Database
engine = create_engine('sqlite:///iqos_management.db')
Base = sqlalchemy.orm.declarative_base()

# Employee Table
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    department = Column(String, nullable=False)
    borrowings = relationship("Borrowing", back_populates="employee")
    sales = relationship("Sale", back_populates="employee")

# Customer Table
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    borrowings = relationship("Borrowing", back_populates="customer")

# Device Table
class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String)
    status = Column(String, default='available')  # e.g., 'available', 'borrowed'
    borrowings = relationship("Borrowing", back_populates="device")

# Borrowing Table (Peminjaman Device)
class Borrowing(Base):
    __tablename__ = 'borrowings'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date)
    employee = relationship("Employee", back_populates="borrowings")
    customer = relationship("Customer", back_populates="borrowings")
    device = relationship("Device", back_populates="borrowings")

# Sale Table (Penjualan Terea)
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    product_name = Column(String, nullable=False)
    sale_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    employee = relationship("Employee", back_populates="sales")

# Inventory Table (Keluar Masuk Barang)
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity_in = Column(Integer, default=0)
    quantity_out = Column(Integer, default=0)
    current_stock = Column(Integer, default=0)

# Create Tables
Base.metadata.create_all(engine)

# Setup Session
Session = sessionmaker(bind=engine)
session = Session()
