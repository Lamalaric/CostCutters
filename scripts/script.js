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
	document.getElementById('add-row-button').addEventListener('click', function () {
		const tableBody = document.getElementById('ingredient-rows');
		const newRow = document.createElement('tr');

		const ingredientCell = document.createElement('td');
		const ingredientInput = document.createElement('input');
		ingredientInput.type = 'text';
		ingredientInput.placeholder = 'Ingredient';
		ingredientCell.appendChild(ingredientInput);

		const quantityCell = document.createElement('td');
		const quantityInput = document.createElement('input');
		quantityInput.type = 'number';
		quantityInput.placeholder = 'Quantity';
		quantityCell.appendChild(quantityInput);

		newRow.appendChild(ingredientCell);
		newRow.appendChild(quantityCell);

		tableBody.appendChild(newRow);
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

});
