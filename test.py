import redis
import json
from tqdm import tqdm

# 连接你的 Upstash Redis
r = redis.Redis(
    host='amused-bream-11167.upstash.io',  # 例：xxx.upstash.io
    port=6379,
    password='ASufAAIjcDE4Y2Q5ZGY3ZDQ3OTc0ZmU5OTI3YzZlMWFmZjMyZDY2ZXAxMA',
    ssl=True,
    decode_responses=True
)

# 获取所有 key
keys = list(r.scan_iter())
print(f"共发现 {len(keys)} 个键，正在导出...")

# 存储数据的结构
backup_data = {}

# 遍历所有 key，并根据类型分别处理
for key in tqdm(keys):
    try:
        key_type = r.type(key)

        if key_type == 'string':
            backup_data[key] = {'type': 'string', 'value': r.get(key)}

        elif key_type == 'hash':
            backup_data[key] = {'type': 'hash', 'value': r.hgetall(key)}

        elif key_type == 'list':
            backup_data[key] = {'type': 'list', 'value': r.lrange(key, 0, -1)}

        elif key_type == 'set':
            backup_data[key] = {'type': 'set', 'value': list(r.smembers(key))}

        elif key_type == 'zset':
            backup_data[key] = {'type': 'zset', 'value': r.zrange(key, 0, -1, withscores=True)}

        else:
            print(f"⚠️ 未支持的类型: {key_type}, key: {key}")

    except Exception as e:
        print(f"❌ 获取 {key} 失败: {e}")

# 写入文件
with open("redis_backup.json", "w", encoding="utf-8") as f:
    json.dump(backup_data, f, ensure_ascii=False, indent=2)

print("✅ 导出完成，保存在 redis_backup.json")
