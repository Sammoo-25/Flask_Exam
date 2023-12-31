from app import *

app.config.from_object(Config)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,  port=5000, host="0.0.0.0")
