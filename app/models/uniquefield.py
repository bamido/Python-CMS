from wtforms.validators import DataRequired, Email, ValidationError

class Unique(object):
    def __init__(self, model, field, fieldname, message=None):
        self.model = model
        self.field = field
        self.fieldname = fieldname
        if not message:
            message = f'This {fieldname} already exists!'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)