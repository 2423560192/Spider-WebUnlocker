import base64
from urllib.parse import quote


def generate_requests_cookie(session_key: str, session_value: str):
    # 对 key 编码：带引号 -> base64 -> URL编码
    key_quoted = '"' + session_key + '"'
    key_base64 = base64.b64encode(key_quoted.encode('latin1')).decode()
    key_encoded = quote(key_base64)

    # 对 value 编码：带引号 -> base64（不需要 URL 编码）
    value_quoted = '"' + session_value + '"'
    value_base64 = base64.b64encode(value_quoted.encode()).decode()

    # 返回 requests 可用 cookie 字典
    return {
        key_encoded: value_base64
    }


# 示例：
cookies = generate_requests_cookie(
    session_key="wk_fnJfkjbR_CHaFhG4sPftpCHTzG5y4TM2kfbREsAMx_clientSession",
    session_value="dae3eb73-9b7f-4225-bcb1-173d9af7b8f5"
)

print("requests cookies 字典：")
print(cookies)
