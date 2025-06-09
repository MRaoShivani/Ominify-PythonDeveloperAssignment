# app/routes.py

from flask import Blueprint, request, jsonify
from app.models import FitnessClass, Booking
from app import db
from sqlalchemy import func
from datetime import datetime
import pytz
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bp = Blueprint('api', __name__)

# Timezone settings: Indian Standard Time (UTC+5:30)
IST = pytz.timezone('Asia/Kolkata')

@bp.route('/classes', methods=['GET'])
def get_classes():
    """
    GET /classes
    Returns all fitness classes with their details including
    date/time converted to IST timezone.
    """
    try:
        # Query all fitness classes from the database
        classes = FitnessClass.query.all()

        result = []
        for c in classes:
            result.append({
                'id': c.id,
                # Class name
                'name': c.name,
                # Convert datetime to IST and return ISO format string
                'datetime': c.datetime.astimezone(IST).isoformat(),
                # Instructor's name
                'instructor': c.instructor,
                # Available slots for booking
                'available_slots': c.available_slots
            })

        # Return list of classes as JSON
        return jsonify(result)

    except Exception as e:
        # Catch any unexpected errors, log e if needed
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/bookings', methods=['GET'])
def get_bookings():
    """
    GET /bookings?email=...
    Returns all bookings made by the email provided as query param.
    """

    try:
        # Extract email from query parameters
        email = request.args.get('email')

        # Validate input presence
        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Case-insensitive search for bookings by email
        bookings = Booking.query.filter(func.lower(Booking.client_email) == email.lower()).all()

        # If no bookings found, return 404 with message
        if not bookings:
            return jsonify({'error': f'No bookings found for email: {email}'}), 404

        result = []
        for b in bookings:
            result.append({
                'booking_id': b.id,
                'class_id': b.class_id,
                'client_name': b.client_name,
                'client_email': b.client_email
            })

        # Return all bookings as JSON list
        return jsonify(result)

    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/book', methods=['POST'])
def book_class():
    """
    POST /book
    Accepts booking data (class_id, client_name, client_email) via JSON,
    form data, or query parameters.
    Validates inputs, checks availability, books if possible.
    """

    try:
        # Attempt to parse JSON body without raising error if not JSON
        data = request.get_json(silent=True)

        # If no JSON, try form data or query params for flexibility
        if not data:
            data = request.form.to_dict() or request.args.to_dict()

        # Get required fields from input; allow some key flexibility
        class_id = data.get('class_id')
        name = data.get('client_name') or data.get('name')
        email = data.get('client_email') or data.get('email')

         # Log the booking attempt with received info
        logger.info(f"Booking attempted by {email} for class {class_id}")

        # Validate that all required fields are present
        if not all([class_id, name, email]):
            return jsonify({'error': 'Missing fields: class_id, client_name, and client_email are required'}), 400

        # Retrieve the fitness class by ID from the DB
        fc = FitnessClass.query.get(class_id)
        if not fc:
            logger.error(f"Booking failed: Class not found for class_id={class_id}")
            return jsonify({'error': 'Class not found'}), 404

        # Check if slots are available for booking
        if fc.available_slots <= 0:
            logger.error(f"Booking failed: No slots available for class_id={class_id}")
            return jsonify({'error': 'No slots available'}), 409  # 409 Conflict for no availability

        # Create new booking record
        booking = Booking(class_id=class_id, client_name=name, client_email=email)
        # Decrement available slots by 1
        fc.available_slots -= 1

        # Add booking and update class in DB session
        db.session.add(booking)
        db.session.commit()

        # Log successful booking
        logger.info(f"Booking successful for {email} in class {class_id}")

        # Return success response
        return jsonify({'message': 'Booking successful'}), 201

    except Exception as e:
        # Log exception e if needed for debugging
        return jsonify({'error': 'Internal server error'}), 500


