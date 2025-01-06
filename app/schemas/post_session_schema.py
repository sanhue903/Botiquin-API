from app.extensions import ma
from marshmallow import fields, validate


class InnerScoreSchema(ma.Schema):
    answer = fields.Str(required=True)
    seconds = fields.Float(required=True)
    is_correct = fields.Boolean(required=True)
    attempt = fields.Integer(required=True)

    question_id = fields.Str(required=True, validate=validate.Length(min=6, max=6))

class PostSessionSchema(ma.Schema):
    seconds = fields.Float(required=True)
    finish_chapter = fields.Boolean(required=True)
    date = fields.DateTime('%d-%m-%Y', required=True)
    
    chapter_id = fields.Str(required=True, validate=validate.Length(min=6, max=6))

    scores = fields.List(fields.Nested(InnerScoreSchema), required=True)
    