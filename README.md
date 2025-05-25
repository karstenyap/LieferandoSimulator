Date: 15/11/2024

Introduction Language: Java Script, HTML, CSS (Frontend) Framework: Flask (Backend) Database: SQLite (Backend)

UI Mockups: Use tools like Balsamiq to create wireframes for seven specific scenarios (account creation, restaurant browsing, order assembly, order summary, order history, item creation, and order management for restaurants). Make sure the design reflects the user flow and incorporates elements like input fields, buttons, and layout needed for each scenario. Website should run in real time.

Food Delivery Service: Use a lot of stickers

New restaurant can be added to the website

1.Manage menus, oder history, order put in the cart 2.when we paid, automatically receipt will be sent to the restaurant and customers through email for confirmation order

Payment Method: Each customer has 100 €, deduct everytime they buy something Each restaurants has 0€ profit 15% to the site and others to restaurants, so meaning if te product is 20 net, then on the website it should 35 because 15 for the site 20 to the restaurant.

Yap Wei Jun Karsten: 3147162 Vasundhra Vythilingam: 3191494 Sylvia Osavbee Imade: 3133283

Concept paper on 2. December 2024

Here’s an example of how you could write a concept paper for the Lieferspatz project, specifically based on using Java with Node.js and SQLite. The paper should cover the required sections, including software architecture and UI mockups.

Concept Paper for Lieferspatz
Group Information
Group Name: Team Alpha
Members:
Alice Smith (Matriculation No: 123456)
Bob Johnson (Matriculation No: 789012)
Charlie Brown (Matriculation No: 345678)
Diana Ross (Matriculation No: 901234)
1. Software Architecture
Overview
The project involves implementing a simplified food and beverage delivery platform, Lieferspatz. The platform will allow restaurants to manage their menus and receive orders, while customers can browse restaurants, place orders, and track them.

We will use a three-layer architecture:

Frontend: Handled by Node.js (with Express.js) to serve HTML/CSS/JavaScript pages and manage user interactions.
Backend: Developed in Java using the Spark framework to implement RESTful APIs for business logic and data management.
Database: SQLite will store all persistent data (e.g., user accounts, restaurant menus, orders).
Tools and Technologies
Component	Technology	Purpose
Frontend Server	Node.js + Express	Serves the HTML pages, handles client-side routing, forwards requests to the backend.
Backend Server	Spark Framework	Implements the core business logic (e.g., account management, order processing).
Database	SQLite	Stores user, restaurant, menu, and order data.
Frontend Frameworks	HTML/CSS/Bootstrap	Provides structure and style to the web pages.
Inter-Server Communication	Axios (Node.js)	Facilitates communication between Node.js and the Java backend.
Key Functionalities
Frontend (Node.js + HTML/CSS/Bootstrap):
Serve static pages for:
Registration/Login for customers and restaurants.
Viewing nearby restaurants and their menus.
Viewing and managing the cart.
Forward user data (e.g., registration forms) to the Java backend via HTTP requests.
Backend (Java with Spark Framework):
Handle API endpoints for:
User and restaurant account creation, login, and management.
CRUD operations for restaurant menus and items.
Managing orders and updating order statuses.
Communicate with the SQLite database to store and retrieve data.
Database (SQLite):
Store the following entities:
Users: Customers and restaurants with their details.
Restaurants: Menu items, opening hours, delivery areas (postcodes).
Orders: Status, items, prices, and customer details.
Wallets: Simplified virtual wallets to handle payments.
2. User Interface Mockups
Below are wireframes for the primary UI components. The mockups were created using Balsamiq.

2.1 Customer Views
1. Account Creation
A simple form where customers can enter:

Name
Email
Address (including postcode)
Password
2. Restaurant Overview
Displays a list of open restaurants that deliver to the customer’s postcode. Each restaurant includes:

Name
Short description
Delivery time estimate
3. Menu View
Allows customers to select items from a restaurant’s menu.
Displays item name, description, price, and quantity selection.
4. Shopping Cart
Shows the selected items, their quantities, and the total price.
Option to add notes for special instructions (e.g., "No onions").
5. Order History
Displays all previous orders, sorted by date, with status (completed, canceled).
2.2 Restaurant Views
1. Account Creation
A form for restaurants to register with:

Name
Address
Delivery area (list of postcodes)
Password
2. Menu Management
Interface to add, edit, or remove items, with fields for:
Name, description, price, and optional image.
3. Order Management
Displays a list of ongoing orders.
Buttons to mark orders as:
"In Preparation"
"Completed"
"Rejected"
3. Implementation Plan
Phase 1: Database Setup
Design and populate SQLite database with sample data:
10 restaurants, each with 10 items.
5 customers, each with 2 completed orders.
Define the schema to support relationships between users, orders, and items.
Phase 2: Backend Development
Use Spark Java to implement RESTful APIs:
/register (POST): Add a new user or restaurant.
/login (POST): Authenticate users.
/restaurants (GET): Fetch open restaurants for a given postcode.
/menu/:restaurantId (GET): Fetch menu items for a specific restaurant.
/orders (POST): Place an order.
/orders/:orderId (PATCH): Update an order’s status.
Phase 3: Frontend Development
Use Node.js with Express to serve static HTML/CSS files.
Integrate Bootstrap for responsive UI.
Forward requests to the Java backend using Axios.
Phase 4: Testing
Test the API endpoints with Postman.
Validate database interactions with sample data.
Perform user acceptance testing for the frontend.
Phase 5: Deployment
Run the application locally during the oral exam using:
Java backend on port 4567.
Node.js frontend on port 3000.
4. Anticipated Challenges and Solutions
Challenge 1: Communication Between Node.js and Java
Solution: Use Axios in Node.js to send HTTP requests to the Java backend.
Challenge 2: Database Schema Design
Solution: Use an iterative approach to design the schema and validate with sample data early in the project.
Challenge 3: Real-Time Notifications
Solution: Use polling to fetch order updates from the backend in the frontend.
This concept paper outlines our approach to successfully completing the Lieferspatz project, ensuring clarity, consistency, and collaboration within the team.

