# LinkedIn 账号自动登录与验证解锁工具

这是一个用于批量自动登录LinkedIn账号并处理验证挑战的工具。该工具支持批量处理账号登录、验证码识别、代理IP管理等功能，并提供了详细的日志记录和结果报告。

## 项目结构

- `linkedin_unlocker.py`: 核心登录模块，负责LinkedIn账号的登录和验证处理
- `captcha_solver.py`: 验证码解决方案，处理LinkedIn登录过程中的验证码挑战
- `proxy.py`: 代理IP管理模块，负责获取和管理代理IP
- `batch_login.py`: 批量登录处理模块，使用线程池实现并发登录
- `thread_pool.py`: 线程池管理模块，提供高效的并发任务处理
- `config.json`: 配置文件，包含账号信息、API密钥和其他设置

## 功能特性

- **批量账号登录**: 支持从文件中批量读取账号信息并执行登录操作
- **验证码自动处理**: 自动识别和处理LinkedIn的验证码挑战
- **代理IP管理**: 支持使用代理IP进行登录，避免IP限制
- **随机UA**: 随机使用不同User-Agent进行登录，模拟不同浏览器环境
- **并发处理**: 使用线程池实现高效的并发账号处理
- **结果报告**: 自动生成Excel格式的登录结果报告
- **详细日志**: 提供详细的日志记录，便于问题排查

## 安装与配置

### 环境要求

- Python 3.6+
- 必要的Python库: requests, beautifulsoup4, pandas, concurrent.futures

### 安装步骤

1. 克隆或下载本项目到本地
2. 安装所需依赖:
   ```
   pip install -r requirements.txt
   ```
3. 配置`config.json`文件:
   ```json
   {
     "username": "你的LinkedIn账号",
     "password": "你的LinkedIn密码",
     "api_key": "验证码服务API密钥",
     "debug_mode": false,
     "timeout": 30,
     "retry_count": 3,
     "user_agent": "User-Agent字符串"
   }
   ```

## 使用方法

### 单个账号登录

使用以下命令执行单个账号登录:

```
python linkedin_unlocker.py
```

这将使用`config.json`中配置的账号信息进行登录。

### 批量账号登录

准备一个包含账号信息的文本文件，每行一个账号，格式为`用户名,密码`，然后执行以下命令:

```
python batch_login.py accounts.txt [输出目录] [账号间延迟秒数] [最大并发数]
```

参数说明:
- `accounts.txt`: 包含账号信息的文件路径
- `输出目录`: 结果输出目录，默认为`login_results`
- `账号间延迟秒数`: 提交任务之间的延迟，默认为30秒
- `最大并发数`: 最大并发任务数，默认为5

例如:
```
python batch_login.py accounts.txt results 60 5
```

### 配置代理

修改`config.json`文件，添加代理API配置:

```json
{
  "proxy_api_url": "http://api.your-proxy-provider.com/get-ip"
}
```

代理配置说明:
- `proxy_api_url`: 代理API的URL，用于获取代理IP
- API应返回文本格式的IP地址，格式通常为 "ip:port" 或包含IP:端口格式的文本
- 系统会自动从返回的文本中提取IP和端口信息

如果不配置代理参数，系统将使用默认值，但建议配置自己的代理API地址以获得更好的服务质量。

### 验证码解决方案配置

默认使用外部API服务解决验证码。在`config.json`中配置相关API信息:

```json
{
  "api_key": "验证码API密钥",
  "api_url": "验证码API的URL",
  "result_url": "结果查询API的URL",
  "surl": "服务URL"
}
```

## 性能优化

本工具已进行了以下性能优化:

1. **并发处理**: 使用线程池进行并发账号处理，提高批量处理效率
2. **指数退避重试**: 登录失败时采用指数退避策略进行重试，减少资源消耗
3. **代理IP轮换**: 自动获取新的代理IP，避免IP被封禁
4. **会话复用**: 使用`requests.Session`保持会话，减少连接建立开销
5. **随机UA**: 使用随机User-Agent，减少被反爬系统识别的风险

## 常见问题

### 登录失败的原因及解决方法

1. **账号密码错误**: 请检查账号信息是否正确
2. **需要二次验证**: 程序会自动处理验证码挑战，但对于需要手机/邮箱验证的账号可能需要手动处理
3. **IP被封禁**: 尝试使用代理IP或减少登录频率
4. **验证码识别失败**: 检查验证码API配置和服务状态

### 提高成功率的技巧

1. 使用高质量的代理IP
2. 减少并发数和提高账号间延迟
3. 确保账号近期登录过，减少触发验证的概率
4. 定期变更User-Agent配置

## 法律风险声明

**重要提示：** 使用本工具可能违反LinkedIn的服务条款。LinkedIn明确禁止：

1. 使用自动化工具、脚本、爬虫或浏览器插件访问LinkedIn服务
2. 规避LinkedIn的安全措施或访问限制
3. 收集、存储或分发LinkedIn用户数据

以下是LinkedIn服务条款相关条款摘录：

> LinkedIn不允许使用任何第三方软件，包括"爬虫"、机器人、浏览器插件或浏览器扩展程序来抓取、修改外观或自动执行LinkedIn网站上的活动。这些工具违反了用户协议。

违反LinkedIn服务条款可能导致以下后果：
- 您的LinkedIn账号被限制或永久关闭
- 法律责任，包括可能的诉讼
- 访问LinkedIn服务的IP被封禁

**使用风险自负：** 本工具仅供学习和研究目的，作者不对因使用本工具而导致的任何问题或损失负责。在使用前，请充分了解相关风险并遵守LinkedIn的服务条款和适用法律。

## 注意事项

- 本工具仅供学习和研究使用，请遵守LinkedIn的使用条款
- 频繁登录可能导致账号被临时限制，请合理使用
- 建议使用代理IP，避免本地IP被封禁
- 对于需要二次验证的账号，可能需要手动处理

## 开发者信息

如需贡献代码或报告问题，请提交Issue或Pull Request。

## 版权信息

本项目仅供学习交流使用，请勿用于商业用途。

## 日志配置

项目使用了统一的日志配置系统，可以通过`log_config.json`文件调整日志输出行为。

### 日志配置项

- `console_level`: 控制台日志级别 (debug, info, warning, error)
- `file_level`: 文件日志级别
- `log_file`: 日志文件名，保存在logs目录下
- `max_file_size`: 日志文件最大大小（字节）
- `backup_count`: 保留的日志文件备份数量
- `module_levels`: 各模块的日志级别配置
- `debug_modules`: 需要临时调试的模块列表

### 示例配置

```json
{
    "console_level": "info",
    "file_level": "info", 
    "log_file": "linkedin.log",
    "max_file_size": 10485760,
    "backup_count": 5,
    "module_levels": {
        "__main__": "info",
        "thread_pool": "warning",
        "proxy": "warning",
        "linkedin_unlocker": "info",
        "batch_login": "info",
        "captcha_solver": "warning"
    },
    "debug_modules": []
}
```

通过修改`debug_modules`数组，可以临时将某些模块的日志级别设置为debug级别，方便调试。 