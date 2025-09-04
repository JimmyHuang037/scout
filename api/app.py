#!/usr/bin/env python3

import sys
import os

# 将api目录添加到Python路径中
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.factory import create_app


if __name__ == '__main__':
    # 根据环境变量确定配置
    config_name = 'testing' if os.environ.get('FLASK_ENV') == 'testing' else 'default'
    
    # 创建并运行应用
    app = create_app(config_name)
    port = app.config.get('PORT', 5000)  # 默认端口5000，测试环境使用5010
    app.run(debug=True, host='0.0.0.0', port=port)