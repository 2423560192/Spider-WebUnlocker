# 配置文件说明

`config.json`文件是系统的主要配置文件，包含了用于登录LinkedIn和处理验证码等功能的各项参数设置。以下是各配置项的详细说明：

## 基本配置

- `api_key`: 验证码服务API密钥
  - 用于调用外部验证码识别服务，当遇到验证码挑战时使用
  - 示例值: "cf823a34eaea4cd8bb67584c8dd7aeb2764679"

- `debug_mode`: 调试模式开关
  - 设置为true时会输出更多的调试信息
  - 默认值: false

- `timeout`: 网络请求超时时间（秒）
  - 所有HTTP请求的默认超时时间
  - 默认值: 30

- `retry_count`: 重试次数
  - 当请求失败时的最大重试次数
  - 默认值: 2

- `user_agent`: 浏览器标识
  - 模拟的浏览器User-Agent，用于HTTP请求头
  - 示例值: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

## 代理配置

- `proxy_api_url`: 代理服务API的URL
  - 用于获取代理IP的API接口地址
  - 此API应当返回文本格式的IP地址，格式通常为 "ip:port"
  - 系统会自动从返回的文本中提取IP和端口信息
  - 示例值: "http://api.your-proxy-provider.com/get-ip"

## 验证码配置

- `captcha_max_wait_time`: 验证码最大等待时间（秒）
  - 等待验证码解决结果的最长时间，超过此时间将视为失败
  - 默认值: 20

- `captcha_check_interval`: 验证码检查间隔（秒）
  - 检查验证码解决结果的时间间隔
  - 默认值: 3

- `captcha_log_interval`: 验证码日志间隔（秒）
  - 记录验证码处理进度日志的时间间隔
  - 默认值: 15

- `use_async_captcha`: 是否使用异步验证码处理
  - 设置为true表示启用异步方式处理验证码，可以提高成功率
  - 默认值: true

- `captcha_concurrent_tasks`: 验证码并发任务数
  - 异步处理验证码时的并发任务数量
  - 默认值: 2

- `captcha_max_retries`: 验证码最大重试次数
  - 处理验证码失败时的最大重试次数
  - 默认值: 3

- `captcha_connection_timeout`: 验证码服务连接超时（秒）
  - 连接验证码服务API的超时时间
  - 默认值: 10

## 使用说明

1. 首次使用前，请确保填写正确的`api_key`和`proxy_api_url`
2. 如需调试，可将`debug_mode`设置为true
3. 如果频繁遇到验证码解决失败的情况，可以尝试：
   - 增加`captcha_max_wait_time`（最长等待时间）
   - 增加`captcha_concurrent_tasks`（并发任务数）
   - 确保`use_async_captcha`设置为true

## 配置示例

以下是一个完整的配置示例：

```json
{
  "api_key": "your_api_key_here",
  "debug_mode": false,
  "timeout": 30,
  "retry_count": 2,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
  "proxy_api_url": "http://api.your-proxy-provider.com/get-ip",
  "captcha_max_wait_time": 20,
  "captcha_check_interval": 3,
  "captcha_log_interval": 15,
  "use_async_captcha": true,
  "captcha_concurrent_tasks": 2,
  "captcha_max_retries": 3,
  "captcha_connection_timeout": 10
}
``` 