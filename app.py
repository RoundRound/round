import json

from flask import Flask, render_template, redirect, url_for

from models import *


DEBUG = True
PORT = 8000
HOST = 'localhost'

app = Flask(__name__)

@app.route('/')
def index():
	current_user = Buyer.get(Buyer.id==1)
	stocks = Stock.select().where(Stock.bought==False)
	stocks = [{'id': json.dumps(str(stock.id)) , 'stock': stock } for stock in stocks] # this will be used for adding listings to the homepage
	
	return render_template('index.html', stocks=stocks, current_user=current_user,
		Order=Order, Stock=Stock, fn=fn)

@app.route('/order/<stock_id>/<quantity>')
def order(stock_id=None, quantity=''):
	quantity = int(quantity)

	if quantity != '' and quantity > 0: #validate the quantity given
		stock = Stock.get(Stock.id==stock_id)

		orders = Order.select(fn.sum(Order.quantity)).where(Order.stock==stock.id).scalar() #Get the current number of orders

		if orders == None: #I don't want a TypeError below
			orders = 0

		if quantity <= (stock.minimum_quantity - orders): #verify if quantity is less than or equal to the needed orders
			price = quantity * stock.price #calculate the amount the buyer has to pay
			Order.make_order(buyer=1, stock=stock, quantity=quantity, price=price)

			if stock.minimum_quantity == Order.select(fn.sum(Order.quantity)).where(Order.stock==stock.id).scalar(): #check if the target has been met
				stock.bought = True #update stock and set it to saved 
				stock.save()
				orders = Stock.get(Stock.id==stock_id).orders

				for order in orders:
					order.ready = True
					order.save()

				#replace the old stock with a fresh one with no orders yet
				new_stock = Stock.enter_stock(product=stock.product, first_description=stock.first_description,
					second_description=stock.second_description, third_description=stock.third_description,
					unit=stock.unit, quantity=stock.quantity, minimum_quantity=stock.minimum_quantity,
					brand=stock.brand, supplier=stock.supplier, price=stock.price)

	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)