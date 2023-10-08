from flask import Flask, render_template, request, redirect, url_for, flash, session,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin, login_required
from werkzeug.utils import secure_filename
import os
from wtforms import StringField, TextAreaField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, TextAreaField, SubmitField
from forms import RecipeForm
from forms import ContactForm

# Create a Flask app
app = Flask(__name__)
app.secret_key = '237f8787500248da4d82524350e07c9d'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads'
app.config['PROFILE_PICTURES_UPLOAD_FOLDER'] = 'static/uploads/profile_pictures'
app.config['RECIPE_IMAGES_UPLOAD_FOLDER'] = 'static/uploads/recipe_images'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'JPG'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.static_folder = 'static'
db = SQLAlchemy(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # Specify the login view route
login_manager.init_app(app)

class ProfilePictureForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'JPG'], 'Only images with jpg, jpeg, or png formats are allowed.')
    ])
    submit = SubmitField('Upload Profile Picture')

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    facebook_link = db.Column(db.String(100))
    twitter_link = db.Column(db.String(100))
    bio = db.Column(db.Text)

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # Define a relationship with recipes (one-to-many or many-to-many)
    recipes = db.relationship('Recipe', backref='author', lazy=True)

# Define the Recipe model

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255))
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define a relationship with the User model
    author = db.relationship('User', backref='recipes')

# Create forms for user profile
class ProfileForm(FlaskForm):
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    facebook_link = StringField('Facebook Link')
    twitter_link = StringField('Twitter Link')
    submit = SubmitField('Update Profile')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    image = FileField('Recipe Image')  # Add this line for the image field
    submit = SubmitField('Save Recipe')


# Routes

@app.route('/')
def index():
    # Fetch the most recent recipes from the database
    recipes = Recipe.query.order_by(Recipe.id.desc()).limit(5).all()
    return render_template('home.html', recipes=recipes)

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()  # Create an instance of your ContactForm
    return render_template('contact.html', form=form)

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            # Generate a secure filename and save the file to a specific folder
            filename = secure_filename(f.filename)
            f.save(filename)
            return 'File uploaded successfully'
    return 'No file selected'

@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    form = ProfilePictureForm()

    if form.validate_on_submit():
        # Handle the profile picture upload
        profile_picture = form.profile_picture.data
        if profile_picture:
            filename = secure_filename(profile_picture.filename)

            # Construct the full path to save the file in 'static/uploads/profile_pictures'
            image_path = os.path.join(app.static_folder, 'uploads', 'profile_pictures', filename)

            # Save the uploaded file
            profile_picture.save(image_path)

            # Update the user's profile picture filename in the database
            current_user.profile_picture = filename
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('upload_profile_picture.html', form=form)

@app.route('/upload_recipe_image', methods=['POST'])
@login_required
def upload_recipe_image():
    form = RecipeImageForm()

    if form.validate_on_submit():
        # Handle the recipe image upload
        recipe_image = form.recipe_image.data
        if recipe_image:
            filename = secure_filename(recipe_image.filename)

            # Construct the full path to save the file in 'static/uploads/recipe_images'
            image_path = os.path.join(app.static_folder, 'uploads', 'recipe_images', filename)

            # Save the uploaded file
            recipe_image.save(image_path)

            # You may want to associate the image filename with a specific recipe in your database
            # For example, if you have a Recipe model with an 'image_filename' field:
            # recipe = Recipe.query.get(recipe_id)
            # recipe.image_filename = filename
            # db.session.commit()

        return redirect(url_for('index'))

    return render_template('upload_recipe_image.html', form=form)

@app.route('/profile_picture_upload')
def profile_picture_upload():
    return render_template('profile_picture_upload.html')

@app.route('/recipe_image_upload')
def recipe_image_upload():
    return render_template('recipe_image_upload.html')

# Authentication routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Add email input
        password = request.form['password']

        # Check if a user with the same username or email already exists
        existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
        else:
            try:
                new_user = User(username=username, email=email, password=password)  # Include email
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully', 'success')
                return redirect(url_for('login'))
            except IntegrityError as e:
                db.session.rollback()
                print(f"IntegrityError: {str(e)}")  # Print the error message for debugging
                flash('Error creating the account. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# User Profile Routes

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    profile_form = ProfilePictureForm()
    if current_user.is_authenticated:
        # Get the currently logged-in user's data
        user_data = {
            'username': current_user.username,
        }

        try:
            # Attempt to create an account (this part of code is not clear in the context)
            # If successful, flash a success message and redirect to the login page
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {str(e)}")  # Print the error message for debugging
            flash('Error creating the account. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.facebook_link = form.facebook_link.data
        user.twitter_link = form.twitter_link.data
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('user_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.facebook_link.data = current_user.facebook_link
        form.twitter_link.data = current_user.twitter_link
    return render_template('edit_profile.html', form=form)

# Recipe-related routes

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if not current_user.is_authenticated:
        flash('Please log in to add a recipe', 'danger')
        return redirect(url_for('login'))
    form = RecipeForm()
    if form.validate_on_submit():
        title = form.title.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        user_id = current_user.id
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=user_id)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form)

@app.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get(id)
    if not current_user.is_authenticated:
        flash('Please log in to edit a recipe', 'danger')
        return redirect(url_for('login'))
    # Check if the user is authorized to edit this recipe
    if recipe.user_id != current_user.id:
        flash('You can only edit your own recipes', 'danger')
        return redirect(url_for('index'))

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        # Handle image upload if a new image is provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                recipe.image = filename  # Update the recipe's image field

        # Update other recipe details
        form.populate_obj(recipe)

        db.session.commit()
        flash('Recipe updated successfully', 'success')
        return redirect(url_for('index'))

    return render_template('edit_recipe.html', form=form, recipe=recipe)

@app.route('/create_recipe', methods=['GET', 'POST'])
@login_required  # You can use this decorator to ensure the user is logged in
def create_recipe():
    form = RecipeForm()

    if form.validate_on_submit():
        # Process the uploaded file
        if form.image.data:
            # Save the file to a location, e.g., the 'uploads' folder
            image_path = 'uploads/' + secure_filename(form.image.data.filename)
            form.image.data.save(image_path)

        # Create and save the recipe
        new_recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            image_filename=image_path,  # Corrected field name to 'image_filename'
            user_id=current_user.id  # Assuming you have a User model with an 'id' field
        )

        # Add the new recipe to the database session
        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe created successfully', 'success')
        return redirect(url_for('index'))

    return render_template('create_recipe.html', form=form)

app.route('/recipe_list')
def recipe_list():
    # Pass the list of sample recipes to the template

    return render_template('recipe_list.html', recipes=sample_recipes)

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not current_user.is_authenticated:
        flash('Please log in to delete a recipe', 'danger')
        return redirect(url_for('login'))
    if recipe.user_id != current_user.id:
        flash('You can only delete your own recipes', 'danger')
        return redirect(url_for('index'))
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully', 'success')
    return redirect(url_for('index'))

# Search Route
@app.route('/search', methods=['GET'])
def search():
    # Retrieve the search query from the URL parameters
    query = request.args.get('query')
    # Perform a database search for recipes based on the query
    recipes = Recipe.query.filter(Recipe.title.ilike(f"%{query}%")).all()
    # Render the search results template with the query and recipes
    return render_template('search_results.html', query=query, recipes=recipes)

@app.route('/recipe/<int:id>')
def recipe(id):
    recipe = Recipe.query.get(id)
    if recipe is None:
        flash('Recipe not found', 'danger')
        return redirect(url_for('index'))
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
