from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json  # For handling the list of items in JSON format
import logging


# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database class
class Database:
    def __init__(self):
        """Initialization function and initial connection to the database."""
        self.db_name = "PriceList.db"

    def execute_query(self, query, params=None, fetch=False):
        """Utility to execute a query with or without parameters."""
        con = sqlite3.connect(self.db_name)
        con.row_factory = sqlite3.Row  # This will allow access to rows as dictionaries
        cur = con.cursor()
        result = None
        try:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if fetch:
                result = cur.fetchall()
            con.commit()
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cur.close()
            con.close()
        return result

    def create_blank(self):
        """Create and populate the 'prices' table."""
        create_prices_table_query = """
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        );
        """
        self.execute_query(create_prices_table_query)
        
        # Create the 'UserRecipes' table
        create_user_recipes_table_query = """
        CREATE TABLE IF NOT EXISTS UserRecipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recipe_name TEXT NOT NULL,
            items TEXT NOT NULL,  -- List of items as a JSON string
            total_price REAL NOT NULL
        );
        """
        self.execute_query(create_user_recipes_table_query)

    def add_recipe(self, username, recipe_name, items, total_price):
        """Add a recipe to the 'UserRecipes' table."""
        # Convert the items list to a JSON string
        items_json = json.dumps(items)
        
        insert_query = """
        INSERT INTO UserRecipes (username, recipe_name, items, total_price)
        VALUES (?, ?, ?, ?);
        """
        self.execute_query(insert_query, (username, recipe_name, items_json, total_price))

    def get_user_recipes(self, username):
        """Retrieve all recipes for a given user from the 'UserRecipes' table."""
        select_query = """
        SELECT id, username, recipe_name, items, total_price
        FROM UserRecipes
        WHERE username = ?;
        """
        rows = self.execute_query(select_query, (username,), fetch=True)

        # Convert each row to a dictionary and decode the items JSON string
        result = []
        for row in rows:
            recipe = dict(row)
            recipe['items'] = json.loads(recipe['items'])  # Decode the items from JSON string to list
            result.append(recipe)

        return result

# Initialize the database
db = Database()
db.create_blank()

# Flask Routes


@app.route('/add-recipe', methods=['POST'])
def add_recipe():
    try:
        data = request.json
        logging.info(f"Received data: {data}")

        username = data.get("username")
        recipe_name = data.get("recipe_name")
        items = data.get("items")
        total_price = data.get("total_price")

        if not username or not recipe_name or not items or total_price is None:
            logging.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Check the data types
        if not isinstance(username, str):
            logging.error("Invalid username type")
            return jsonify({"error": "Invalid username type"}), 400

        if not isinstance(recipe_name, str):
            logging.error("Invalid recipe_name type")
            return jsonify({"error": "Invalid recipe_name type"}), 400

        if not isinstance(items, list):
            logging.error("Items must be a list")
            return jsonify({"error": "Items must be a list"}), 400

        if not isinstance(total_price, (float, int)):
            logging.error("Total price must be a number")
            return jsonify({"error": "Total price must be a number"}), 400

        # Check each item in the list
        for item in items:
            if not isinstance(item, dict):
                logging.error("Each item must be a dictionary")
                return jsonify({"error": "Each item must be a dictionary"}), 400

            if not all(k in item for k in ["store", "ingredient", "quantity"]):
                logging.error("Each item must contain 'store', 'ingredient', and 'quantity'")
                return jsonify({"error": "Missing keys in item"}), 400

        # Simulate saving to DB
        logging.info(f"Saving recipe for user: {username}")
        db.add_recipe(username, recipe_name, items, total_price)

        return jsonify({"message": "Recipe added successfully!"}), 201

    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return jsonify({"error": str(e)}), 400


@app.route('/get-recipes', methods=['POST'])
def get_recipes():
    data = request.json
    try:
        username = data.get("username")

        if not username:
            return jsonify({"error": "Username is required"}), 400

        recipes = db.get_user_recipes(username)

        if recipes:
            return jsonify({"recipes": recipes}), 200
        else:
            return jsonify({"message": "No recipes found for this user"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
