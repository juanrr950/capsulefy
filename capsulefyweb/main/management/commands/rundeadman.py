from django.core.management.base import BaseCommand, CommandError
from main.views import check_deadman_switch

from apscheduler.schedulers.blocking import BlockingScheduler
from main.logic import check_modules_release

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def run_deadman():
    check_deadman_switch()
    
    #check_modules_release()

sched.start()