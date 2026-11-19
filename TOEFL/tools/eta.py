"""预计完成时间：2021 套共 100 篇 × 3 段 = 300 段。
用法：python3 TOEFL/tools/eta.py [今天日期 YYYY-MM-DD，默认取系统日期]
输出：已完成段数、剩余段数、按每天一段（她的计划）和按实际平均速度的预计完成日。
"""
import json, sys, datetime as dt
TOTAL = 300
d = json.load(open("TOEFL/data/reading-log.json"))
done = [x for x in d if x.get("set") == "2021" and x.get("date")]
n = len({x["passage"] for x in done})
left = TOTAL - n
today = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
plan_end = today + dt.timedelta(days=left)  # 今天之后每天一段
first = min(dt.date.fromisoformat(x["date"]) for x in done)
days = (today - first).days + 1
pace = n / days
act_end = today + dt.timedelta(days=round(left / pace)) if pace else None
print(f"完成 {n}/{TOTAL} 段，剩余 {left} 段")
print(f"按每天一段：{plan_end}")
print(f"按实际平均 {pace:.2f} 段/天（{first} 起 {days} 天）：{act_end}")
