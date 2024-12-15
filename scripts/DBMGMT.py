from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
#region Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Database class
#endregion


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
        create_table_query = """
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT NOT NULL,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        );
        """
        self.execute_query(create_table_query)
    #region -------- GET ITEMS --------
    def get_item(self, store, item):
        """Retrieve an item from the 'prices' table."""
        select_query = """
        SELECT DISTINCT store, item, price, lat, lon
        FROM prices
        WHERE store = ? AND item = ?;
        """
        rows = self.execute_query(select_query, (store, item), fetch=True)

        # Convert each row to a dictionary before returning
        result = [dict(row) for row in rows] if rows else []
        return result

    def get_items(self, items):
        """Retrieve multiple items from the 'prices' table."""
        results = []
        for item in items:
            store = item.get("store")
            item_name = item.get("item")
            result = self.get_item(store, item_name)
            if result:
                results.extend(result)
        return results
    
    def add_recipe(self, username, recipe_name, items, total_price):
        """Adds a recipie to the user recipie table 'UserRecipes' """

        execute_query = '''
        INSERT INTO UserRecipes (username, recipe_name, items, total_price)
        VALUES (?, ?, ?, ?)'''

        self.execute_query(execute_query, (username, recipe_name, items, total_price), fetch=False)

    def retrieve_recipe(self, username, recipe_name):
        """Retrieves a recipe based on username and recipe name."""
        query = '''
        SELECT * FROM UserRecipes 
        WHERE username = ? AND recipe_name = ?
        '''
        result = self.execute_query(query, (username, recipe_name), fetch=True)

        if result:
            recipe = result[0]  # If found, return the first result (since it's unique)
            return {
                "username": recipe["username"],
                "recipe_name": recipe["recipe_name"],
                "items": recipe["items"],
                "total_price": recipe["total_price"]
            }
        else:
            return None  # If no recipe is found
        


    #endregion
#region -------- Init database
# Initialize the database
db = Database()
db.create_blank()
#endregion
#region -------- Flask app routes --------

# Find the cheapest recipie 
@app.route('/find-cheapest', methods=['POST'])
def find_cheapest():
    data = request.json
    items = data.get('items', [])

    results = []
    for item in items:
        store = item.get('store')
        ingredient_name = item.get('ingredient')
        quantity = float(item.get('quantity'))

        # Query the database for the item in the specified store
        items_in_store = db.get_item(store, ingredient_name)  # Assuming this method exists
        if items_in_store:
            # Find the cheapest item for the ingredient in the given store
            cheapest_item = min(items_in_store, key=lambda x: x['price'])

            # Calculate total cost for the requested quantity
            total_cost = cheapest_item['price'] * quantity
            results.append({
                'ingredient': ingredient_name,
                'quantity': f"{quantity} kg",
                'costPerItem': cheapest_item['price'],
                'totalCost': total_cost,
                'store': cheapest_item['store'],
                'travelTime': "10 min"  # Or you could calculate this based on lat/lon
            })
        else:
            results.append({
                'ingredient': ingredient_name,
                'quantity': f"{quantity} kg",
                'costPerItem': "N/A",
                'totalCost': "N/A",
                'store': store,
                'travelTime': "N/A"
            })

    return jsonify({'results': results})

# Get an item
@app.route('/get-item', methods=['POST'])
def get_item():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data, no data received"}), 400  # Return error if no JSON data is found
    
    print("Received data:", data)  # Debugging: Check the received data
    
    try:
        items = data.get("items", [])
        
        if not items:
            return jsonify({"error": "No items provided in the request"}), 400
        
        # Check for missing store or item in each object in the items array
        for item in items:
            if not item.get("store") or not item.get("item"):
                return jsonify({"error": "Store or item missing in one of the items"}), 400
        
        # Get results for all items
        result = db.get_items(items)
        
        if result:
            return jsonify({"data": result}), 200
        else:
            return jsonify({"message": "Items not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# add a recipie 
@app.route('/add-recipe', methods=['POST'])
def add_recipe():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON data, no data received"}), 400
        
        username = data.get("username")
        recipe_name = data.get("recipe_name")
        items = data.get("items")
        total_price = data.get("total_price")

        if not username or not recipe_name or not items or not total_price:
            return jsonify({"error": "Missing required fields: username, recipe_name, items, or total_price"}), 400
        
        # Add recipe to the database
        db.add_recipe(username, recipe_name, items, total_price)
        return jsonify({"message": "Recipe added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# retrieve a recipe
@app.route('/retrieve-recipe', methods=['GET'])
def retrieve_recipe():
    try:
        # Extract query parameters
        username = request.args.get("username")
        recipe_name = request.args.get("recipe_name")

        if not username or not recipe_name:
            return jsonify({"error": "Missing required query parameters: username or recipe_name"}), 400
        
        # Retrieve the recipe from the database
        recipe = db.retrieve_recipe(username, recipe_name)

        if recipe:
            return jsonify({"recipe": recipe}), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#endregion
#region -------- Run Program --------
if __name__ == "__main__":
    app.run(debug=True)
#endregion
