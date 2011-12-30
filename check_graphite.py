#!/usr/bin/env python
"""
check_graphite.py
~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import json
import optparse
import urllib
import urllib2
import sys

NAGIOS_STATUSES = {
    'OK': 0,
    'WARNING': 1,
    'CRITICAL': 2,
    'UNKNOWN': 3
}

class Graphite(object):

    def __init__(self, url, target, time_from, time_until):
        self.url = url.rstrip('/')
        self.target = target
        self.time_from = time_from
        self.time_until = time_until
        self.full_url = self.url + '/render?' +\
            urllib.urlencode({
                'target': self.target,
                'from': self.time_from,
                'until': self.time_until,
                'format': 'json'
            })

    def check_datapoints(self, datapoints, threshold, func):
       def within_bounds(val):
           return func(val, threshold)
       return filter(within_bounds, datapoints)

    def fetch_metrics(self):
        try:
            response = urllib2.urlopen(self.full_url)

            if response.code != 200:
                return None
            else:
                return json.loads(response.read())
        except urllib2.URLError:
            return None

def main():
    parser = optparse.OptionParser()
    parser.add_option('-U', '--graphite-url', dest='graphite_url',
                      default='http://localhost/',
                      metavar='URL',
                      help='Graphite URL [%default]')
    parser.add_option('-t', '--target', dest='target',
                      help='Target to check')
    parser.add_option('--from', dest='time_from',
                      help='From timestamp/date')
    parser.add_option('--until', dest='time_until',
                      default='now',
                      help='Until timestamp/date [%default]')
    parser.add_option('--percentile', dest='percentile',
                      default=0,
                      type='int',
                      metavar='PERCENT',
                      help='Use nPercentile Graphite function on the target (returns one datapoint)')
    parser.add_option('--over', dest='over',
                      default=True,
                      action='store_true',
                      help='Over specified threshold [%default]')
    parser.add_option('--under', dest='under',
                      default=False,
                      action='store_true',
                      help='Under specified threshold [%default]')
    parser.add_option('-W', dest='warning',
                      default=0,
                      type='int',
                      metavar='NUM',
                      help='Warn on >= NUM beyond threshold [%default]')
    parser.add_option('-C', dest='critical',
                      default=0,
                      type='int',
                      metavar='NUM',
                      help='Critical on >= NUM beyond threshold [%default]')
    parser.add_option('--threshold', dest='threshold',
                      metavar='VALUE',
                      help='Set threshold to VALUE')

    (options, args) = parser.parse_args()

    for mandatory in ['time_from', 'target', 'threshold']:
        if not options.__dict__[mandatory]:
            print 'ERROR: missing option: --%s\n' % mandatory.replace('time_', '')
            parser.print_help()
            return NAGIOS_STATUSES['UNKNOWN']

    if options.over and options.under:
        print 'ERROR: --over and --under are mutually exclusive\n'
        parser.print_help()
        return NAGIOS_STATUSES['UNKNOWN']

    if options.percentile:
        target = 'nPercentile(%s, %d)' % (options.target, options.percentile)
    else:
        target = options.target

    try:
        if options.threshold.endswith('%'):
            check_threshold = float(options.threshold.rstrip('%'))
            if options.over:
                check_func = lambda x, y: (x > y) / 100.0
            else:
                check_func = lambda x, y: (x < y) / 100.0
        else:
            check_threshold = float(options.threshold)
            if options.over:
                check_func = lambda x, y: x > y
            else:
                check_func = lambda x, y: x < y
    except:
        print 'ERROR: threshold is not a number\n'
        parser.print_help()
        return NAGIOS_STATUSES['UNKNOWN']

    graphite = Graphite(options.graphite_url, target, options.time_from, options.time_until)
    metric_data = graphite.fetch_metrics()

    if metric_data:
        for target in metric_data:
            datapoints = [x[0] for x in target.get('datapoints', [])]
            points_oob = graphite.check_datapoints(datapoints, check_threshold, check_func)

            if len(points_oob) > options.critical:
                print 'CRITICAL: timeseries out of bounds [threshold=%0.3f|maxcrit=%d|datapoints=%s]' %\
                    (check_threshold, options.critical, ','.join(['%s' % str(x) for x in points_oob]))
                status = 'CRITICAL'
            elif len(points_oob) > options.warning:
                print 'WARNING: timeseries out of bounds [threshold=%0.3f|maxwarn=%d|datapoints=%s]' %\
                    (check_threshold, options.warning, ','.join(['%s' % str(x) for x in points_oob]))
                status = 'WARNING'
            else:
                print 'OK: timeseries OK [threshold=%0.3f|maxwarn=%d|maxcrit=%d|datapoints=%s]' %\
                    (check_threshold, options.warning, options.critical, ','.join(['%s' % str(x) for x in datapoints]))
                status = 'OK'
    else:
        print 'CRITICAL: No output from Graphite!'
        status = 'CRITICAL'

    return NAGIOS_STATUSES[status]

if __name__ == '__main__':
  sys.exit(main())
