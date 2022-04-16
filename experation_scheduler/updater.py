from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from experation_scheduler import vote_api




def start():
    # return
    scheduler = BackgroundScheduler()

    # scheduler.add_job(vote_api.update_experation_model, 'interval', minutes=1) #minutes
    scheduler.add_job(vote_api.update_experation_model, 'cron', day_of_week="mon"  ) #week
    
    scheduler.start()