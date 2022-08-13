from base import db
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO



class ComplainDAO:
    def insert_complain(self, complain_vo):
        db.session.add(complain_vo)
        db.session.commit()

    def user_view_complain(self):
        complain_vo_list = db.session.query(LoginVO, ComplainVO) \
            .filter(LoginVO.login_id == ComplainVO.complain_from_login_id) \
            .all()
        return complain_vo_list

    def admin_view_complain(self):
        complain_vo_list = db.session.query(ComplainVO, LoginVO) \
            .join(LoginVO, ComplainVO.complain_from_login_id == LoginVO.login_id).all()
        return complain_vo_list

    def delete_complain(self, complain_vo):
        complain_vo_list = ComplainVO.query.get(complain_vo.complain_id)
        db.session.delete(complain_vo_list)
        db.session.commit()

    def edit_complain(self, complain_vo):
        complain_vo_list = ComplainVO.query.get(complain_vo.complain_id)
        return complain_vo_list

    def update_reply(self, complain_vo):
        db.session.merge(complain_vo)
        db.session.commit()
