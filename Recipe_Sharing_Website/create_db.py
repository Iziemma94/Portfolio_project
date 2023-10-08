import sqlite3

# Function to create the database and tables
def create_database():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        with sqlite3.connect("recipes.db") as connection:
            cursor = connection.cursor()

            # Define SQL statements for table creation
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username VARCHAR UNIQUE,
                Email VARCHAR UNIQUE,         -- New Email field
                Password VARCHAR,
                FacebookLink VARCHAR(100),    -- Adjusted for Facebook Link with a maximum length of 100 characters
                TwitterLink VARCHAR(100),     -- Adjusted for Twitter Link with a maximum length of 100 characters
                Bio TEXT                      -- Bio as a TEXT field with variable length
            );
            """

            create_recipes_table = """
            CREATE TABLE IF NOT EXISTS recipes (
                RecipeID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Ingredients TEXT,
                Instructions TEXT,
                AuthorID INTEGER,
                image_file_name VARCHAR(255),  -- New image_file_name field
                FOREIGN KEY (AuthorID) REFERENCES users (UserID)
            );
            """

            # Execute SQL statements to create tables
            cursor.execute(create_users_table)
            cursor.execute(create_recipes_table)

            # Commit changes and close connection
            connection.commit()
            
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Call the function to create the database
if __name__ == "__main__":
    create_database()
