from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from data.event import Event
from data.concert_hall import ConcertHall
from flask import jsonify, request


def abort_if_events_not_found(events_id):
    session = db_session.create_session()
    events = session.query(Event).get(events_id)
    if not events:
        abort(404, message=f"Events {events_id} not found")


def abort_if_wrong_format(events_id):
    if not events_id.isdigit():
        abort(404, message=f"Wrong format! Id must be integer")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('hall_id', required=True)


class EventResource(Resource):
    def get(self, events_id):
        abort_if_wrong_format(events_id)
        events_id = int(events_id)
        abort_if_events_not_found(events_id)
        session = db_session.create_session()
        events = session.query(Event).get(events_id)
        return jsonify({'events': events.to_dict(only=('name', 'about', 'start_date_formatted', 'city', 'capacity_left',
                                                       'price', 'place'))})

    def delete(self, events_id):
        abort_if_events_not_found(events_id)
        session = db_session.create_session()
        events = session.query(Event).get(events_id)
        session.delete(events)
        session.commit()
        return jsonify({'success': 'OK'})


class EventListResource(Resource):
    def get(self):
        session = db_session.create_session()
        events = session.query(Event).all()
        return jsonify({'events': [item.to_dict(
            only=('name', 'about', 'start_date_formatted', 'city', 'capacity_left',
                  'price', 'place')) for item in events]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        hall = session.query(ConcertHall).filter(ConcertHall.id == args['hall_id']).first()
        event = Event(
            name=args['name'],
            about=args['about'],
            place=hall.fullname,
            capacity_left=hall.capacity,
            city=hall.city,
            hall_id=args['hall_id']

        )
        session.add(event)
        session.commit()
        return jsonify({'event': {'id': event.id, 'name': event.name, 'hall_id': event.hall_id},
                        'success': 'OK'})
