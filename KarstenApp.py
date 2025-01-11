from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a strong, random key
DATABASE = 'Main.db'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to execute database queries
def execute_query(query, params=(), fetch_one=False, fetch_all=False, fetch_lastrowid=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        if fetch_lastrowid:
            return cursor.lastrowid

@app.route('/debug-session')
def debug_session():
    return str(session)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/restaurant-register', methods=['GET', 'POST'])
def restaurant_register():
    if request.method == 'POST':
        data = {
            'Name': request.form['restaurant_name'],
            'Email': request.form['email'],
            'Password': request.form['password'],
            'Phone_number': request.form['phoneNumber'],
            'Street': request.form['street'],
            'Building_number': request.form['buildingNumber'],
            'Postcode': request.form['postcode'],
            'City': request.form['city'],
            'Image': None,
            'Description': request.form['description']
        }

        image = request.files['image[]']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            data['Image'] = filename  # Save the file path to the database
        else:
            return "Invalid file format", 400
        
        query = """
        INSERT INTO Restaurant (Name, Email, Password, Phone_number, Street, Building_number, Postcode, City, Image, Description)
        VALUES (:Name, :Email, :Password, :Phone_number, :Street, :Building_number, :Postcode, :City, :Image, :Description)
        """

        restaurant_id = execute_query(query, data, fetch_lastrowid=True)
        return redirect(url_for('restaurant_opening_hours', Restaurant_id=restaurant_id))

    return render_template('restaurant_register.html')

@app.route('/restaurant-opening-hours', methods=['GET', 'POST'])
def restaurant_opening_hours():
    restaurant_id = request.args.get('Restaurant_id')  # Match the name with the database

    if request.method == 'POST':
        opening_hours = []
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            opening_hours.append({
                'Restaurant_id': restaurant_id,  # Use the correct field name
                'day': day.capitalize(),
                'open_time': request.form.get(f'{day}_open'),
                'close_time': request.form.get(f'{day}_close'),
                'is_closed': f'{day}_closed' in request.form
            })

        query = """
        INSERT INTO OpeningHours (Restaurant_id, day, open_time, close_time, is_closed)
        VALUES (:Restaurant_id, :day, :open_time, :close_time, :is_closed)
        """
        for entry in opening_hours:
            execute_query(query, entry)

        return redirect(url_for('menu_creation', Restaurant_id=restaurant_id))

    return render_template('restaurant_opening_hours.html', Restaurant_id=restaurant_id)

@app.route('/menu-creation', methods=['GET', 'POST'])
def menu_creation():
    restaurant_id = request.args.get('Restaurant_id')  # Match the name with the database

    if request.method == 'POST':
        restaurant_id = request.form.get('Restaurant_id')  # Fetch from form
        if not restaurant_id:
            return "Restaurant ID is missing", 400

        menu_items = []

        for i in range(len(request.form.getlist('item_name[]'))):
            menu_item = {
                'Restaurant_id': restaurant_id,  # Use the correct field name
                'Item_name': request.form.getlist('item_name[]')[i],
                'Price': request.form.getlist('price[]')[i],
                'Description': request.form.getlist('description[]')[i],
                'Image': None
            }

            if 'image[]' in request.files:
                image_file = request.files.getlist('image[]')[i]
                if image_file and allowed_file(image_file.filename):
                    image_filename = secure_filename(image_file.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    image_file.save(image_path)
                    menu_item['Image'] = image_filename

            menu_items.append(menu_item)

        query = """
        INSERT INTO Menu (Restaurant_id, Item_name, Price, Description, Image)
        VALUES (:Restaurant_id, :Item_name, :Price, :Description, :Image)
        """

        for item in menu_items:
            execute_query(query, item)

        return redirect(url_for('restaurant_signin'))

    return render_template('menu.html', Restaurant_id=restaurant_id)

@app.route('/success')
def success():
    return 'Successful'

@app.route('/customer-register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        data = {
            'Name': request.form['name'],
            'Email': request.form['email'],
            'Password': request.form['password'],  # In production, hash passwords securely
            'Phone_number': request.form['phone_number'],
            'Street': request.form.get('street', None),
            'House_number': request.form.get('house_number', None),
            'Postcode': request.form.get('postcode', None),
            'City': request.form.get('city', None)
        }

        query = """
        INSERT INTO Customer (Name, Email, Password, Phone_number, Street, House_number, Postcode, City)
        VALUES (:Name, :Email, :Password, :Phone_number, :Street, :House_number, :Postcode, :City)
        """
        try:
            execute_query(query, data)
            return redirect(url_for('customer_signin'))
        except sqlite3.IntegrityError:
            return "Email already registered. Try a different email.", 400

    return render_template('customer_register.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/restaurant-signin', methods=['GET', 'POST'])
def restaurant_signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM Restaurant WHERE Email = ? AND Password = ?"
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email, password))
            restaurant = cursor.fetchone()

        if restaurant:
            # Login successful
            return redirect(url_for('success'))  # Redirect to a dashboard or success page
        else:
            # Login failed
            return "Invalid email or password", 401

    return render_template('restaurant_signin.html')

@app.route('/customer-signin', methods=['GET', 'POST'])
def customer_signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM Customer WHERE Email = ? AND Password = ?"
        customer = execute_query(query, (email, password), fetch_one=True)

        if customer:
            session['user_id'] = customer[0]  # Customer ID
            session['user_name'] = customer[1]  # Customer name
            return redirect(url_for('browse_restaurants'))
        else:
            return "Invalid email or password", 401

    return render_template('customer_signin.html')

@app.route('/browse-restaurants', methods=['GET', 'POST'])
def browse_restaurants():
    user_id = session.get('user_id') 

    if not user_id:
        return redirect(url_for('browse_restaurants'))

    # Fetch the customer's credit balance
    credit_query = "SELECT Balance FROM Customer WHERE ID = ?"
    credit_balance_result = execute_query(credit_query, (user_id,), fetch_one=True)

    # Extract balance and format it to two decimal points
    credit_balance = f"{credit_balance_result[0]:.2f}" if credit_balance_result else "0.00"

    search_query = request.form.get('search')  # Get search query from the form (if POST request)

    if search_query:
        # Filter restaurants by name if a search query is provided
        restaurant_query = """
        SELECT ID, Name, Street, Building_number, Postcode, City, Phone_number, Image
        FROM Restaurant
        WHERE Name LIKE ?
        """
        restaurants = execute_query(restaurant_query, ('%' + search_query + '%',), fetch_all=True)
    else:
        # Fetch all restaurants if no search query is provided
        restaurant_query = """
        SELECT ID, Name, Street, Building_number, Postcode, City, Phone_number, Image
        FROM Restaurant
        """
        restaurants = execute_query(restaurant_query, fetch_all=True)

    return render_template('browse_restaurants.html', restaurants=restaurants, credit_balance=credit_balance)

@app.route('/restaurant-details/<int:id>')
def restaurant_details(id):
    user_id = session.get('user_id')  # Get the logged-in user's ID

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT Name, Street, Building_number, Postcode, City, Phone_number, Image FROM Restaurant WHERE ID = ?", (id,))
    restaurant = cursor.fetchone()

    cursor.execute("SELECT Item_name, Price, Description, Image, ID FROM Menu WHERE Restaurant_id = ?", (id,))
    menu_items = cursor.fetchall()

    # Get the count of unique menu items in the cart for the current user
    cart_count = 0
    if user_id:
        cursor.execute("SELECT COUNT(DISTINCT Menu_Item_id) FROM Cart WHERE Customer_id = ?", (user_id,))
        cart_count = cursor.fetchone()[0]

    conn.close()

    return render_template('restaurant_details.html', restaurant=restaurant, menu_items=menu_items, restaurant_id=id, cart_count=cart_count)

# Route to add items to the cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    restaurant_id = request.form.get('restaurant_id')
    menu_item_id = request.form.get('menu_item_id')
    quantity = request.form.get('quantity')
    user_id = session.get('user_id')

    if not all([restaurant_id, menu_item_id, quantity, user_id]):
        return jsonify({"error": "Missing data"}), 400

    # Check if cart contains items from a different restaurant
    query_check = "SELECT Restaurant_id FROM Cart WHERE Customer_id = ? LIMIT 1"
    existing_restaurant = execute_query(query_check, (user_id,), fetch_one=True)

    if existing_restaurant and existing_restaurant[0] != int(restaurant_id):
        # Clear the cart if ordering from a different restaurant
        query_clear = "DELETE FROM Cart WHERE Customer_id = ?"
        execute_query(query_clear, (user_id,))

    # Add item to the cart
    query_add = """
    INSERT INTO Cart (Customer_id, Restaurant_id, Menu_Item_id, Quantity)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(Customer_id, Menu_Item_id)
    DO UPDATE SET Quantity = Cart.Quantity + excluded.Quantity
    """
    execute_query(query_add, (user_id, restaurant_id, menu_item_id, quantity))

    # Calculate the unique number of menu items in the cart
    query_unique_count = "SELECT COUNT(DISTINCT Menu_Item_id) FROM Cart WHERE Customer_id = ?"
    unique_item_count = execute_query(query_unique_count, (user_id,), fetch_one=True)[0]

    return jsonify({"cart_count": unique_item_count})

@app.route('/cart_count', methods=['GET'])
def cart_count():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"cart_count": 0})

    # Query the count of unique items in the cart for the user
    query_count = "SELECT COUNT(DISTINCT Menu_Item_id) FROM Cart WHERE Customer_id = ?"
    count = execute_query(query_count, (user_id,), fetch_one=True)[0]
    return jsonify({"cart_count": count})

@app.route('/cart', methods=['GET'])
def view_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Customer not logged in"}), 401

    # Fetch cart items for the current user
    query_cart_items = """
    SELECT Menu.Item_name, Menu.Price, Cart.Quantity, Cart.Menu_Item_id
    FROM Cart
    JOIN Menu ON Cart.Menu_Item_id = Menu.ID
    WHERE Cart.Customer_id = ?
    """
    cart_items = execute_query(query_cart_items, (user_id,), fetch_all=True)

    if not cart_items:
        return render_template('cart.html', cart_items=[], subtotal=0, delivery_fee=0, total_fee=0)

    # Fetch customer and restaurant details
    customer_query = "SELECT Postcode, City FROM Customer WHERE ID = ?"
    customer_info = execute_query(customer_query, (user_id,), fetch_one=True)

    if not customer_info:
        return jsonify({"error": "Customer not found"}), 404

    customer_postcode, customer_city = customer_info

    restaurant_query = """
    SELECT DISTINCT Restaurant.Postcode, Restaurant.City 
    FROM Restaurant 
    JOIN Cart ON Restaurant.ID = Cart.Restaurant_id 
    WHERE Cart.Customer_id = ?
    """
    restaurant_info = execute_query(restaurant_query, (user_id,), fetch_one=True)

    if not restaurant_info:
        return jsonify({"error": "No restaurant found for this cart"}), 404

    restaurant_postcode, restaurant_city = restaurant_info

    # Determine delivery fee
    if str(customer_postcode).strip() == str(restaurant_postcode).strip() and customer_city.strip().lower() == restaurant_city.strip().lower():
        delivery_fee = 0.00
    elif str(customer_postcode).strip() != str(restaurant_postcode).strip() and customer_city.strip().lower() == restaurant_city.strip().lower():
        delivery_fee = 3.00
    else:
        delivery_fee = 7.00

    # Calculate subtotal
    subtotal = sum(item[1] * item[2] for item in cart_items)
    total_fee = subtotal + delivery_fee

    formatted_cart = [
        {"item_name": item[0], "price": item[1], "quantity": item[2], "menu_item_id": item[3], "total": item[1] * item[2]}
        for item in cart_items
    ]

    return render_template('cart.html', cart_items=formatted_cart, subtotal=subtotal, delivery_fee=delivery_fee, total_fee=total_fee)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Get the logged-in user's ID
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Customer not logged in"}), 401

    # Fetch the remark from the form
    remark = request.form.get('remark', '').strip()

    # Fetch cart items for the current user
    query_cart_items = """
    SELECT Menu_Item_id, Quantity
    FROM Cart
    WHERE Customer_id = ?
    """
    cart_items = execute_query(query_cart_items, (user_id,), fetch_all=True)

    if not cart_items:
        return redirect(url_for('view_cart'))  # Redirect if cart is empty

    # Fetch customer and restaurant details
    customer_query = "SELECT Postcode, City FROM Customer WHERE ID = ?"
    customer_info = execute_query(customer_query, (user_id,), fetch_one=True)

    if not customer_info:
        return jsonify({"error": "Customer not found"}), 404

    customer_postcode, customer_city = customer_info

    restaurant_query = """
    SELECT DISTINCT Restaurant.Postcode, Restaurant.City 
    FROM Restaurant 
    JOIN Cart ON Restaurant.ID = Cart.Restaurant_id 
    WHERE Cart.Customer_id = ?
    """
    restaurant_info = execute_query(restaurant_query, (user_id,), fetch_one=True)

    if not restaurant_info:
        return jsonify({"error": "No restaurant found for this cart"}), 404

    restaurant_postcode, restaurant_city = restaurant_info

    # Determine delivery fee
    if str(customer_postcode).strip() == str(restaurant_postcode).strip() and customer_city.strip().lower() == restaurant_city.strip().lower():
        delivery_fee = 0.00
    elif str(customer_postcode).strip() != str(restaurant_postcode).strip() and customer_city.strip().lower() == restaurant_city.strip().lower():
        delivery_fee = 3.00
    else:
        delivery_fee = 7.00

    # Calculate the total amount
    query_subtotal = """
    SELECT SUM(Menu.Price * Cart.Quantity)
    FROM Cart
    JOIN Menu ON Cart.Menu_Item_id = Menu.ID
    WHERE Cart.Customer_id = ?
    """
    subtotal = execute_query(query_subtotal, (user_id,), fetch_one=True)[0] or 0
    total_amount = subtotal + delivery_fee

    # Fetch the customer's current balance
    query_balance = "SELECT balance FROM Customer WHERE ID = ?"
    balance = execute_query(query_balance, (user_id,), fetch_one=True)[0]

    if balance < total_amount:
        # Insufficient balance
        return jsonify({"error": f"Insufficient funds. Your balance is €{balance:.2f}, but your total is €{total_amount:.2f}."}), 400

    # Deduct total_amount from the customer's balance
    new_balance = balance - total_amount
    update_balance_query = "UPDATE Customer SET balance = ? WHERE ID = ?"
    execute_query(update_balance_query, (new_balance, user_id))

    # Determine the Restaurant_id
    query_restaurant_id = """
    SELECT Menu.Restaurant_id
    FROM Cart
    JOIN Menu ON Cart.Menu_Item_id = Menu.ID
    WHERE Cart.Customer_id = ?
    LIMIT 1
    """
    restaurant_id = execute_query(query_restaurant_id, (user_id,), fetch_one=True)[0]

    # Insert a new order into the Orders table with the remark
    query_insert_order = """
    INSERT INTO Orders (Customer_id, Restaurant_id, Total_Amount, Remark, Order_Status)
    VALUES (?, ?, ?, ?, 'Pending')
    """
    execute_query(query_insert_order, (user_id, restaurant_id, total_amount, remark))

    # Clear the cart for the current user
    query_clear_cart = "DELETE FROM Cart WHERE Customer_id = ?"
    execute_query(query_clear_cart, (user_id,))

    return redirect(url_for('view_orders', success='true'))

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Customer not logged in"}), 401

    menu_item_id = request.form.get('menu_item_id')

    if not menu_item_id:
        return jsonify({"error": "Menu item ID is required"}), 400

    # Check if the cart item belongs to a valid restaurant for the customer
    restaurant_query = """
    SELECT DISTINCT Restaurant.ID
    FROM Restaurant
    JOIN Cart ON Restaurant.ID = Cart.Restaurant_id
    WHERE Cart.Customer_id = ? AND Cart.Menu_Item_id = ?
    """
    restaurant_info = execute_query(restaurant_query, (user_id, menu_item_id), fetch_one=True)

    if not restaurant_info:
        return jsonify({"error": "No restaurant found for this cart"}), 404

    # Proceed to remove item from cart
    delete_query = "DELETE FROM Cart WHERE Customer_id = ? AND Menu_Item_id = ?"
    execute_query(delete_query, (user_id, menu_item_id))

    return render_template('cart.html')

@app.route('/view-orders')
def view_orders():
    # Query to display orders for the current user
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Customer not logged in"}), 401

    query = """
    SELECT Orders.Orders_id, Restaurant.Name, Orders.Total_Amount, Orders.Order_Status, Orders.Order_Date
    FROM Orders
    JOIN Restaurant ON Orders.Restaurant_id = Restaurant.ID 
    WHERE Orders.Customer_id = ?
    """

    orders = execute_query(query, (user_id,), fetch_all=True)
    return render_template('orders.html', orders=orders)

@app.route('/logout')
def logout():
    return redirect(url_for('customer_signin'))

if __name__ == '__main__':
    app.run(debug=True)
