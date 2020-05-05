from flask import Flask, redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'


logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

navbar = """
         <a href='/'>Home</a> |
         <a href='/login'>Login</a> |
         <a href='/products'>Products</a> |
         <a href='/productdetails'>Product Details</a>
         """

# Customer Pages
@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/register')
def register():
    pagecontent = 'Register Page. Place Regsitration Page contents here.'
    return navbar+pagecontent

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')
# insert 'register' button

@app.route('/auth', methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)
# insert 'search product' function
# insert 'add to cart' function/buttons

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code','')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code, product=product)
# insert 'add to cart' function

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')


# Manager Pages
@app.route('/addproduct')
def addproduct():
    return 'Add Product Page. Place Add Product Page contents here.'

@app.route('/salestransactions')
def salestransactions():
    return 'Sales Transactions Page. Place Sales Transactions Page contents here.'
