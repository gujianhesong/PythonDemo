"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors


def open_db():
    # print("打开数据库")
    global connection
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     db='joke',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print("打开数据库出错：", e)


def close_db():
    # print("关闭数据库")
    try:
        connection.close()
    except Exception as e:
        print("关闭数据库出错：", e)


# ----------------------------------------------

# 保存joke
def insert_joke(joke_info):
    sql = "INSERT INTO joke (id_from_src, theme_id, type, text, user_id, user_name, user_head, src, up, down, comment, forward, passtime, cate, obj_url, download_url, thumb_url, width, height, duration, top_comments) " \
          "VALUES " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (joke_info["id_from_src"], joke_info["theme_id"], joke_info["type"], joke_info["text"],
                             joke_info["user_id"], joke_info["user_name"], joke_info["user_head"], joke_info["src"],
                             joke_info["up"], joke_info["down"], joke_info["comment"],
                             joke_info["forward"], joke_info["passtime"], joke_info["cate"],
                             joke_info["obj_url"], joke_info["download_url"], joke_info["thumb_url"],
                             joke_info["width"], joke_info["height"], joke_info["duration"],
                             joke_info["top_comments"]
                             ))
        connection.commit()


# 判断是否存在joke
def check_has_joke(id_from_src):
    sql = "SELECT id_from_src FROM joke WHERE id_from_src = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (id_from_src))
        results = cursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False


# ----------------------------------------------


# 保存joke
def insert_joke_xiubai(joke_info):
    sql = "INSERT INTO joke_xiubai (id_from_src, theme_id, type, text, user_id, user_name, user_head, src, up, down, comment, forward, passtime, cate, obj_url, download_url, thumb_url, width, height, duration, top_comments) " \
          "VALUES " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (joke_info["id_from_src"], joke_info["theme_id"], joke_info["type"], joke_info["text"],
                             joke_info["user_id"], joke_info["user_name"], joke_info["user_head"], joke_info["src"],
                             joke_info["up"], joke_info["down"], joke_info["comment"],
                             joke_info["forward"], joke_info["passtime"], joke_info["cate"],
                             joke_info["obj_url"], joke_info["download_url"], joke_info["thumb_url"],
                             joke_info["width"], joke_info["height"], joke_info["duration"],
                             joke_info["top_comments"]
                             ))
        connection.commit()


# 判断是否存在joke
def check_has_joke_xiubai(id_from_src):
    sql = "SELECT id_from_src FROM joke_xiubai WHERE id_from_src = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (id_from_src))
        results = cursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False
