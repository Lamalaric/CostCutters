from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import math
#region Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Database class
#endregion


class Database:
    def __init__(self):
        """Initialization function and initial connection to the database."""
        self.db_name = "PriceList.db"
        self.MaxDistance = 0
        self.userLat = 0
        self.userLon = 0
    
    def set_location(self, lat, lon, maxDistance):
        """Set users location for distance calc which isn't needed as the stores are local"""
        self.userLat = lat
        self.userLon = lon
        self.MaxDistance = maxDistance
        print("users location has been set")
        print(self.userLat)
        print(self.userLon)
        print("max distance")
        print(self.MaxDistance)

    def get_distance(self, lat1, lon1):
        """Returns the distance between lat lon in db and users loc"""
        R = 6371.0  # Radius of the Earth in km
        
        # Convert deg to rad
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(self.userLat), math.radians(self.userLon)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Return distance as int
        print(int(R * c))
        return int(R * c)  # Distance in kilometers in int

        

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
    
    def get_all_recipes(self):
        """Retrieve all recipes with name and total cost."""
        query = "SELECT recipe_name, total_price, username FROM UserRecipes"
        rows = self.execute_query(query, fetch=True)
        return [{"recipe_name": row["recipe_name"], "total_cost": row["total_price"], "username": row["username"]} for row in rows]

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
    def add_recipe(self, username, recipe_name, items_json, total_price):
        """Add a new recipe to the database."""
        insert_query = """
        INSERT INTO recipes (username, recipe_name, items, total_price)
        VALUES (?, ?, ?, ?)
        """
        self.execute_query(insert_query, (username, recipe_name, items_json, total_price))

    
    def get_items(self, items):
        """Retrieve multiple items from the 'prices' table."""
        results = []
        for item in items:
            store = item.get("store")
            item_name = item.get("item")
            
            # Corrected to use execute_query to retrieve items directly without calling get_item()
            if store:
                # Query for a specific store
                select_query = """
                SELECT * FROM prices
                WHERE store = ? AND item = ?;
                """
                result = self.execute_query(select_query, (store, item_name), fetch=True)
            else:
                # Query for all stores if no store is provided
                select_query = """
                SELECT * FROM prices
                WHERE item = ?;
                """
                result = self.execute_query(select_query, (item_name,), fetch=True)
            
            if result:
                results.extend(result)  # Add the found items to the results
        
        return results
    
    def add_recipe(self, username, recipe_name, items, total_price):
        """Adds a recipie to the user recipie table 'UserRecipes' """

        execute_query = '''
        INSERT INTO UserRecipes (username, recipe_name, items, total_price)
        VALUES (?, ?, ?, ?)'''

        self.execute_query(execute_query, (username, recipe_name, items, total_price), fetch=False)

    def retrieve_recipe(self, username, recipe_name): # add distance filter
        """Retrieves a recipe based on username and recipe name."""
        query = '''
        SELECT * FROM UserRecipes 
        WHERE username = ? AND recipe_name = ?
        '''
        result = self.execute_query(query, (username, recipe_name), fetch=True)

        if result:
            recipe = result[0]  # If found, return the first result (since it's unique)

            # Deserialize the 'items' field if it's a JSON string
            items = json.loads(recipe["items"]) if isinstance(recipe["items"], str) else recipe["items"]

            return {
                "username": recipe["username"],
                "recipe_name": recipe["recipe_name"],
                "items": items,  # Make sure items is a list
                "total_price": recipe["total_price"]
            }
        else:
            return None  # If no recipe is found
    def find_cheapest(self, store, ingredient_name):
        """Finds the cheapest price for an ingredient at a given store."""
        # Assuming db.get_items works and returns a list of items matching the store and ingredient_name
        items_in_store = db.get_items([{"store": store, "item": ingredient_name}])  # Corrected method usage

        if not items_in_store:
            return {"error": "No items found for the given store and ingredient."}, 404
        
        # Find the item with the lowest price
        cheapest_item = min(items_in_store, key=lambda x: x['price'])
        print(self.get_distance(cheapest_item["lat"], cheapest_item["lon"]))
        return {
            "store": cheapest_item["store"],
            "ingredient": cheapest_item["ingredient"],
            "price": cheapest_item["price"],
            "lat": cheapest_item["lat"],
            "lon": cheapest_item["lon"]
    }
        


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
        ingredient_name = item.get('ingredient')
        quantity = float(item.get('quantity'))
        store = item.get('store')  # Store can be None or missing

        items_in_store = []
        
        # If store is provided, query that specific store for the ingredient
        if store:
            items_in_store = db.get_items([{"store": store, "item": ingredient_name}])
        else:
            # If no store is provided, query all stores for the ingredient
            select_query = """
            SELECT DISTINCT store, item, price, lat, lon
            FROM prices
            WHERE item = ?;
            """
            rows = db.execute_query(select_query, (ingredient_name,), fetch=True)
            items_in_store = [dict(row) for row in rows] if rows else []

        if items_in_store:
            # Find the cheapest item in the available stores (if multiple stores)
            cheapest_item = min(items_in_store, key=lambda x: x['price'])

            # Calculate total cost for the requested quantity
            total_cost = cheapest_item['price'] * quantity

            results.append({
                'ingredient': ingredient_name,
                'quantity': f"{quantity} kg",
                'costPerItem': cheapest_item['price'],
                'totalCost': total_cost,
                'store': cheapest_item['store'],
                'travelTime': db.get_distance(cheapest_item['lat'],cheapest_item['lon'])
            })
        else:
            # If no item found, append a result indicating the item is unavailable
            results.append({
                'ingredient': ingredient_name,
                'quantity': f"{quantity} kg",
                'costPerItem': "N/A",
                'totalCost': "N/A",
                'store': store if store else "N/A",  # If store is provided, show it; otherwise show N/A
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


        # -- UNTESTED CODE IF THERE IS A BUG THIS IS IT
        # warning
        # warning
        # warning
        # warning
        # warning
        # warning
        # warning
        if (get_distance(self, lat1, lon1 <= db.MaxDistance):
            return jsonify({"message": "Out of distance"}), 400
        else:
            pass
        
        if not items:
            return jsonify({"error": "No items provided in the request"}), 400
        # warning
        # warning
        # warning
        # warning
        # warning
        # warning
        # warning
        # warning
        
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
        
        # Serialize the items list to a JSON string
        items_json = json.dumps(items)

        # Add recipe to the database (you need to adjust the DB method to handle this)
        db.add_recipe(username, recipe_name, items_json, total_price)
        return jsonify({"message": "Recipe added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# retrieve a recipe
@app.route('/retrieve-recipe', methods=['POST'])
def retrieve_recipe():
    try:
        # Extract the JSON data from the request body
        data = request.json
        username = data.get("username")
        recipe_name = data.get("recipe_name")
        #distance = data.get("distance")

        if not username or not recipe_name:
            return jsonify({"error": "Missing required fields: username or recipe_name"}), 400
        
        # Retrieve the recipe from the database
        recipe = db.retrieve_recipe(username, recipe_name)

        if recipe:
            return jsonify({"recipe": recipe}), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-all-recipes', methods=['GET'])
def get_all_recipes():
    try:
        # Fetch all recipes
        recipes = db.get_all_recipes()

        if recipes:
            return jsonify({"recipes": recipes}), 200
        else:
            return jsonify({"message": "No recipes found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mouse-data', methods=['POST'])
def save_mouse_data():
    try:
        # Get the mouse data from the request
        data = request.json

        # Save the data to a file (or database)
        with open("mouse_data.json", "a") as file:
            file.write(json.dumps(data) + "\n")

        return jsonify({"message": "Mouse data saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/set-user-location', methods=['POST'])
def set_user_location():
    try:
        # Get the location data from the request JSON
        data = request.json
        user_lat = data.get('lat')
        user_lon = data.get('lon')
        maxDistance = data.get('maxDistance')

        if user_lat is None or user_lon is None:
            return jsonify({"error": "Missing latitude or longitude"}), 400

        # Set the user's location using the Database class
        db.set_location(user_lat, user_lon, maxDistance)

        return jsonify({"message": "User location, max distance set successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/create-user-report', methods=['POST'])
def create_user_report():
    try:
        data = request.json  # Get JSON data from the request
        
        # Extract variables from the JSON body
        variable1 = data.get('variable1')
        variable2 = data.get('variable2')
        variable3 = data.get('variable3')

        # Create the content for the file
        report_content = f"Variable 1: {variable1}\nVariable 2: {variable2}\nVariable 3: {variable3}\n"

        # Write content to a file on the server
        with open('userreports.txt', 'w') as file:
            file.write(report_content)

        return jsonify({"message": "File created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#endregion
#region -------- Run Program --------
if __name__ == "__main__":
    app.run(debug=True)
#endregion
