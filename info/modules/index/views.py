from . import index_blu
from flask import render_template, session,request,jsonify
from flask import current_app
from info.models  import User, News, Category
from info import constants
from info import create_app
from info.utils.response_code import RET


@index_blu.route('/newslist')
def get_news_list():
    args_dict = request.args
    page = args_dict.get("p", "1")
    per_page = args_dict.get("per_page", constants.HOME_PAGE_MAX_NEWS)
    category_id = args_dict.get("cid", 1)
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg = "参数错误")

    filter = []
    if category_id != "1":
        filter.append(News.category_id == category_id)
    try:
        paginate = News.query.filter(*filter).order_by(News.create_time.desc()).paginate(page, per_page, False)
        items = paginate.items
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    news_li = []
    for news in items if items else []:
        news_li.append(news.to_basic_dict())
    return jsonify(errno=RET.OK, ermsg="ok", totalPage=total_page, current_age=current_page,newsList=news_li, cid=category_id)


@index_blu.route('/')
def index():
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    news_list = None
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_new_list = []
    for news in news_list if news_list else []:
        news.to_dict()
        click_new_list.append(news.to_basic_dict())
    categories = Category.query.all()
    categories_dicts = []
    for category in categories if categories else []:
        categories_dicts.append(category.to_dict())

    data = { "user_info":user.to_dict() if user else None,
             "click_news_list":click_new_list,
             "categories":categories_dicts}

    return render_template('news/index.html', data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')

