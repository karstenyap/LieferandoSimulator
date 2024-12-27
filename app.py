from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename
connection = sqlite3.connect('Main.db', check_same_thread=False)


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/restaurant-register', methods=['GET', 'POST'])
def restaurant_register():
    if request.method == 'POST':
        # Save form data
        data = {
            'Name': request.form['restaurant_name'],
            'Email': request.form['email'],
            'Password': request.form['password'],
            'Phone_number': request.form['phone'],
            'Street': request.form['street'],
            'Building_number': request.form['building_number'],
            'Postcode': request.form['postcode'],
            'City': request.form['city']
        }
        
        # Handle image upload
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            data['Image'] = filepath  # Save the file path to the database
        else:
            return "Invalid file format", 400

        # Insert into database
        query = """
        INSERT INTO Restaurant (Name, Email, Password, Phone_number, Street, Building_number, Postcode, City, Image)
        VALUES (:Name, :Email, :Password, :Phone_number, :Street, :Building_number, :Postcode, :City, :Image)
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

        # Query the Restaurant table
        query = "SELECT ID, Name FROM Restaurant WHERE Email = ? AND Password = ?"
        restaurant = execute_query(query, (email, password), fetch_one=True)

        if restaurant:
            # Login successful, store restaurant details in session
            session['restaurant_id'] = restaurant[0]  # Store the restaurant ID in session
            session['restaurant_name'] = restaurant[1]  # Store the restaurant name in session
            return redirect(url_for('menu_or_order', Restaurant_id=restaurant[0]))
        else:
            # Login failed
            error_message = "Invalid email or password"
            return render_template('restaurant_signin.html', error=error_message)

    return render_template('restaurant_signin.html')


@app.route('/menu_or_order')
def menu_or_order():
    restaurant_id = request.args.get('Restaurant_id') or session.get('restaurant_id')

    if not restaurant_id:
        return redirect(url_for('restaurant_signin'))

    # Fetch restaurant details or menu items using restaurant_id if needed
    return render_template('menu_or_order.html', Restaurant_id=restaurant_id)

@app.route('/menu_management', methods=['GET', 'POST'])
def menu_management():
    restaurant_id = request.args.get('Restaurant_id') or session.get('restaurant_id')

    if not restaurant_id:
        return redirect(url_for('restaurant_signin'))

    # Fetch existing menu items for the restaurant
    query = "SELECT ID, Item_name, Price, Description, Image FROM Menu WHERE Restaurant_id = ?"
    menu_items = execute_query(query, (restaurant_id,), fetch_all=True)

    return render_template('menu_management.html', menu_items=menu_items, Restaurant_id=restaurant_id)


@app.route('/edit_menu_item/<int:item_id>', methods=['GET', 'POST'])
def edit_menu_item(item_id):
    if request.method == 'POST':
        # Update menu item
        data = {
            'Item_name': request.form['item_name'],
            'Price': request.form['price'],
            'Description': request.form['description'],
            'Image': None
        }

        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)
                data['Image'] = filepath  # Update image path in the database

        # Update query
        query = """
        UPDATE Menu 
        SET Item_name = :Item_name, Price = :Price, Description = :Description, Image = :Image
        WHERE ID = :item_id
        """
        data['item_id'] = item_id
        execute_query(query, data)
        return redirect(url_for('menu_or_order'))

    # Fetch menu item details for editing
    query = "SELECT ID, Item_name, Price, Description, Image FROM Menu WHERE ID = ?"
    menu_item = execute_query(query, (item_id,), fetch_one=True)

    return render_template('edit_menu_item.html', menu_item=menu_item)

@app.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    restaurant_id = session.get('restaurant_id')

    if not restaurant_id:
        return redirect(url_for('restaurant_signin'))

    if request.method == 'POST':
        # Add new menu item
        data = {
            'Restaurant_id': restaurant_id,
            'Item_name': request.form['item_name'],
            'Price': request.form['price'],
            'Description': request.form['description'],
            'Image': None
        }

        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)
                data['Image'] = filepath  # Save image path to the database

        # Insert query
        query = """
        INSERT INTO Menu (Restaurant_id, Item_name, Price, Description, Image)
        VALUES (:Restaurant_id, :Item_name, :Price, :Description, :Image)
        """
        execute_query(query, data)
        return redirect(url_for('menu_or_order'))

    return render_template('add_menu_item.html')


@app.route('/customer-signin', methods=['GET', 'POST'])
def customer_signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM Customer WHERE Email = ? AND Password = ?"
        customer = execute_query(query, (email, password), fetch_one=True)

        if customer:
            # Login successful
            session['user_id'] = customer[0]  # Store the customer ID in session
            session['user_name'] = customer[1]  # Store the customer name in session
            return redirect(url_for('customer_dashboard'))
        else:
            # Login failed
            return "Invalid email or password", 401

    return render_template('customer_signin.html')

@app.route('/customer-dashboard')
def customer_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        query = "SELECT Name FROM Customer WHERE ID = ?"
        customer_name = execute_query(query, (user_id,), fetch_one=True)

        if customer_name:
            return render_template('customer_dashboard.html', user_name=customer_name[0])
        else:
            return "User not found", 404
    else:
        return redirect(url_for('customer_signin'))

@app.route('/browse-restaurants')
def browse_restaurants():
    return "Browse Restaurants Page"

@app.route('/view-orders')
def view_orders():
    return "Orders Page"

@app.route('/logout')
def logout():
    return redirect(url_for('customer_signin'))


if __name__ == '__main__':
    app.run(debug=True)
