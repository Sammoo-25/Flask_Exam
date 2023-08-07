import os

from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_login import UserMixin, login_required, logout_user, LoginManager, current_user, login_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from forms import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdasdfasdgfasdgasdgasdgasdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Samvel357552@localhost:5432/advertisements_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASH_MESSAGES_CATEGORY'] = 'message'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'index'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(100))
    gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)

    products = db.relationship('Product', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    expire_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), default='default.jpg')
    rating = db.Column(db.Integer, default=0)
    rating_count = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    products = Product.query.order_by(Product.id.desc()).all()

    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')

            next_page = session.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('userPage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    session['next'] = request.args.get('next')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = Users(name=form.name.data, surname=form.surname.data,
                         email=form.email.data, gender=form.gender.data, phone_number=form.phone_number.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('userPage'))

    return render_template('register.html', form=form)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()

    if form.validate_on_submit():
        name = form.ProductName.data
        description = form.Description.data
        category = form.category.data
        expire_date = form.expire_date.data
        price = form.price.data
        image = form.image.data
        new_product = Product(
            name=name,
            description=description,
            category=category,
            expire_date=expire_date,
            price=price,
            user=current_user
        )

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.root_path, 'static/product_images', filename)
            image.save(image_path)
            new_product.image = filename
            db.session.commit()

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')

        return redirect(url_for('myitems'))

    return render_template('addProducts.html', form=form)


@app.route('/ProductPage/<int:id>', methods=['POST', 'GET'])
def ProductPage(id):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    product = session.query(Product).filter_by(id=id).first()
    form = GetRating()

    # if form.validate_on_submit():
    print(product.rating)
    print(form.rating.data)
    # Fix the logic of this route
    if product:
        if form.validate_on_submit():
            product.rating += form.rating.data
            product.rating_count += 1
            db.session.add(product.rating)
            db.session.commit()
        return render_template('productPage.html', products=[product], form=form)
    else:
        flash('Product not found', 'danger')
        return redirect(url_for('myitems'))
    # Fix the logic of this route
# return render_template('productPage.html', products=[product], form=form)

@app.route('/UserPage', methods=['GET', 'POST'])
@login_required
def userPage():
    # from forms import UpdateProfileImageForm
    form = UpdateProfileImageForm()

    if form.validate_on_submit():
        if form.profile_image.data:
            filename = secure_filename(form.profile_image.data.filename)
            file_path = os.path.join(app.root_path, 'static/profile_images', filename)
            form.profile_image.data.save(file_path)
            current_user.profile_image = filename
            db.session.commit()

    return render_template('userPage.html', current_user=current_user, form=form)


@app.route('/myitems', methods=['GET', 'POST'])
@login_required
def myitems():
    prod_form = AddProductForm()
    products = Product.query.filter_by(user_id=current_user.id).order_by(Product.id.desc()).all()

    return render_template('myitems.html', prod_form=prod_form, products=products)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
