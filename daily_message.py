#daily_message.py

import polling

from datetime import time, datetime
import asyncio

daily_task_time = "11:19"

last_run = {}

def should_run(task_name, current_time):
    # Only run once per day
    return last_run.get(task_name) != current_time.date()


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if current_time == daily_task_time and should_run("workout", now):
        workouts = polling.load_workouts()
        msg = polling.choose_msg_to_send(workouts)
        asyncio.run(polling.main(msg))
        last_run["workout"] = now.date()
