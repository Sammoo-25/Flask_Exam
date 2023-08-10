from flask_login import LoginManager
from app.config import *
from app import *
from app.routes import *

app.config.from_object(Config)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
