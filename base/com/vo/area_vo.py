from base import db


class AreaVO(db.Model):
    __tablename__ = 'area_table'
    area_id = db.Column('area_id', db.Integer, primary_key=True, autoincrement=True, onupdate='CASCADE')
    area_name = db.Column('area_name', db.String(255), nullable=False)
    area_pincode = db.Column('area_pincode', db.Integer, nullable=False)

    def as_dict(self):
        return {
            'area_id': self.area_id,
            'area_name': self.area_name,
            'area_pincode': self.area_pincode
        }


db.create_all()
