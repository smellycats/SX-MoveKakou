# -*- coding: utf-8 -*-
import os
import json
import base64
from functools import wraps

import arrow
from flask import g, Blueprint, request, jsonify

#from sqlalchemy import create_engine
from .. import app, limiter, logger, access_logger
from ..models import CarInfo
from .. import db
from ..helper_url import *
from ..helper import *

blueprint = Blueprint('car', __name__)

def verify_addr(f):
    """IP地址白名单"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or request.remote_addr == '127.0.0.1' or request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return {'status': '403.6',
                    'error': u'禁止访问:客户端的 IP 地址被拒绝'}, 403
        return f(*args, **kwargs)
    return decorated_function

def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not request.headers.get('Access-Token'):
                return {'status': '401.6', 'message': 'missing token header'}, 401
            token_result = verify_auth_token(request.headers['Access-Token'],
                                             app.config['SECRET_KEY'])
            if not token_result:
                return {'status': '401.7', 'message': 'invalid token'}, 401
            elif token_result == 'expired':
                return {'status': '401.8', 'message': 'token expired'}, 401
            g.uid = token_result['uid']
            g.scope = set(token_result['scope'])
        except Exception as e:
            logger.error(e)
            raise
        return f(*args, **kwargs)
    return decorated_function

def verify_scope(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            scope = '_'.join(request.blueprint, request.method.lower())
        except Exception as e:
            logger.error(e)
        if 'all' in g.scope or scope in g.scope:
            pass
        else:
            return {'status': 405, 'error': 'Method Not Allowed'}, 405
        return f(*args, **kwargs)
    return decorated_function

@blueprint.route('', methods=['POST'])
#@verify_addr
@limiter.limit("5000/hour")
#@verify_token
def index():
    try:
        if not request.json.get('img', None):
            error = {
                'resource': 'Car',
                'field': 'img',
                'code': 'missing_field'
            }
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422
        if request.json.get('wc', None) is None:
            error = {
                'resource': 'Car',
                'field': 'wc',
                'code': 'missing_field'
            }
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422
        if request.json.get('date_created', None):
            try:
                date_created = arrow.get(request.json['date_created']).datetime
            except Exception as e:
                error = {
                    'resource': 'Car',
                    'field': 'date_created',
                    'code': 'error format'
                }
                return jsonify(
                    {'message': 'Validation Failed', 'errors': error}), 400
        else:
            date_created = arrow.now().datetime
        # 当前时间
        t = arrow.now()
        # 图片路径
        path = os.path.join('imgs', t.format('YYYYMMDD'),
                            '%s.jpg' % t.format('HHmmssSSSSSS'))
        make_dirs(os.path.join('imgs', t.format('YYYYMMDD')))
        file=open(path, 'wb')
        file.write(base64.b64decode(request.json['img']))
        file.close()

        car = CarInfo(date_created=date_created, date_upload=t.datetime,
                      hphm=u'', wc=json.dumps(request.json['wc']),
                      img_path=path)
        db.session.add(car)
        db.session.commit()
    except Exception as e:
        print e

    return jsonify({'id': car.id, 'date_created': str(car.date_created),
                    'hphm': car.hphm, 'wc': car.wc,
                    'img_url': car.img_path}), 201

