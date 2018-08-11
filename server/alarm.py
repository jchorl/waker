import schedule

import clear_next_wakeup_song, get_next_wakeup_song from spotify


def alarm_job():
    wakeup_song = get_next_wakeup_song()
    print('waking up to {}'.format(wakeup_song))
    clear_next_wakeup_song()

def alarm_job_once():
    alarm_job()
    return schedule.CancelJob
