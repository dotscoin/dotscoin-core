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

    def sync_time(self):
        time_tuple1 = (2012,   # Year
                      9,   # Month
                      6,   # Day
                      0,   # Hour
                      38,   # Minute
                      0,   # Second
                      0, )  # Millisecond
        if sys.platform == 'linux':
            self.linux_set_time(time_tuple1)
