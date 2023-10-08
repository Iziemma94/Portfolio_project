from app import app, db, User, Recipe

# Inside your app.py or a separate script

# Delete the existing user with the username 'Toby' if it exists
with app.app_context():
    # Your code here (deleting existing user and creating a new one)
    existing_user = User.query.filter_by(username='Chevalier').first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()

with app.app_context():
    db.create_all()

    # Create a user
    user = User(username="Chevalier", email="tariemmanuel00@gmail.com", password="?TZl2^~m{(&>")
    db.session.add(user)
    db.session.commit()

    # Sample Recipe 1
    recipe1 = Recipe(
            title="Spaghetti Carbonara",
            ingredients="Pasta, Eggs, Bacon, Cheese",
            instructions="Cook pasta, fry bacon, mix with eggs and cheese",
            image_filename="uploads/spaghetti_carbonara.jpg",
            user_id=user.id
    )
    db.session.add(recipe1)

    # Sample Recipe 2
    recipe2 = Recipe(
            title="Chicken Stir-Fry",
            ingredients="Chicken, Vegetables, Soy Sauce",
            instructions="Stir-fry chicken and vegetables, add soy sauce",
            image_filename="uploads/chicken_stir_fry.jpg",
            user_id=user.id
    )
    db.session.add(recipe2)

    # Sample Recipe 3
    recipe3 = Recipe(
            title="Spaghetti Bolognese",
            ingredients="1 pound (450g) ground beef, 1 onion, chopped, 2 cloves garlic, minced, 1 (28-ounce) can crushed tomatoes, 1/4 cup tomato paste, 1/2 cup red wine (optional), 1 teaspoon dried basil, 1 teaspoon dried oregano, Salt and pepper to taste, 12 ounces (340g) spaghetti, Grated Parmesan cheese for serving",
            instructions="Brown beef, sauté onion and garlic, add tomatoes, wine, and seasonings, serve over cooked spaghetti, top with Parmesan cheese",
            image_filename="uploads/spaghetti_bolognese.jpg",
            user_id=user.id
    )
    db.session.add(recipe3)

    # Sample Recipe 4
    recipe4 = Recipe(
            title="Pancakes",
            ingredients="1 cup all-purpose flour, 2 tablespoons sugar, 1 teaspoon baking powder, 1/2 teaspoon baking soda, 1/4 teaspoon salt, 1 cup buttermilk, 1 large egg, 2 tablespoons unsalted butter, melted",
            instructions="Mix dry ingredients, whisk wet ingredients separately, combine, cook spoonfuls of batter on a hot griddle until bubbly, flip and cook until golden brown",
            image_filename="uploads/pancakes.jpg",
            user_id=user.id
    )
    db.session.add(recipe4)

    # Sample Recipe 5
    recipe5 = Recipe(
            title="Caesar Salad",
            ingredients="Romaine lettuce, Croutons, Grated Parmesan cheese, Caesar dressing",
            instructions="Tear lettuce, add croutons and Parmesan, toss with dressing",
            image_filename="uploads/caesar_salad.jpg",
            user_id=user.id
    )
    db.session.add(recipe5)

    # Sample Recipe 6
    recipe6 = Recipe(
            title="Chocolate Chip Cookies",
            ingredients="1 cup (2 sticks) unsalted butter, 3/4 cup granulated sugar, 3/4 cup brown sugar, 1 teaspoon vanilla extract, 2 large eggs, 2 1/4 cups all-purpose flour, 1 teaspoon baking soda, 1/2 teaspoon salt, 2 cups semisweet chocolate chips",
            instructions="Cream butter and sugars, add eggs and vanilla, mix dry ingredients separately, combine, fold in chocolate chips, drop spoonfuls onto baking sheets, bake at 350°F (175°C) for 10-12 minutes",
            image_filename="uploads/chocolate_chip_cookies.jpg",
            user_id=user.id
    )
    db.session.add(recipe6)

    # Sample Recipe 7
    recipe7 = Recipe(
            title="Tomato Basil Pasta",
            ingredients="Pasta, Fresh tomatoes, Fresh basil, Olive oil, Garlic, Salt, Pepper",
            instructions="Cook pasta, sauté garlic and tomatoes in olive oil, add cooked pasta and fresh basil, season with salt and pepper",
            image_filename="uploads/tomato_basil_pasta.jpg",
            user_id=user.id
    )
    db.session.add(recipe7)

    # Sample Recipe 8
    recipe8 = Recipe(
            title="Grilled Chicken Sandwich",
            ingredients="Chicken breast, Hamburger bun, Lettuce, Tomato, Mayonnaise, Mustard, Pickles",
            instructions="Season chicken breast, grill until cooked, assemble sandwich with toppings and condiments",
            image_filename="uploads/grilled_chicken_sandwich.jpg",
            user_id=user.id

    )
    db.session.add(recipe8)

    # Sample Recipe 9
    recipe9 = Recipe(
            title="Mushroom Risotto",
            ingredients="Arborio rice, Mushrooms, Onion, Garlic, White wine, Chicken broth, Parmesan cheese, Butter",
            instructions="Sauté mushrooms, onion, and garlic, add rice, deglaze with wine, gradually add broth, stir until creamy, mix in Parmesan cheese and butter",
            image_filename="uploads/mushroom_risotto.jpg",
            user_id=user.id
    )
    db.session.add(recipe9)

    # Sample Recipe 10
    recipe10 = Recipe(
            title="Greek Salad",
            ingredients="Cucumbers, Tomatoes, Red onion, Kalamata olives, Feta cheese, Olive oil, Red wine vinegar, Oregano, Salt, Pepper",
            instructions="Chop vegetables and olives, crumble feta cheese, whisk olive oil, vinegar, and seasonings for dressing, toss all ingredients together",
            image_filename="uploads/greek_salad.jpg",
            user_id=user.id
    )
    db.session.add(recipe10)

    # Sample Recipe 11
    recipe11 = Recipe(
            title="Egusi Soup",
            ingredients="Egusi seeds, Meat (e.g., beef, chicken), Vegetables (e.g., spinach, bitter leaf), Palm oil, Onions, Pepper, Seasonings (e.g., bouillon cubes), Water",
            instructions="1. Toast egusi seeds until they turn slightly brown. 2. Cook meat with onions and seasonings until tender. 3. Add palm oil, egusi seeds, and water. 4. Simmer until egusi thickens the soup. 5. Add vegetables and pepper, and cook until vegetables are tender. 6. Serve hot.",
            image_filename="uploads/egusi_soup.jpg",
            user_id=user.id
    )
    db.session.add(recipe11)

    # Sample Recipe 12
    recipe12 = Recipe(
            title="Jollof Rice",
            ingredients="Rice, Tomatoes, Red bell peppers, Onions, Scotch bonnet peppers, Cooking oil, Spices (e.g., thyme, curry), Salt, Chicken or beef (optional), Peas and carrots (optional)",
            instructions="1. Blend tomatoes, red bell peppers, onions, and scotch bonnet peppers to make a sauce. 2. Heat cooking oil, add chopped onions, and fry until translucent. 3. Add spices and tomato sauce and cook until oil separates. 4. Add rice, peas, carrots, and meat (if desired). 5. Cook until rice is done and everything is well mixed. 6. Serve hot.",
            image_filename="uploads/jollof_rice.JPG",  # Specify the path relative to the "uploads" directory
            user_id=user.id
    )
    db.session.add(recipe12)

    try:
        # Commit the changes to the database
        db.session.commit()
        print("Recipes added successfully.")
    except Exception as e:
        print(f"Error adding recipes: {str(e)}")
