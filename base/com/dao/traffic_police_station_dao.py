from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.traffic_police_station_vo import TrafficPoliceStationVO
from base.com.vo.login_vo import LoginVO


class TrafficPoliceStationDAO:
    def insert_user(self, traffic_police_station_vo):
        db.session.add(traffic_police_station_vo)
        db.session.commit()

    def view_user(self):
        traffic_police_station_vo_list = db.session.query(AreaVO, LoginVO, TrafficPoliceStationVO) \
            .filter(AreaVO.area_id == TrafficPoliceStationVO.traffic_police_station_area_id) \
            .filter(LoginVO.login_id == TrafficPoliceStationVO.traffic_police_station_login_id) \
            .all()
        return traffic_police_station_vo_list
