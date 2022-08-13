from base import db
from base.com.vo.area_vo import AreaVO


class AreaDAO:
    def insert_area(self, area_vo):
        db.session.add(area_vo)
        db.session.commit()

    def view_area(self):
        area_vo_list = AreaVO.query.all()
        return area_vo_list

    def delete_area(self, area_vo):
        area_vo_list = AreaVO.query.get(area_vo.area_id)
        db.session.delete(area_vo_list)
        db.session.commit()

    def edit_area(self, area_vo):
        area_edit_list = AreaVO.query.filter_by(area_id=area_vo.area_id).all()
        return area_edit_list


    def update_area(self, area_vo):
        db.session.merge(area_vo)
        db.session.commit()
