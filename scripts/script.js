// PROGRESS BAR
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
	})
}

//Wait for the full DOM to be loaded...
document.addEventListener('DOMContentLoaded', function () {
	const menuIcon = document.getElementById('menu-icon');
	const navLinks = document.getElementById('nav-links');


	//BURGER MENU
	if (menuIcon && navLinks) {
		menuIcon.addEventListener('click', function () {
			navLinks.classList.toggle('active');
		});
	}

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
                <td>${ingredient.travelTime}</td>
            `;
				ingredientsList.appendChild(row);
			});

			// Afficher le coût total
			const totalCostElement = document.querySelector('.total-cost');
			totalCostElement.textContent = recipe.totalCost;

			// Afficher le bloc des détails de la recette
			document.getElementById('recipe-details').classList.remove('hidden');
		});
	});


	// ISSUE GRADE 1, SAVE BUTTON HAVING ISSUES DUE TO CORS POLICY
	document.getElementById("save-button").addEventListener("click", function () {
		const rows = document.querySelectorAll("#ingredient-rows tr");
		let items = [];
	
		// Collect ingredient, store, and quantity values from each row
		rows.forEach(row => {
			const inputs = row.querySelectorAll("input");
			const store = inputs[0].value.trim();
			const ingredient = inputs[1].value.trim();
			const quantity = parseFloat(inputs[2].value.trim());
	
			if (store && ingredient && !isNaN(quantity)) {
				items.push({
					store: store,
					ingredient: ingredient,
					quantity: quantity
				});
			} else {
				console.error("Invalid row data:", { store, ingredient, quantity });
			}
		});
	
		if (items.length === 0) {
			alert("No valid ingredients to save.");
			return;
		}
	
		// Calculate total price (just as an example)
		const totalPrice = items.reduce((total, item) => total + item.quantity * 2.5, 0).toFixed(2);
	
		const data = {
			username: "test_user", // You can replace this with dynamic input if needed
			recipe_name: "Sample Recipe", // Replace with a user-provided recipe name
			items: items,
			total_price: totalPrice
		};
	
		console.log("Data being sent to backend:", data);
	
		fetch('/add-recipe', {
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

});

