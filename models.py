import datetime

from peewee import *


DB = SqliteDatabase('peewee.db')

class BaseModel(Model):
	class meta:
		database = DB

class Buyer(BaseModel):
	name = CharField()
	phone = IntegerField()
	email = CharField(unique=True, max_length=140)
	password = CharField(max_length=50)
	buyer_type = CharField(max_length=50, default='free')
	address = TextField()
	longitude = DoubleField(null=True)
	latitude = DoubleField(null=True)
	rating = DoubleField(default=0)
	date_joined = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def create_buyer(cls, name='tatenda', phone=775527640, email='tatendazimba@gmail.com',
		password='tatenda',	address='77 Quorn Avenue, Mount Pleasant, Harare, Zimbabwe'):

		cls.create(name=name, phone=phone, email=email,
			password=password, address=address)

class Supplier(BaseModel):
	name = CharField()
	phone = IntegerField()
	email = CharField(unique=True, max_length=140)
	password = CharField(max_length=50)
	buyer_type = CharField(max_length=50, default='free')
	address = TextField()
	longitude = DoubleField(null=True)
	latitude = DoubleField(null=True)
	rating = DoubleField(default=0)
	date_joined = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def create_supplier(cls, name='GMB', phone=775527640, email='orders@gmb.com',
		password='tatenda',	address='77 Workington Road, Harare, Zimbabwe'):

		cls.create(name=name, phone=phone, email=email,
			password=password, address=address)

class Courier(BaseModel):
	name = CharField()
	phone = IntegerField()
	email = CharField(unique=True, max_length=140)
	password = CharField(max_length=50)
	buyer_type = CharField(max_length=50, default='free')
	address = TextField()
	longitude = DoubleField(null=True)
	latitude = DoubleField(null=True)
	rating = DoubleField(default=0)
	date_joined = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def create_courier(cls, name='Sabot', phone=775527640, email='courier@sabot.com',
		password='tatenda',	address='77 Mutare Road, Harare, Zimbabwe'):

		cls.create(name=name, phone=phone, email=email,
			password=password, address=address)

class Staff(BaseModel):
	name = CharField()
	phone = IntegerField()
	email = CharField(unique=True, max_length=140)
	password = CharField(max_length=50)
	buyer_type = CharField(max_length=50, default='free')
	address = TextField()
	longitude = DoubleField(null=True)
	latitude = DoubleField(null=True)
	role = CharField(max_length=50, default='clerk')
	is_admin = BooleanField(default=False)
	date_joined = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def create_staff(cls, name='tawanda', phone=775527640, email='tawandazimba@gmail.com',
		password='tatenda',	address='77 Quorn Avenue, Mount Pleasant, Harare, Zimbabwe'):

		cls.create(name=name, phone=phone, email=email,
			password=password, address=address)

class Product(BaseModel):
	name = CharField(unique=True)
	date_created = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def create_product(cls, name):
		cls.create(name=name)

class Unit(BaseModel):
	long_name = CharField(max_length=50, unique=True)
	short_name = CharField(max_length=10, unique=True)

	@classmethod
	def create_unit(cls, long_name='kilogrammes', short_name='KG'):
		cls.create(long_name=long_name, short_name=short_name)

class Descriptor(BaseModel):
	description = CharField(max_length=140, unique=True)

	@classmethod
	def create_description(cls, description):
		cls.create(description=description)

class Brand(BaseModel):
	name = CharField(max_length=140, unique=True)
	image = TextField(unique=True)

	@classmethod
	def create_brand(cls, name, image):
		cls.create(name=name, image=image)

class Stock(BaseModel):
	product = ForeignKeyField(Product, related_name='in_stock')
	first_description = ForeignKeyField(Descriptor, related_name='in_stock_first')
	second_description = ForeignKeyField(Product, related_name='in_stock_second', null=True)
	third_description = ForeignKeyField(Product, related_name='in_stock_third', null=True)
	unit = ForeignKeyField(Unit, related_name='in_stock')
	quantity = IntegerField()
	minimum_quantity = IntegerField()
	brand = ForeignKeyField(Brand, related_name='in_stock')
	supplier = ForeignKeyField(Supplier, related_name='products')
	price = DoubleField()
	bought = BooleanField(default=False)

	@classmethod
	def enter_stock(cls, product, first_description, unit, brand, supplier, price,
		second_description=None, third_description=None, minimum_quantity=500, quantity=2):

		cls.create(product=product, first_description=first_description,
			second_description=second_description, third_description=third_description,
			unit=unit, quantity=quantity, minimum_quantity=minimum_quantity, brand=brand,
			supplier=supplier, price=price)

class Order(BaseModel):
	buyer = ForeignKeyField(Buyer, related_name='orders')
	stock = ForeignKeyField(Stock, related_name='orders')
	quantity = IntegerField()
	price = DoubleField()
	payment = DoubleField(default=0)
	ready = BooleanField(default=False)
	fulfilled = BooleanField(default=False)
	date_ordered = DateTimeField(default=datetime.datetime.now)

	@classmethod
	def make_order(cls, buyer, stock, quantity, price):

		cls.create(buyer=buyer, stock=stock, quantity=quantity, price=price)

if __name__ == '__main__':
	DB.create_tables([Buyer, Supplier, Courier, Staff, Product, Unit, Descriptor,
		Brand, Stock, Order], safe=True)
	print('Database successfully created!')