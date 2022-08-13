from base import db


class LoginVO(db.Model):
    __tablename__ = 'login_table'
    login_id = db.Column('login_id', db.Integer, primary_key=True, autoincrement=True)
    login_username = db.Column('login_username', db.String(100), nullable=False)
    login_password = db.Column('login_password', db.String(100), nullable=False)
    login_role = db.Column('login_role', db.String(100), nullable=False)
    login_status = db.Column('login_status', db.String(100), nullable=False)
    login_secretkey = db.Column('login_secretkey', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'login_status': self.login_status,
            'login_secretkey': self.login_secretkey
        }


db.create_all()
