#!/usr/bin/python

# author: Christian Berendt <berendt@b1-systems.de>

import ping, socket, time, sys
from daemon import runner

class Pinger():
    def __init__(self, number, interval, addresses):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/pinger.log'
        self.stderr_path = '/var/log/pinger.log'
        self.pidfile_path =  '/var/run/pinger.pid'
        self.pidfile_timeout = 5

        self._number = number
        self._interval = interval
        self._addresses = addresses

    def run(self):
        try:
            for _ in range(self._number):
                for target in self._addresses:
                    delay = ping.do_one(target, 2, 64)
                    if delay:
                        print "%s: %.8f seconds" % (target, delay)
                    else:
                        print "%s not reachable" % target

                time.sleep(self._interval)
        except socket.error, e:
            pass

# arguments: NUMBER_OF_PINGS INTERVAL_BETWEEN_PINGS ADDRESS_1 ADDRESS_2 ..

#   example: python pinger.py start/stop 10 3 10.10.10.10 10.10.10.20 ..

try:
    pinger = Pinger(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:])
except:
    print "usage: %s start/stop NUMBER_OF_PINGS INTERVAL_BETWEEN_PINGS ADDRESS_1 ADDRESS_2 .." % sys.argv[0]
    sys.exit(1)

daemon_runner = runner.DaemonRunner(pinger)
daemon_runner.do_action()
