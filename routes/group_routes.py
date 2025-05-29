from flask import Blueprint, request, jsonify
from models import db, GroupBuy, Participant
from datetime import datetime, timedelta
from utils.whatsapp import send_order_confirmation

# ✅ This is the Blueprint being imported in app.py
group_routes = Blueprint('group_routes', __name__)

@group_routes.route("/create-group", methods=["POST"])
def create_group():
    data = request.json
    new_group = GroupBuy(
        product_id=data["product_id"],
        deadline=datetime.utcnow() + timedelta(hours=24),
        min_qty=data.get("min_qty", 1),
        max_qty=data.get("max_qty", 10)
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group created", "group_id": new_group.id}), 201

@group_routes.route("/join-group", methods=["POST"])
def join_group():
    data = request.json
    group = GroupBuy.query.get(data["group_buy_id"])
    if group.is_closed:
        return jsonify({"error": "Group is closed"}), 400

    participant = Participant(
        group_buy_id=data["group_buy_id"],
        name=data["name"],
        phone=data["phone"],
        size=data.get("size"),
        qty=data["qty"]
    )
    db.session.add(participant)
    db.session.commit()

    total = db.session.query(db.func.sum(Participant.qty)).filter_by(group_buy_id=data["group_buy_id"]).scalar()
    if group.max_qty and total >= group.max_qty:
        group.is_closed = True
        db.session.commit()

    return jsonify({"message": "Joined group", "total_joined": total}), 200

# ✅ New WhatsApp Notification Route
@group_routes.route('/send-whatsapp', methods=['POST'])
def whatsapp_notify():
    data = request.json
    success = send_order_confirmation(
        data['name'],
        data['phone'],
        data['order_id'],
        data['delivery_date'],
        data['delivery_time']
    )
    return jsonify({'status': 'sent' if success else 'failed'})
