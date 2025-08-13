from apscheduler.schedulers.background import BackgroundScheduler
import time

app = FastAPI()
scheduler = BackgroundScheduler()

def job():
    print(f"📅 Job chạy lúc {time.strftime('%X')}")

scheduler.add_job(job, "interval", seconds=10)  # Chạy mỗi 10s
scheduler.start()
