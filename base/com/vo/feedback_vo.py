from base import db
from base.com.vo.login_vo import LoginVO


class FeedbackVO(db.Model):
    __tablename__ = "feedback_table"
    feedback_id = db.Column("feedback_id", db.Integer, primary_key=True, autoincrement=True)
    feedback_description = db.Column("feedback_description", db.String(255), nullable=False)
    feedback_rating = db.Column("feedback_rating", db.Integer, nullable=False)
    feedback_datetime = db.Column("feedback_datetime", db.DateTime)
    feedback_login_id = db.Column("feedback_login_id", db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'))

    def as_di1ct(self):
        return {

            "feedback_id": self.feedback_id,
            "feedback_description": self.feedback_description,
            "feedback_rating": self.feedback_rating,
            "feedback_datetime": self.feedback_datetime,
            "feedback_login_id": self.feedback_login_id,
        }


db.create_all()
