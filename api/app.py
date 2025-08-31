import sys
import os
import argparse

# Add the api directory to the Python path
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.factory import create_app

# 解析命令行参数
parser = argparse.ArgumentParser(description='Run the Flask application')
parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
parser.add_argument('--test', action='store_true', help='Run in test mode with test database')
args, unknown = parser.parse_known_args()

# 设置环境变量
if args.test:
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['MYSQL_DB'] = 'school_management_test'

app = create_app('testing' if args.test else 'default')

if __name__ == '__main__':
    port = args.port
    app.run(debug=True, host='0.0.0.0', port=port)