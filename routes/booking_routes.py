from flask import Blueprint, request, jsonify
from database import get_connection
import uuid
import qrcode
import os

booking_bp = Blueprint("booking", __name__)


# ===============================
# BOOK EVENT (USER REGISTRATION)
# ===============================
@booking_bp.route("/book", methods=["POST"])
def book_event():

    data = request.json

    user_id = data["user_id"]
    event_id = data["event_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # STEP 1: Check if user already booked this event
        cursor.execute(
            "SELECT * FROM bookings WHERE user_id=%s AND event_id=%s",
            (user_id, event_id)
        )

        existing_booking = cursor.fetchone()

        if existing_booking:
            return jsonify({
                "message": "You have already booked this event"
            }), 400

        # STEP 2: Check seat availability
        cursor.execute(
            "SELECT available_seats FROM events WHERE id=%s",
            (event_id,)
        )

        event = cursor.fetchone()

        if not event:
            return jsonify({
                "message": "Event not found"
            }), 404

        if event["available_seats"] <= 0:
            return jsonify({
                "message": "No seats available"
            }), 400

        # STEP 3: Generate ticket ID and QR Code
        ticket_id = "NOVA-" + str(uuid.uuid4())[:8].upper()
        
        qr_dir = os.path.join(os.getcwd(), "static", "qrcodes")
        os.makedirs(qr_dir, exist_ok=True)
        img = qrcode.make(ticket_id)
        img.save(os.path.join(qr_dir, f"{ticket_id}.png"))
        qr_code_path = f"/static/qrcodes/{ticket_id}.png"

        # STEP 4: Insert booking record
        cursor.execute(
            """
            INSERT INTO bookings (user_id, event_id, ticket_id, status)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, event_id, ticket_id, "confirmed")
        )

        # STEP 5: Reduce available seats
        cursor.execute(
            """
            UPDATE events
            SET available_seats = available_seats - 1
            WHERE id=%s
            """,
            (event_id,)
        )

        conn.commit()

        return jsonify({
            "message": "Booking successful",
            "ticket_id": ticket_id,
            "qr_code": qr_code_path
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            "message": "Booking failed",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# ===============================
# GET USER BOOKINGS
# ===============================
@booking_bp.route("/my-bookings/<int:user_id>", methods=["GET"])
def get_user_bookings(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                events.title AS event_title,
                bookings.ticket_id,
                bookings.booking_date,
                bookings.status
            FROM bookings
            JOIN events ON bookings.event_id = events.id
            WHERE bookings.user_id = %s
            ORDER BY bookings.booking_date DESC
        """
        cursor.execute(query, (user_id,))
        bookings = cursor.fetchall()
        
        return jsonify(bookings)

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch your bookings",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# ADMIN: VIEW ALL BOOKINGS
# ===============================
@booking_bp.route("/admin/bookings", methods=["GET"])
def view_all_bookings():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                users.name,
                users.email,
                events.title AS event_title,
                bookings.ticket_id,
                bookings.booking_date,
                bookings.status
            FROM bookings
            JOIN users ON bookings.user_id = users.id
            JOIN events ON bookings.event_id = events.id
            ORDER BY bookings.booking_date DESC
        """

        cursor.execute(query)
        bookings = cursor.fetchall()

        return jsonify(bookings)

    except Exception as e:
        return jsonify({
            "message": "Failed to fetch bookings",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
