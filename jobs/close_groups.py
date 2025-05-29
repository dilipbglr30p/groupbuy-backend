from models import db, GroupBuy, Participant
from datetime import datetime

def close_expired_groups(app):
    with app.app_context():
        now = datetime.utcnow()
        groups = GroupBuy.query.filter_by(is_closed=False).all()
        print(f"\n⏱️ Auto-close check at {now} — Found {len(groups)} open group(s)")
        closed = 0

        for group in groups:
            total_qty = db.session.query(db.func.sum(Participant.qty)).filter_by(group_buy_id=group.id).scalar() or 0
            print(f"🔍 Group {group.id} — deadline: {group.deadline} | now: {now} | qty: {total_qty}/{group.max_qty}")

            if group.deadline <= now or (group.max_qty and total_qty >= group.max_qty):
                group.is_closed = True
                db.session.commit()
                print(f"✅ Group {group.id} auto-closed!")
                closed += 1

        print(f"🧹 Total groups auto-closed: {closed}")
