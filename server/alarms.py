from itertools import groupby
import schedule
from uuid import uuid4


"""
an alarm is comprised of multiple jobs, one for each day it should run
the alarm is uniquely identified by a uuid, which all the jobs are tagged by
alarms are specified by a dict:
    {
        id: some_uuid,
        time: {
            hour: 10,
            minute: 0
        },
        repeat: true,
        days: ['monday', 'tuesday'] // days only need to be provided if repeat is true
                                    // otherwise the alarm will just run at that time once
    }
"""

def alarm_job():
    print("I'm working...")

def alarm_job_once():
    print("I'm working once...")
    return schedule.CancelJob

def get_alarms():
    # group jobs by tag
    jobs = schedule.jobs
    sorted_jobs = sorted(jobs, key=lambda job: next(iter(job.tags)))

    alarms = []
    for alarm_uuid, alarm_jobs in groupby(sorted_jobs, lambda job: next(iter(job.tags))):
        alarm = {
                'id': alarm_uuid,
                'days': []
                }
        for alarm_job in alarm_jobs:
            alarm['days'].append(alarm_job.start_day)
            alarm['time'] = {
                    'hour': alarm_job.at_time.hour,
                    'minute': alarm_job.at_time.minute,
                    } # overwrite the time each time, they should all be the same anyway
        alarms.append(alarm)
    return alarms

def new_alarm(alarm_info):
    alarm_id = uuid4()
    alarm_time = '{hour:02d}:{minute:02d}'.format(**alarm_info['time'])
    if alarm['repeat']:
        for day in alarm_info['days']:
            job = schedule.every().week
            job.start_day = day
            job.at(alarm_time).tag(alarm_id).do(alarm_job)
    else:
        schedule.every().day.at(alarm_time).do(alarm_job_once)
    return alarm_info
