from datetime import datetime
import sys


class TimeServer:
    def linux_set_time(self, time_tuple):
        import subprocess
        import shlex

        time_string = datetime(*time_tuple).isoformat()

        subprocess.call(shlex.split("timedatectl set-ntp false")) # For Centos7/RHEL
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
        subprocess.call(shlex.split("sudo hwclock -w"))

    def set_time(self, timestamp: int):
        time_obj = datetime.fromtimestamp(timestamp)

        time_tuple1 = (time_obj.year, #year
                      time_obj.month,   # Month
                      time_obj.day,   # Day
                      time_obj.hour,   # Hour
                      time_obj.minute,   # Minute
                      time_obj.second,   # Second
                      time_obj.microsecond / 1000, )  # Millisecond
        if sys.platform == 'linux':
            self.linux_set_time(time_tuple1)
