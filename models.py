from sqlalchemy import (create_engine, Column, 
                        Integer, String, Date)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class Product(Base):
    __tablename__ = "Inventory"
    
    id = Column(Integer, primary_key=True)
    product_name = Column('product_name', String)
    product_price = Column('product_price', Integer)
    product_quantity = Column('product_quantity', Integer)
    date_updated = Column('date_updated', Date)
    
    def __repr__(self):
        return f'''product_name: {self.product_name}, 
                   \rproduct_price: {self.product_price}, 
                   \rproduct_quantity: {self.product_quantity}, 
                   \rdate_updated: {self.date_updated}'''
