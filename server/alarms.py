from itertools import groupby
import schedule
from uuid import uuid4

from alarm import alarm_job, alarm_job_once


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

# tag to apply to all alarm jobs
ALARM_TAG = 'alarm'

def get_alarms():
    # group jobs by tag
    jobs = [job for job in schedule.jobs if ALARM_TAG in job.tags]
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

            # if there is already a next_run, take the min, otherwise just use the next_run of the current alarm_job
            alarm['next_run'] = min(alarm['next_run'], alarm_job.next_run) if 'next_run' in alarm else alarm_job.next_run
        alarms.append(alarm)
    return alarms

def new_alarm(alarm_info):
    alarm_id = str(uuid4())
    alarm_time = '{hour:02d}:{minute:02d}'.format(**alarm_info['time'])
    if alarm_info['repeat']:
        for day in alarm_info['days']:
            job = schedule.every().week
            job.start_day = day
            job.at(alarm_time).tag(ALARM_TAG, alarm_id).do(alarm_job)
            alarm_info['next_run'] = min(alarm_info['next_run'], job.next_run) if 'next_run' in alarm_info else job.next_run
    else:
        job = schedule.every().day.at(alarm_time).tag(ALARM_TAG, alarm_id).do(alarm_job_once)
        alarm_info['next_run'] = job.next_run
    alarm_info['id'] = alarm_id
    return alarm_info

def delete_alarm(alarm_id):
    schedule.clear(alarm_id)
    return alarm_id
