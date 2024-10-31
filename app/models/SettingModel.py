from app.models.mydb  import db

class SettingModel(db.Model):
    __tablename__ = 'settings'

    setting_id = db.Column(db.Integer, primary_key=True)
    thekey = db.Column(db.String(255), unique=True, nullable=False)
    thevalue = db.Column(db.Text, unique=False, nullable=False)    
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<SettingModel {}>'.format(self.thekey)

    def get_setting_item(thekey):
        result = SettingModel.query.filter_by(thekey=thekey).first()
        return result