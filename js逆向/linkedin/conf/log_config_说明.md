# 日志配置文件说明

`log_config.json`文件用于配置系统的日志行为。以下是各配置项的详细说明：

## 基本配置

- `console_level`: 控制台日志输出级别（可选值: debug, info, warning, error, critical）
  - 当前值"info"表示输出INFO及以上级别的日志到控制台

- `file_level`: 文件日志输出级别（可选值同上）
  - 当前值"debug"表示将所有DEBUG及以上级别的日志记录到文件

- `log_file`: 日志文件名称，保存在logs目录下
  - 当前值设为"linkedin.log"

- `max_file_size`: 单个日志文件的最大大小（字节）
  - 当前值10485760约为10MB，超过此大小将创建新文件

- `backup_count`: 保留的日志文件备份数量
  - 当前值为5，表示当日志轮转时最多保留5个旧日志文件

## 模块级别配置

- `module_levels`: 各模块的日志级别单独配置，可以针对不同模块设置不同的日志级别
  - `__main__`: 主模块，设置为"info"
  - `thread_pool`: 线程池模块，设置为"warning"（仅输出警告及以上级别）
  - `proxy`: 代理模块，设置为"info"
  - `linkedin_unlocker`: LinkedIn解锁器模块，设置为"info"
  - `batch_login`: 批量登录模块，设置为"info"
  - `captcha_solver`: 验证码解决模块，设置为"info"

## 调试配置

- `debug_modules`: 需要临时调试的模块列表
  - 这些模块会忽略上面的配置，强制使用DEBUG级别
  - 当前仅对"proxy"模块启用DEBUG调试
  - 当您需要调试特定模块时，只需将模块名添加到此列表中

## 使用示例

日志级别从高到低为：CRITICAL > ERROR > WARNING > INFO > DEBUG

例如，如果需要调试验证码模块，可将配置修改为：
```json
"debug_modules": ["proxy", "captcha_solver"]
```

如果希望减少控制台输出，可将console_level设置为"warning"：
```json
"console_level": "warning"
``` 