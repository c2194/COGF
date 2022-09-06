
import pymysql



# 打开数据库连接
try:
    db = pymysql.connect(host='localhost', user='muser', passwd='muser', port=3306, db='muser')
    print('连接成功！')
except:
    print('something wrong!')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# SQL 更新语句
sql = "INSERT INTO `test` (`tid`, `tint`, `tname`) VALUES (NULL, '123', 'ab c');"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    print('数据更新成功！')
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()

