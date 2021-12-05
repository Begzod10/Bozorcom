from app import db, Integer, Column, String


class Region(db.Model):
    __tablename__ = 'Region'
    id = Column(Integer,primary_key=True)
    region_name = Column(String)


class Bazar(db.Model):
    __tablename__ = 'Bazar'
    id = Column(Integer, primary_key=True)
    bazar_name = Column(String)
    cordinates = Column(String)
    address = Column(String)
    owner = Column(String)
    phone = Column(String)
    work_days = Column(String)
    type = Column(String)
    region_id = Column(Integer)


class Shops(db.Model):
    __tablename__ = 'Shops'
    id = Column(Integer, primary_key=True)
    shop_name = Column(String)
    region_id = Column(Integer)
    bazar_id = Column(Integer)
    address = Column(String)


class Products(db.Model):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    region_id = Column(Integer)
    bazar_id = Column(Integer)
    shop_id = Column(Integer)
    cattegory = Column(String)
    amount = Column(String)
    cost = Column(String)


