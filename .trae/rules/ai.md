# AI 助手规则与指令

## 语言偏好
- 无论输入语言如何，均以中文回复。

## 系统状态检查命令
- os_version: cat /etc/os-release
- kernel_version: uname -r
- architecture: uname -m
- system_load: uptime
- disk_usage: df -h
- memory_usage: free -h

## 其他指令
- 在提出更改建议前，始终验证文件路径是否存在于提供的上下文中。
- 切勿对上下文中不存在的文件虚构代码更改。
- 优先考虑如何实施任务的想法。
- 仅使用提供的工具。
- 在使用任何编辑工具之前，如果不知道文件内容，首先使用 view_files。
- 在设计和对话中保持简洁。