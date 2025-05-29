from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.group_routes import group_routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Create tables on first run
with app.app_context():
    db.create_all()

# Register API routes
app.register_blueprint(group_routes)

# ⏰ Schedule job to auto-close groups
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.close_groups import close_expired_groups

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda: close_expired_groups(app), trigger="interval", seconds=60)
scheduler.start()

# Start server
if __name__ == "__main__":
    print("🚀 Starting Group Buy Backend...")
    app.run(debug=True)
