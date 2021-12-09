from flask import Flask
from redis import Redis
from flask_sse import sse
from flask import request, abort
from flask import jsonify
import traceback
from flask_uwsgi_websocket import GeventWebSocket
import time
from util.log_utils import logger as LOG
from models.db import initialize_db
from models.models import NotiMessage, UserReadMessage
from service.message_service import get_message_by_group_ids1, read_message, get_group_ids,\
     is_have_message, save_new_message, update_message_status, get_message_by_group_ids, count_message_by_group_ids
app = Flask(__name__)
# app.wsgi_app = AuthMiddleWare(app.wsgi_app)
websocket = GeventWebSocket(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'notify_db',
    'host': 'notify-db',
    'port': 27017,
    'username':'admin',
    'password':'adminpwd',
    'connect': False,
}

initialize_db(app)

redis = Redis(host='redis', port=6379)

CHANNEL='notifications_channel'
pub = redis.pubsub()

@websocket.route('/ws/notification/<group_ids>')
def echo(ws, group_ids):
    pub.subscribe(CHANNEL)
    while True:
        msg = get_redis_message()
        if msg:
            # str_mess = str(msg)+'-'+client_id
            # ws.send(str_mess.encode('utf-8'))
            LOG.info('---------')
            LOG.info(msg)
            if is_have_message(group_ids, msg):
                LOG.info('....')
                ws.send(msg)
        time.sleep(1)

@websocket.route('/echo')
def echo1(ws):
    while True:
        msg = ws.receive()
        if msg:
            ws.send(msg)
        time.sleep(1)


# def send_message_to_ws(ws, group_ids, msg):
#     try:
#         client1 ='"{}"'.format(group_id)
#         client2 =client1.replace('"',"'")
#         print(client1)
#         print(client2)
#         if client1 in str(msg) or client2 in str(msg):
#             print('send.....')
#             ws.send(msg)
#         else:
#             print('not send.....')
#             print(str(msg))
#     except Exception as e:
#         LOG.exception(e)
#         print(e)
def get_socket_message_and_send(ws):
    msg = ws.receive()
    # ws.send(msg)
    if msg:
        redis.publish(
            channel=CHANNEL,
            message=msg
        ) 
    return msg 
def get_redis_message():
    data = pub.get_message()
    LOG.info(data)
    if data:
        message = data['data']
        if message and message != 1:
            return message
    return None
def publish_message(data, channel=CHANNEL):
    redis.publish(
        channel=channel,
        message=str(data)
    )

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api/v1/notifications/push', methods = ['POST'])
def push_notification():
    data =request.get_json(force=True)
    print(data)
    LOG.info(data)
    publish_message(data, CHANNEL)
    save_new_message(data)
    return 'ok'

@app.route('/api/v1/notifications/<client_id>', methods=['GET'])
def get_message(client_id):
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    status = request.args.get('status')
    group_ids = request.args.get('group_ids')
    message = get_message_by_group_ids1(client_id, group_ids, status, limit, offset)
    LOG.info(message)
    if not message:
        return jsonify({'error': 'data not found'})
    return jsonify(message)

@app.route('/api/v1/notifications/messages/<id>', methods=['PUT'])
def update_message_status(id):
    record = request.get_json(force=True)
    message = update_message_status(id, record['status'])
    if not message:
        return jsonify({'error': 'data not found'})
    return jsonify(message)

@app.route('/api/v1/notifications/messages/read', methods=['POST'])
def mark_message_read():
    record = request.get_json(force=True)
    return read_message(record)
    
@app.route('/api/v1/notifications/messages/<client_id>/count', methods=['GET'])
def get_status_count(client_id):
    status = request.args.get('status')
    group_ids = request.args.get('group_ids')
    message = count_message_by_group_ids(client_id, group_ids, status)
    LOG.info(message)
    if not message:
        return jsonify({'error': 'data not found'})
    return message
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
