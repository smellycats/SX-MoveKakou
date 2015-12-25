# -*- coding: utf-8 -*-
import arrow

from kakou import db

class CarInfo(db.Model):
    """惠州黄标车数据"""
    __tablename__ = 'car_info'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    hphm = db.Column(db.String(16))
    wc = db.Column(db.String(255))
    img_path = db.Column(db.String(255))
    banned = db.Column(db.Integer, default=0)

    def __init__(self, date_created=None, hphm='', wc='', img_path='', banned=0):
        if date_created:
            self.date_created = arrow.now().datetime
        else:
            self.date_created = date_created
        self.hphm = hphm
        self.wc = wc
        self.img_path = img_path
        self.banned = banned

    def __repr__(self):
        return '<CarInfo %r>' % self.id

