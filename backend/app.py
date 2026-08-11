from pathlib import Path

from flask import Flask, render_template

from extensions import db
from routes.listings import listings_bp
from routes.images import images_bp


# ==========================
# DATABASE
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "rental.db"


# ==========================
# FLASK APPLICATION
# ==========================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(listings_bp)
app.register_blueprint(images_bp)


# ==========================
# ROUTES
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":
    app.run(debug=True)