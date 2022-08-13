from base import db


class CitizenDetailsVO(db.Model):
    __tablename__ = 'citizendetails_table'
    citizen_id = db.Column('citizen_id', db.Integer,primary_key=True, autoincrement=True)
    citizen_name = db.Column('citizen_name', db.String(255), nullable=False)
    citizen_gender = db.Column('citizen_gender', db.String(255), nullable=False)
    citizen_address = db.Column('citizen_address', db.String(255), nullable=False)
    citizen_age = db.Column('citizen_age', db.Integer, nullable=False)
    citizen_contact = db.Column('citizen_contact', db.BigInteger, nullable=False)
    citizen_email = db.Column('citizen_email', db.String(255), nullable=False)
    citizen_license_number = db.Column('citizen_license_number', db.String(255), nullable=False)
    citizen_filename = db.Column('citizen_filename', db.String(255), nullable=False)
    citizen_filepath = db.Column('citizen_filepath', db.String(255), nullable=False)

    def as_dict(self):
        return {
            'citizen_id': self.citizen_id,
            'citizen_name': self.citizen_name,
            'citizen_gender': self.citizen_gender,
            'citizen_address': self.citizen_address,
            'citizen_age': self.citizen_age,
            'citizen_contact': self.citizen_contact,
            'citizen_email': self.citizen_email,
            'citizen_license_number': self.citizen_license_number,
            'citizen_filename': self.citizen_filename,
            'citizen_filepath': self.citizen_filepath
        }


db.create_all()
