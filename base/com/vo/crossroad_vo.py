from base import db
from base.com.vo.area_vo import AreaVO


class CrossroadVO(db.Model):
    __tablename__ = 'crossroad_table'
    crossroad_id = db.Column('crossroad_id', db.Integer, primary_key=True, autoincrement=True)
    crossroad_name = db.Column('crossroad_name', db.String(255), nullable=False)
    crossroad_area_id = db.Column('crossroad_area_id', db.Integer, db.ForeignKey(AreaVO.area_id, ondelete='CASCADE', onupdate='CASCADE'))

    def as_dict(self):
        return {
            'crossroad_id': self.crossroad_id,
            'crossroad_name': self.crossroad_name,
            'crossroad_area_id': self.crossroad_area_id
        }


db.create_all()
