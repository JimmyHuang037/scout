# 项目重构说明

本文档记录了对API项目的重构过程和关键变更。

## 重构目标

1. 改善项目结构，提高代码可维护性
2. 确保所有模块导入路径正确
3. 保持应用功能完整性和可运行性

## 主要变更

### 1. 目录结构调整

- 创建 `apps` 目录用于存放核心应用组件
- 将 `blueprints`、`services` 和 `utils` 移动到 `apps` 目录中
- 保持 `app.py` 和 `config.py` 在项目根目录

重构前结构：
```
api/
├── app/
│   ├── blueprints/
│   ├── services/
│   └── utils/
├── app.py
└── config.py
```

重构后结构：
```
api/
├── apps/
│   ├── blueprints/
│   ├── services/
│   └── utils/
├── app.py
└── config.py
```

### 2. 导入路径更新

所有模块导入路径已更新为使用新的 `apps` 结构：
- 蓝图导入：`from apps.blueprints.module import function`
- 服务导入：`from apps.services import ServiceName`
- 工具导入：`from apps.utils import utility`

### 3. 日志系统规范

- 使用Flask内置日志系统，不再使用自定义日志实现
- 在业务代码中使用 `current_app.logger` 记录日志
- 禁止直接使用 `logging` 模块
- 移除所有文件中的 `import logging` 语句

### 4. 应用工厂模式

- 保持应用工厂类在 `app.py` 中
- 确保应用入口点简洁明了
- 所有蓝图在工厂中统一注册

## 验证结果

应用已成功启动并正常运行，所有API端点可正常访问。