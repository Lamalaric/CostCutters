#!/usr/bin/env python3
# -- CostCutters Database software --
import time, os, sys, sqlite3, math



class database():
    """This class is designed to create and modify the database for our website"""
    def __init__(self):
        """Initilisation function and initial connect to our db"""
        
        con = sqlite3.connect("PriceList.db")
            # Database connected or created if non existent 
        cur = con.cursor()
            # test cursor (delete later)
        print("Database initialised")
        
    def _append(self, key, item, price, store):
        """Adds an item from a shop to the database"""
        pass
    
    def _generateKey(self, item, store):
        """Item + store = key to detect same items"""
        pass
    
    def conflictDetect(self, key):
        """Return True if item already exists in DB"""
        pass


    def getItem(self, store, item):

        con = sqlite3.connect("PriceList.db")
        cur = con.cursor()

        
        query ="""
            SELECT store, item, price, lat, lon
            FROM prices
            WHERE store = ? AND item = ?
            """


        # Execute the query with parameters
        cur.execute(query, (store, item))

        # Fetch the result
        result = cur.fetchall()

        # Check if we got any result and print it
        if result:
            for row in result:
                print(f"Store: {row[0]}, Item: {row[1]}, Price: {row[2]}PLN, Latitude: {row[3]}, Longitude: {row[4]}")
        else:
            print(f"No data found for {item} in {store}.")

        # Close the connection
        con.close()


    def AddItem(self, store, price, lat, lon):
        insert_query = """
        INSERT INTO prices (store, item, price, lat, lon) VALUES
        ('Lidl', 'Cheese', 4.60, 51.1150, 17.0300);""")
        
    def CreateBlank(self):
        # quickly connect and execute table creation
        con = sqlite3.connect("PriceList.db")
        cur = con.cursor()
        
        insert_query = """
        INSERT INTO prices (store, item, price, lat, lon) VALUES
        ('Zabka', 'Flour', 2.50, 51.1079, 17.0385),
        ('Zabka', 'Sugar', 1.80, 51.1079, 17.0385),
        ('Zabka', 'Eggs', 3.20, 51.1079, 17.0385),
        ('Zabka', 'Milk', 1.50, 51.1079, 17.0385),
        ('Zabka', 'Butter', 4.00, 51.1079, 17.0385),
        ('Zabka', 'Olive Oil', 5.50, 51.1079, 17.0385),
        ('Zabka', 'Salt', 1.00, 51.1079, 17.0385),
        ('Zabka', 'Pepper', 2.10, 51.1079, 17.0385),
        ('Zabka', 'Rice', 3.50, 51.1079, 17.0385),
        ('Zabka', 'Pasta', 2.30, 51.1079, 17.0385),
        ('Zabka', 'Tomatoes', 4.00, 51.1079, 17.0385),
        ('Zabka', 'Garlic', 1.90, 51.1079, 17.0385),
        ('Zabka', 'Onions', 2.20, 51.1079, 17.0385),
        ('Zabka', 'Carrots', 1.60, 51.1079, 17.0385),
        ('Zabka', 'Potatoes', 1.30, 51.1079, 17.0385),
        ('Zabka', 'Chicken Breast', 8.00, 51.1079, 17.0385),
        ('Zabka', 'Beef', 10.50, 51.1079, 17.0385),
        ('Zabka', 'Pork', 7.00, 51.1079, 17.0385),
        ('Zabka', 'Fish', 5.80, 51.1079, 17.0385),
        ('Zabka', 'Cheese', 4.50, 51.1079, 17.0385),
        ('Biedronka', 'Flour', 2.40, 51.1090, 17.0450),
        ('Biedronka', 'Sugar', 1.70, 51.1090, 17.0450),
        ('Biedronka', 'Eggs', 3.00, 51.1090, 17.0450),
        ('Biedronka', 'Milk', 1.40, 51.1090, 17.0450),
        ('Biedronka', 'Butter', 3.80, 51.1090, 17.0450),
        ('Biedronka', 'Olive Oil', 5.20, 51.1090, 17.0450),
        ('Biedronka', 'Salt', 0.90, 51.1090, 17.0450),
        ('Biedronka', 'Pepper', 1.80, 51.1090, 17.0450),
        ('Biedronka', 'Rice', 3.20, 51.1090, 17.0450),
        ('Biedronka', 'Pasta', 2.10, 51.1090, 17.0450),
        ('Biedronka', 'Tomatoes', 3.80, 51.1090, 17.0450),
        ('Biedronka', 'Garlic', 1.70, 51.1090, 17.0450),
        ('Biedronka', 'Onions', 2.00, 51.1090, 17.0450),
        ('Biedronka', 'Carrots', 1.50, 51.1090, 17.0450),
        ('Biedronka', 'Potatoes', 1.20, 51.1090, 17.0450),
        ('Biedronka', 'Chicken Breast', 7.50, 51.1090, 17.0450),
        ('Biedronka', 'Beef', 9.80, 51.1090, 17.0450),
        ('Biedronka', 'Pork', 6.50, 51.1090, 17.0450),
        ('Biedronka', 'Fish', 5.60, 51.1090, 17.0450),
        ('Biedronka', 'Cheese', 4.20, 51.1090, 17.0450),
        ('Lidl', 'Flour', 2.60, 51.1150, 17.0300),
        ('Lidl', 'Sugar', 1.90, 51.1150, 17.0300),
        ('Lidl', 'Eggs', 3.40, 51.1150, 17.0300),
        ('Lidl', 'Milk', 1.60, 51.1150, 17.0300),
        ('Lidl', 'Butter', 4.20, 51.1150, 17.0300),
        ('Lidl', 'Olive Oil', 5.70, 51.1150, 17.0300),
        ('Lidl', 'Salt', 1.10, 51.1150, 17.0300),
        ('Lidl', 'Pepper', 2.00, 51.1150, 17.0300),
        ('Lidl', 'Rice', 3.30, 51.1150, 17.0300),
        ('Lidl', 'Pasta', 2.40, 51.1150, 17.0300),
        ('Lidl', 'Tomatoes', 4.10, 51.1150, 17.0300),
        ('Lidl', 'Garlic', 1.80, 51.1150, 17.0300),
        ('Lidl', 'Onions', 2.10, 51.1150, 17.0300),
        ('Lidl', 'Carrots', 1.70, 51.1150, 17.0300),
        ('Lidl', 'Potatoes', 1.40, 51.1150, 17.0300),
        ('Lidl', 'Chicken Breast', 8.30, 51.1150, 17.0300),
        ('Lidl', 'Beef', 10.20, 51.1150, 17.0300),
        ('Lidl', 'Pork', 7.40, 51.1150, 17.0300),
        ('Lidl', 'Fish', 5.90, 51.1150, 17.0300),
        ('Lidl', 'Cheese', 4.60, 51.1150, 17.0300);
        """

        # Execute the query to insert data
        cur.execute(insert_query)
        con.commit()  # Save the changes to the database

        # Close the connection


         #remove dupes
        CMD = """
        DELETE FROM prices
        WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM prices
        GROUP BY store, item, price, lat, lon);
        """
        cur.execute(CMD)
        con.commit()  # Save the changes to the database
        cur.close()
        con.close()

        

    
        

        

class Measure():
    """This class is designed for measuring distance and cost by travel time"""
    def __init__(self):
        """NSTR"""
        pass
    
    def GetDist(lat1, lon1, lat2, lon2):
        """use the haversine to get P2P distance between two points"""
        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
    
        # Calculate the distance using the spherical law of cosines formula
        distance = math.acos(math.sin(lat1) * math.sin(lat2)
                             + math.cos(lat1) * math.cos(lat2)
                             * math.cos(lon2 - lon1)) * 6371  # Radius of Earth in KM
    
        return distance
        
x = database()
x.CreateBlank()
    
