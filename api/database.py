import mysql.connector
from flask import current_app, g
import click
from flask.cli import with_appcontext


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
    return g.db


def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


def init_app(app):
    """初始化应用数据库"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库命令"""
    # 这里可以添加数据库初始化逻辑
    click.echo('Database initialized.')