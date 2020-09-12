import datetime
import flask
import hashlib
import hmac
import json
import os

app = flask.Flask(__name__)

TELEGRAM_BOT_ID     = os.environ['TELEGRAM_BOT_ID']
TELEGRAM_BOT_DOMAIN = os.environ['TELEGRAM_BOT_DOMAIN']
TELEGRAM_BOT_SECRET = os.environ['TELEGRAM_BOT_SECRET']

@app.route('/')
def index():
    return flask.render_template('index.htm',
        TELEGRAM_BOT_ID=TELEGRAM_BOT_ID,
        TELEGRAM_BOT_DOMAIN=TELEGRAM_BOT_DOMAIN,
    )

@app.route('/telegram-auth-callback/')
def telegram_auth_callback():
    now_timestamp = datetime.datetime.now().timestamp()

    arg_id = flask.request.args.get('id')
    arg_firstname = flask.request.args.get('first_name')
    arg_username = flask.request.args.get('username')

    # check hash
    arg_hash = flask.request.args.get('hash')
    data_check_str = flask.request.args
    data_check_str = data_check_str.items()
    data_check_str = filter(lambda i:i[0]!='hash',data_check_str)
    data_check_str = sorted(data_check_str)
    data_check_str = map(lambda i:f"{i[0]}={i[1]}",data_check_str)
    data_check_str = "\n".join(data_check_str)
    secret_key_bin = sha256_bin(TELEGRAM_BOT_SECRET)
    expected_hash_str = hmacsha256_str(secret_key_bin, data_check_str)
    if arg_hash != expected_hash_str:
        return error_4xx('WOQSSLZA bad hash')

    # check timestamp
    arg_authdate = flask.request.args.get('auth_date')
    arg_authdate_int = int(arg_authdate)
    if abs(arg_authdate_int-now_timestamp) > 10:
        return error_4xx('JOBPKXAG bad auth_date')

    return flask.render_template(
        'telegram_auth_callback.htm',
        user_id = flask.request.args.get('id'),
        user_name = flask.request.args.get('username'),
    )

def error_4xx(err_msg):
    return flask.render_template('error_4xx.htm',err_msg=err_msg), 400

def sha256_bin(msg_str):
    m = hashlib.sha256()
    m.update(msg_str.encode('utf8'))
    return m.digest()

def hmacsha256_str(key_bin, msg_str):
    return hmac.new(
        key=key_bin,
        msg=msg_str.encode('utf8'),
        digestmod=hashlib.sha256,
    ).hexdigest()
