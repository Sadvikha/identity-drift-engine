from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

scheduler = BlockingScheduler()

def run_pipeline():
    print("⏰ Running scheduled drift scan...")
    subprocess.run(["python", "orchestrator.py"])
    subprocess.run(["python", "action_engine.py"])

scheduler.add_job(run_pipeline, "interval", minutes=1)

print("Scheduler started. Running every 1 minute...")
scheduler.start()
