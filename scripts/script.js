// PROGRESS BAR
//#region ignore 
window.onload = () => {
	// Ecouteur d'évènement sur scroll
	window.addEventListener("scroll", () => {
		// Calcul de la hauteur "utile" du document
		let hauteur = document.documentElement.scrollHeight - window.innerHeight
		// Récupération de la position verticale
		let position = window.scrollY
		// Récupération de la largeur de la fenêtre
		let largeur = document.documentElement.clientWidth
		// Calcul de la largeur de la barre
		let barre = position / hauteur * largeur
		// Modification du CSS de la barre
		document.getElementById("progress").style.width = barre+"px"


        // PLEASE FIX LATER
        sendPositionToPython(navigator.geolocation.getCurrentPosition(showPosition));
	})
}
//#endregion

//Wait for the full DOM to be loaded...
document.addEventListener('DOMContentLoaded', function () {
	const menuIcon = document.getElementById('menu-icon');
	const navLinks = document.getElementById('nav-links');


	//#region BURGER MENU
	if (menuIcon && navLinks) {
		menuIcon.addEventListener('click', function () {
			navLinks.classList.toggle('active');
		});
	}
	//#endregion

	//Click on "Find" to display the next step table
	document.getElementById('find-button').addEventListener('click', function () {
		const resultsContainer = document.getElementById('results-container');
		resultsContainer.classList.remove('hidden'); // Show the results table
	});
	//Add a row in the find recipe table
	// Add event listener to the "add-row-button" button
	document.getElementById("add-row-button").addEventListener("click", function() {
		const ingredientRows = document.getElementById("ingredient-rows");
		
		// Create a new row with the same structure as the previous rows
		const newRow = document.createElement("tr");

		const storeCell = document.createElement("td");
		storeCell.innerHTML = '<input type="text" placeholder="Store">';
		
		const ingredientCell = document.createElement("td");
		ingredientCell.innerHTML = '<input type="text" placeholder="Ingredient">';
		
		const quantityCell = document.createElement("td");
		quantityCell.innerHTML = '<input type="number" placeholder="Quantity">';
		
		newRow.appendChild(storeCell);
		newRow.appendChild(ingredientCell);
		newRow.appendChild(quantityCell);
		
		// Append the new row to the table body
		ingredientRows.appendChild(newRow);
	});


	//Show the table of details of a recipe
	document.querySelectorAll('.recipe-link').forEach(link => {
		link.addEventListener('click', function (event) {
			event.preventDefault(); // Empêche la navigation vers une autre page

			// Obtenir le nom de la recette pour laquelle les détails doivent être affichés
			const recipeName = this.getAttribute('data-recipe');

			// Logique pour récupérer les informations spécifiques à la recette (ici des données statiques pour l'exemple)
			const recipes = {
				pierogi: {
					ingredients: [
						{ name: 'Flour', quantity: '500g', cost: '2 PLN', totalCost: '4 PLN', store: 'Zabka', travelTime: '10 min' },
						{ name: 'Water', quantity: '1L', cost: '1 PLN', totalCost: '1 PLN', store: 'Biedronka', travelTime: '5 min' }
					],
					totalCost: '500 PLN'
				},
				foobar: {
					ingredients: [
						{ name: 'FOOOO', quantity: '500g', cost: '2 PLN', totalCost: '4 PLN', store: 'Zabka', travelTime: '10 min' },
						{ name: 'BAAAR', quantity: '1L', cost: '1 PLN', totalCost: '1 PLN', store: 'Biedronka', travelTime: '5 min' }
					],
					totalCost: '500 PLN'
				}
			};

			// Obtenir les détails de la recette choisie
			const recipe = recipes[recipeName];
			if (!recipe) return;

			// Mettre à jour le tableau des ingrédients avec les détails de la recette
			const ingredientsList = document.getElementById('ingredients-list');
			ingredientsList.innerHTML = ''; // Vider les lignes existantes

			recipe.ingredients.forEach(ingredient => {
				const row = document.createElement('tr');
				row.innerHTML = `
                <td>${ingredient.name}</td>
                <td>${ingredient.quantity}</td>
                <td>${ingredient.cost}</td>
                <td>${ingredient.totalCost}</td>
                <td>${ingredient.store}</td>
                <td>${ingredient.travelTime}</td>`
            ;
				ingredientsList.appendChild(row);
			});

			// Afficher le coût total
			const totalCostElement = document.querySelector('.total-cost');
			totalCostElement.textContent = recipe.totalCost;

			// Afficher le bloc des détails de la recette
			document.getElementById('recipe-details').classList.remove('hidden');
		});
	});











//region save recipe 
document.getElementById("save-button").addEventListener("click", function () {
    // Prompt the user for their username
    const username = prompt("Please enter your username:");

    // If the username is empty or canceled, alert the user and stop the process
    if (!username) {
        alert("Username is required. Please enter a username.");
        return;
    }

	const recipeName = prompt("Please enter your recipe name:");

    // If the username is empty or canceled, alert the user and stop the process
    if (!recipeName) {
        alert("recipe name is required. Please enter a name.");
        return;
    }

    const rows = document.querySelectorAll("#ingredient-rows tr");
    let items = [];

    // Collect ingredient, store, and quantity values from each row
    rows.forEach(row => {
        const inputs = row.querySelectorAll("input");
        const store = inputs[0].value.trim();  // Store can be empty
        const ingredient = inputs[1].value.trim();
        const quantity = parseFloat(inputs[2].value.trim());

        // Check if ingredient and quantity are valid
        if (ingredient && !isNaN(quantity)) {
            items.push({
                store: store,  // Store can be empty
                ingredient: ingredient,
                quantity: quantity
            });
        } else {
            console.error("Invalid row data:", { store, ingredient, quantity });
            // Optionally, alert the user about missing ingredient or invalid quantity
            alert(`Invalid data in row: ${ingredient} - Make sure quantity is a number.`);
        }
    });

    if (items.length === 0) {
        alert("No valid ingredients to save.");
        return;
    }

    // Calculate total price (example: assuming $2.5 per unit)
    const totalPrice = items.reduce((total, item) => total + item.quantity * 2.5, 0).toFixed(2);

    const data = {
        username: username, // Use the entered username
        recipe_name: recipeName, // Replace with a user-provided recipe name
        items: items,
        total_price: totalPrice
    };

    console.log("Data being sent to backend:", data);

    fetch('http://127.0.0.1:5000/add-recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();
    })
    .then(result => {
        console.log(result.message);
        alert("Recipe saved successfully!");
    })
    .catch(error => {
        console.error("Error saving recipe:", error);
        alert("Failed to save recipe. Check console for details.");
    });
});
//#endregion














//#region Find Ingredients 
async function submitForm() {
    const ingredients = [];
    const rows = document.querySelectorAll("#ingredient-rows tr");

    // Collect ingredient, store, and quantity values from each row
    for (const row of rows) {
        const inputs = row.querySelectorAll("input");

        if (inputs.length >= 2) {  // Ensure there are at least 2 inputs (store and ingredient, store is optional)
            const store = inputs[0] ? inputs[0].value.trim() : "";  // Store can be empty
            const ingredient = inputs[1].value.trim();
            const quantity = parseFloat(inputs[2].value.trim());

            // Validate that ingredient and quantity are filled, store is optional
            if (ingredient && !isNaN(quantity)) {
                ingredients.push({ store, ingredient, quantity }); // Store can be an empty string
            } else {
                alert("Each row must have an ingredient and valid quantity.");
                return; // Stop submission if any row is incomplete
            }
        } else {
            alert("Invalid row format. Each row must have ingredient and quantity inputs.");
            return;
        }
    }

    // Log the data being sent to the backend
    console.log("Ingredients to be sent:", ingredients);

    // Send data to the server
    try {
        const response = await fetch('http://127.0.0.1:5000/find-cheapest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: ingredients }) // Align with Python's expected input structure
        });

        const data = await response.json();
        console.log("Response from server:", data); // Log the response

        if (data.results) {
            displayResults(data.results);
        } else {
            alert("Error: " + (data.error || data.message || "Unknown error occurred."));
        }
    } catch (error) {
        console.log("Request failed:", error);
        alert("Error: " + error.message);
    }
}

// Function to display the results in the results table
function displayResults(items) {
    const resultsBody = document.getElementById("results-body");
    resultsBody.innerHTML = ""; // Clear previous results

    items.forEach(item => {
        const row = document.createElement("tr");

        // Check if totalCost is a valid number before calling toFixed
        const totalCost = (typeof item.totalCost === "number" && !isNaN(item.totalCost)) 
            ? item.totalCost.toFixed(2) 
            : "N/A";  // If not a valid number, set as N/A

        // Add columns for each data field
        row.innerHTML = `
            <td style="border: 1px solid #ddd; padding: 8px;">${item.ingredient}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${item.quantity}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${item.costPerItem}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${totalCost}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${item.store}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${item.travelTime}</td>`
        ;
        resultsBody.appendChild(row);
    });

    // Show the results container
    document.getElementById("results-container").style.display = "block";
}


// Event listener for the "Find" button
document.getElementById("find-button").addEventListener("click", (event) => {
    event.preventDefault();  // Prevent default form submission (if any)
    submitForm();  // Trigger the form submission process
//#endregion
});




//#region GeoLocation 
// call on start of page load with an alert 
async function sendPositionToPython(position) {

  alert("Please enable location for distance calculation");
  // remove line below later
  navigator.geolocation.getCurrentPosition(showPosition);
  const data = await response.json();
  ingredients.push({ store, ingredient, quantity });


  // Not yet implemented or tested 
  const url = 'http://127.0.0.1:5000/DistanceCalculation';
    const dataGeo = 
    {
    y: position.coords.latitude, // first var latitude 
    x: position.coords.longitude // second var longitude 
    };

    // push the data to the FLASK server 
    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataGeo)
    })
    .then(response => response.json())  // Parse the JSON response
    .then(dataGeo => console.log(dataGeo));   // Remove on final version we don't need user location on client side 
}
//#endregion



//#region Populate lists RCP
async function populateRecipies() {
    // Get the dropdown element by its ID
    var dropdown = document.getElementById("recipes");

    // testing and dev
    const apiUrl = 'http://127.0.0.1:5000/get-all-recipes';

    // Fetch all recipes from the API
        // Send GET request to the /get-all-recipes route
    fetch(apiUrl)
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        // Loop through each recipe and print it to the console
        data.recipes.forEach(recipe => {

            // remove console.log after testing
            console.log(`Recipe Name: ${recipe.recipe_name}, Total Cost: $${recipe.total_cost}`);

            // Create a new option element
            var newOption = document.createElement("option");

            // Set the value and text of the new option
            newOption.value = "RECIPE" + recipe.recipe_name;
            // Recipe name - Price in PLN from flask hook
            newOption.textContent = "PLN" + recipe.total_cost;

            // Append the new option to the dropdown
            dropdown.appendChild(newOption);
        });
    });
}
//#endregion



	//Slider distance filter
	var slider = document.getElementById("myRange");
	var output = document.getElementById("demo");
	output.innerHTML = slider.value;

	slider.oninput = function() {
		output.innerHTML = this.value;
	}
});