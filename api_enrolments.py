from flask import Blueprint, jsonify, request

from database import db_session
from models import Cohort, Enrolment, User
from schemata import EnrolmentSchema

api_enrolments = Blueprint('api_enrolments', __name__)


@api_enrolments.route('/enrolments')
def get_enrolments():
    enrolments = Enrolment.query.order_by(Enrolment.id).all()
    data = EnrolmentSchema(many=True).dump(enrolments)

    return jsonify(data), 200


@api_enrolments.route('/enrolments', methods=['POST'])
def create_enrolment():
    keys = ['user_id', 'cohort_id']

    if sorted([key for key in request.json]) == sorted(keys):
        user_id = request.json.get('user_id')
        cohort_id = request.json.get('cohort_id')
        user = User.query.filter_by(id=user_id).one_or_none()
        cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

        if user is not None and cohort is not None:
            existing_enrolment = Enrolment.query.filter_by(user_id=user_id)\
                .filter_by(cohort_id=cohort_id)\
                .one_or_none()

            if existing_enrolment is None:
                enrolment_schema = EnrolmentSchema()

                try:
                    enrolment = enrolment_schema.load(request.json)
                except Exception as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    db_session.add(enrolment)
                    db_session.commit()
                    data = {
                        'title': 'Created',
                        'status': 201,
                        'detail': f'Enrolment {enrolment.id} created'
                    }

                    return data, 201
            else:
                data = {
                    'title': 'Conflict',
                    'status': 409,
                    'detail': 'Enrolment with posted details already exists'
                }

                return data, 409
        else:
            data = {
                'title': 'Bad Request',
                'status': 400,
                'detail': 'User or cohort does not exist'
            }

            return data, 400

    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400
