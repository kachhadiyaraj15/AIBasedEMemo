from base import db
from base.com.vo.login_vo import LoginVO


class ComplainVO(db.Model):
    __tablename__ = "complain_table"
    complain_id = db.Column("complain_id", db.Integer, primary_key=True, autoincrement=True)
    complain_subject = db.Column("complain_subject", db.String(255), nullable=False)
    complain_description = db.Column("complain_description", db.String(255), nullable=False)
    complain_datetime = db.Column("complain_datetime", db.DateTime)
    complain_status = db.Column("complain_status", db.String(20))
    complain_from_login_id = db.Column("complain_from_login_id", db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'))
    complain_to_login_id = db.Column("complain_to_login_id", db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'))
    complain_reply_description = db.Column("complain_reply_description", db.String(255))
    complain_reply_datetime = db.Column("complain_reply_datetime", db.DateTime)

    def as_di1ct(self):
        return {
            "complain_id": self.complain_id,
            "complain_subject": self.complain_subject,
            "complain_description": self.complain_description,
            "complain_datetime": self.complain_datetime,
            "complain_status": self.complain_status,
            "complain_from_login_id": self.complain_from_login_id,
            "complain_to_login_id": self.complain_to_login_id,
            "complain_reply_description": self.complain_reply_description,
            "complain_reply_datetime": self.complain_reply_datetime,
        }


db.create_all()
