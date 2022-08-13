from base import db
from base.com.vo.fine_receipt_vo import FineReceiptVO
from base.com.vo.citizendetails_vo import CitizenDetailsVO


class FineReceiptDAO:
    def insert_finereceipt(self, finereceipt_vo):
        db.session.add(finereceipt_vo)
        db.session.commit()

    def user_view_finereceipt(self):
        finereceipt_vo_list = db.session.query(CitizenDetailsVO, FineReceiptVO) \
            .filter(CitizenDetailsVO.citizen_id == FineReceiptVO.finereceipt_citizendetails_id) \
            .all()
        return finereceipt_vo_list


    def admin_view_finereceipt(self):
        finereceipt_vo_list = db.session.query(CitizenDetailsVO, FineReceiptVO) \
            .filter(CitizenDetailsVO.citizen_id == FineReceiptVO.finereceipt_citizendetails_id) \
            .all()
        return finereceipt_vo_list