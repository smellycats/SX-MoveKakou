# -*- coding: cp936 -*-
#import cgs

from cgs.models import Users, Scope, GDVehicle, HbcAll, HZVehicle, MyView
#from . import test

def user_get():
    user = Users.query.all()
    for i in user:
        print i.username

def scope_get():
    s = Scope.query.all()
    for i in s:
        print i.name

def gdvehicle_get():
    s = GDVehicle.query.first()
    print s.hphm, s.hpzl

def hbcall_get():
    h = HbcAll.query.first()
    print h.hphm

def hzvehicle_get():
    h = HZVehicle.query.first()
    print h.hphm

def view_get():
    h = session.query(MyView).first()
    print h


if __name__ == "__main__":
    #hbcall_get()
    #hzvehicle_get()
    view_get()
