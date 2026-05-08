from flask import Blueprint, request, jsonify
from database import get_connection

event_bp = Blueprint("event", __name__)


# GET ALL EVENTS
@event_bp.route("/events", methods=["GET"])
def get_events():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM events")

    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(events)

# ===============================
# ADMIN: CREATE EVENT
# ===============================


@event_bp.route("/admin/create-event", methods=["POST"])
def create_event():
    data = request.json
    try:
        title = data["title"]
        description = data.get("description", "")
        date = data["date"]
        location = data.get("location", "")
        total_seats = int(data["total_seats"])

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO events (title, description, event_date, location, total_seats, available_seats)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, description, date,
                       location, total_seats, total_seats))
        conn.commit()

        return jsonify({
            "message": "Event created successfully"
        })
    except Exception as e:
        print(e)
        return jsonify({"message": "Event creation failed", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ===============================
# ADMIN: EVENT STATS
# ===============================


@event_bp.route("/admin/event-stats", methods=["GET"])
def get_event_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Sums all events
        query = """
            SELECT 
                COALESCE(SUM(total_seats), 0) AS total_seats,
                COALESCE(SUM(total_seats - available_seats), 0) AS booked_seats,
                COALESCE(SUM(available_seats), 0) AS remaining_seats
            FROM events
        """
        cursor.execute(query)
        stats = cursor.fetchone()

        # Ensures returned values are integers safely
        return jsonify({
            "total_seats": int(stats["total_seats"]),
            "booked_seats": int(stats["booked_seats"]),
            "remaining_seats": int(stats["remaining_seats"])
        })
    except Exception as e:
        print(e)
        return jsonify({"message": "Stats fetch failed", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
