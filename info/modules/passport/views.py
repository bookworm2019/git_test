from flask import current_app, jsonify
from flask import make_response
from flask import request
from info import constants
from info import redis_store
from info.utils.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu

@passport_blu.route('/image_code')
def get_image_code():
    code_id = request.args.get('code_id')
    print(code_id)

    name, text, image = captcha.captcha.generate_captcha()
    try:
        redis_store.setex('ImageCode' + code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(error=RET.DATAERR, errmsg = "保存图片验证码失败"))

    resp = make_response(image)
    resp.headers['Content-Type'] = 'image/JPEG'
    return resp




















