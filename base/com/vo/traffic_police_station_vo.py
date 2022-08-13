from base import db
from base.com.vo.login_vo import LoginVO
from base.com.vo.area_vo import AreaVO


class TrafficPoliceStationVO(db.Model):
    __tablename__ = 'traffic_police_station_table'

    traffic_police_station_id = db.Column('traffic_police_station_id', db.Integer, primary_key=True, autoincrement=True)
    traffic_police_station_name = db.Column('traffic_police_station_name', db.String(100), nullable=False)
    traffic_police_head_name = db.Column('traffic_police_head_name', db.String(100), nullable=False)
    traffic_police_head_contact = db.Column('traffic_police_head_contact', db.Numeric, nullable=False)
    traffic_police_station_login_id = db.Column('traffic_police_station_login_id', db.Integer,
                                                db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'))
    traffic_police_station_area_id = db.Column('traffic_police_station_area_id', db.Integer,
                                               db.ForeignKey(AreaVO.area_id, ondelete='CASCADE', onupdate='CASCADE'))

    def as_dict(self):
        return {
            'traffic_police_station_id': self.traffic_police_station_id,
            'traffic_police_station_name': self.traffic_police_station_name,
            'traffic_police_station_area_id': self.traffic_police_station_area_id,
            'traffic_police_head_name': self.traffic_police_head_name,
            'traffic_police_head_contact': self.traffic_police_head_contact,
            'traffic_police_station_login_id': self.traffic_police_station_login_id,

        }


db.create_all()
