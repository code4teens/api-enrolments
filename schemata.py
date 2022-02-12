from marshmallow import fields, post_load, Schema

from models import Enrolment


class EnrolmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)

    user = fields.Nested('UserSchema', dump_only=True)
    cohort = fields.Nested('CohortSchema', dump_only=True)

    @post_load
    def make_enrolment(self, data, **kwargs):
        return Enrolment(**data)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class CohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()
