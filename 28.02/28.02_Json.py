
logs = [
    "2025-02-01 10:15:33|INFO|user=anna action=login status=success ip=10.0.0.1",
    "2025-02-01 10:17:10|ERROR|user=bob action=payment status=fail amount=120",
    "2025-02-01 10:20:01|INFO|user=anna action=logout status=success",
    "2025-02-01 10:22:45|WARNING|user=anna action=payment status=fail amount=300",
    "2025-02-01 10:30:12|ERROR|user=tom action=login status=fail ip=10.0.0.5"
]
def parse_line(line):
    parts = line.split("|")
    date = parts[0]
    level = parts[1]
    message = parts[2]
    fields = message.split(" ")
    data = {}
    for f in fields:
        if "=" in f:
            key, value = f.split("=")
            if value.isdigit():
                value = int(value)
            data[key] = value
    data["date"] = date
    data["level"] = level
    return data
def parse_all_logs(log_lines):
    result = []
    for line in log_lines:
        result.append(parse_line(line))
    return result
import json
def save_to_json(data, filename="logs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def filter_logs(logs_list, **kwargs):
    filtered = []
    for log in logs_list:
        match = True
        for key, value in kwargs.items():
            if log.get(key) != value:
                match = False
                break
        if match:
            filtered.append(log)
    return filtered
def count_by_level(logs_list):
    counts = {}
    for log in logs_list:
        level = log.get("level")
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1
    return counts
def count_by_user(logs_list):
    counts = {}
    for log in logs_list:
        user = log.get("user")
        if user:
            if user in counts:
                counts[user] += 1
            else:
                counts[user] = 1
    return counts
def sum_amount_failed_payments(logs_list):
    total = 0
    for log in logs_list:
        if log.get("action") == "payment" and log.get("status") == "fail":
            amount = log.get("amount")
            if isinstance(amount, (int, float)):
                total += amount
    return total
def count_by_action(logs_list):
    counts = {}
    for log in logs_list:
        action = log.get("action")
        if action:
            if action in counts:
                counts[action] += 1
            else:
                counts[action] = 1
    return counts
def count_by_status(logs_list):
    counts = {}
    for log in logs_list:
        status = log.get("status")
        if status:
            if status in counts:
                counts[status] += 1
            else:
                counts[status] = 1
    return counts
parsed_logs = parse_all_logs(logs)
save_to_json(parsed_logs)
print("---- FAIL ONLY ----")
fail_logs = filter_logs(parsed_logs, status="fail")
for log in fail_logs:
    print(log)
print("\n---- ONLY ERRORS ----")
error_logs = filter_logs(parsed_logs, level="ERROR")
for log in error_logs:
    print(log)
print("\n---- ONLY anna ----")
anna_logs = filter_logs(parsed_logs, user="anna")
for log in anna_logs:
    print(log)
print("\n---- COUNT BY LEVEL ----")
level_counts = count_by_level(parsed_logs)
info = level_counts.get("INFO", 0)
error = level_counts.get("ERROR", 0)
warning = level_counts.get("WARNING", 0)
print(info, error, warning)
