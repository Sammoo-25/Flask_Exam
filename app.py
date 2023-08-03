from flask import Flask, render_template, flash
from flask_login import UserMixin, login_required, logout_user, LoginManager, current_user, login_user
# from forms import RegisterForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)


from flask import redirect, url_for, session, request


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm()

    if current_user.is_authenticated:  # Check if the user is already logged in
        return redirect(url_for('index'))  # Redirect to the homepage

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Use the method you defined to check the password
            # Successful login
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')

            # Redirect to the page the user tried to access before logging in
            next_page = session.get('next')
            if next_page:
                return redirect(next_page)

            # If no specific page was requested, redirect to the homepage
            return redirect(url_for('index'))
        else:
            # Failed login
            flash('Login failed. Please check your email and password.', 'danger')

    session['next'] = request.args.get('next')

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = Users(name=form.name.data, surname=form.surname.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/AddProducts')
def AddProducts():
    return render_template('addProducts.html')


@app.route('/ProductPage')
def ProductPage():
    return render_template('productPage.html')


@app.route('/UserPage')
@login_required
def userPgae():
    return render_template('userPage.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
