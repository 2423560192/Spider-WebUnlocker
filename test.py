from datetime import datetime, timezone

current_time_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

print(current_time_ms)