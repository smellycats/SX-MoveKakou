# -*- coding: utf-8 -*-
import arrow

from kakou import db
from kakou.models import Users, Scope, CarInfo

def test_scope_get():
    scope = Scope.query.all()
    for i in scope:
        print i.name

def test_user_get():
    user = Users.query.filter_by(username='admin', banned=0).first()
    print user.scope

    
def test_hbc_get():
    hbc = Hbc.query.first()
    print hbc.hphm, hbc.kkdd_id

def test_hbc_add():
    datetime = '2013-05-11 21:23:58'
    t = arrow.get(datetime).replace(hours=-8)
    hbc = Hbc(date=t.format('YYYY-MM-DD'), jgsj=t.datetime, hphm='粤L12345',
              kkdd_id='441302002', hpys_code='BU', fxbh_code='IN', cdbh=5,
              imgurl='httP;//123', imgpath='c:123', banned=0)
    db.session.add(hbc)
    db.session.commit()
    print hbc.id

def test_car_add():
    car = CarInfo(date_created=arrow.now().datetime,
                  hphm=u'粤L12345', wc='[345.123,456,345]',
                  img_path=u'20140203\123.jpg')
    db.session.add(car)
    db.session.commit()

if __name__ == '__main__':
    #hpys_test()
    #hbc_add()
    #test_scope_get()
    #test_user_get()
    #test_hbc_get()
    #test_hbc_add()
    #test_hbcimg_get()
    #test_kkdd()
    print test_car_add()


