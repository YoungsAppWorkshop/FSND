from marshmallow import Schema, fields, post_load

from ..models.question import Question


class QuestionSchema(Schema):
    question = fields.Str()
    answer = fields.Str()
    category = fields.Str()
    difficulty = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        return Question(**data)
