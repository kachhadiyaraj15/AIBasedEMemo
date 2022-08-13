from base import db
from base.com.vo.citizendetails_vo import CitizenDetailsVO


class FineReceiptVO(db.Model):
    __tablename__ = 'finereceipt_table'
    finereceipt_id = db.Column('fine_recipt_id', db.Integer, primary_key=True, autoincrement=True)
    finereceipt_reason = db.Column('finereceipt_reason', db.String(255), nullable=False)
    finereceipt_amount = db.Column('finereceipt_amount', db.Integer, nullable=False)
    finereceipt_datetime = db.Column('finereceipt_datetime', db.DateTime)
    finereceipt_citizendetails_id = db.Column('finereceipt_citizendetails_id', db.Integer,
                                              db.ForeignKey(CitizenDetailsVO.citizen_id, ondelete='CASCADE', onupdate='CASCADE'))

    def as_dict(self):
        return {
            'finereceipt_id': self.finereceipt_id,
            'finereceipt_reason': self.finereceipt_reason,
            'finereceipt_amount': self.finereceipt_amount,
            'finereceipt_datetime': self.finereceipt_datetime,
            'finereceipt_citizendetails_id': self.finereceipt_citizendetails_id
        }


db.create_all()
