from flask import Flask, request, render_template, redirect, url_for, flash  
import sqlite3  
from sqlite3 import Error  
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # 用于闪现消息  
  
def init_db():  
    """ 初始化数据库，创建表 """  
    try:  
        conn = sqlite3.connect('messages.db')  
        cursor = conn.cursor()  
        cursor.execute('''  
            CREATE TABLE IF NOT EXISTS messages (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                username TEXT NOT NULL,  
                message TEXT NOT NULL,  
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            )  
        ''')  
        conn.commit()  
        conn.close()  
    except Error as e:  
        print(e)  
  
# 可以在这里调用init_db()，或者通过运行一个单独的脚本来初始化数据库  
init_db()  
  
@app.route('/')  
def index():  
    """ 显示留言板页面和所有留言 """  
    try:  
        conn = sqlite3.connect('messages.db')  
        cursor = conn.cursor()  
        cursor.execute('SELECT id, username, message, timestamp FROM messages ORDER BY timestamp DESC')  
        messages = cursor.fetchall()  
        conn.close()  
        return render_template('index.html', messages=messages)  
    except Error as e:  
        flash('数据库错误: ' + str(e), 'error')  
        return redirect(url_for('index'))  
  
@app.route('/', methods=['POST'])  
def add_message():  
    """ 处理表单提交，添加新留言 """  
    if not request.form['username'] or not request.form['message']:  
        flash('用户名和消息都不能为空', 'error')  
        return redirect(url_for('index'))  
  
    try:  
        conn = sqlite3.connect('messages.db')  
        cursor = conn.cursor()  
        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)',  
                       (request.form['username'], request.form['message']))  
        conn.commit()  
        conn.close()  
        flash('留言已添加', 'success')  
    except Error as e:  
        flash('数据库错误: ' + str(e), 'error')  
  
    return redirect(url_for('index'))  
  

# 开启debug 
if __name__ == '__main__':
    app.run(debug=True, port=3000) # 修改端口

