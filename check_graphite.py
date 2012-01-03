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

    def __init__(self, url, targets, time_from, time_until):
        self.url = url.rstrip('/')
        self.targets = targets
        self.time_from = time_from
        self.time_until = time_until
        params = [('target', t) for t in self.targets] +\
          [('from', self.time_from)] +\
          [('until', self.time_until)] +\
          [('format', 'json')]
        self.full_url = self.url + '/render?' +\
            urllib.urlencode(params)

    def check_datapoints(self, datapoints, func, **kwargs):
        if kwargs.get('threshold'):
            return [x for x in datapoints if func(x, kwargs['threshold'])]

    def fetch_metrics(self):
        try:
            response = urllib2.urlopen(self.full_url)

            if response.code != 200:
                return None
            else:
                return json.loads(response.read())
        except urllib2.URLError:
            return None

    def generate_output(self, oob, all_points, **kwargs):
        check_output = dict(OK=[], WARNING=[], CRITICAL=[])
        warning = kwargs['warning']
        critical = kwargs['critical']
        threshold = kwargs.get('threshold', None)
        target = kwargs.get('target', 'timeseries')

        if len(oob) > critical:
            check_output['CRITICAL'].append('%s out of bounds [threshold=%s|maxcrit=%d|datapoints=%s]' %\
                (target, str(threshold), critical, ','.join(['%s' % str(x) for x in oob])))
        elif len(oob) > warning:
            check_output['WARNING'].append('%s out of bounds [threshold=%s|maxwarn=%d|datapoints=%s]' %\
                (target, str(threshold), warning, ','.join(['%s' % str(x) for x in oob])))
        else:
            check_output['OK'].append('%s OK [threshold=%s|maxwarn=%d|maxcrit=%d|datapoints=%s]' %\
                (target, str(threshold), warning, critical, ','.join(['%s' % str(x) for x in all_points])))

        return check_output


def do_checks():
    parser = optparse.OptionParser()
    parser.add_option('-U', '--graphite-url', dest='graphite_url',
                      default='http://localhost/',
                      metavar='URL',
                      help='Graphite URL [%default]')
    parser.add_option('-t', '--target', dest='targets',
                      action='append',
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

    for mandatory in ['time_from', 'targets', 'threshold']:
        if not options.__dict__[mandatory]:
            print 'ERROR: missing option: --%s\n' % mandatory.replace('time_', '').replace('targets', 'target')
            parser.print_help()
            sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    if options.over and options.under:
        print 'ERROR: --over and --under are mutually exclusive\n'
        parser.print_help()
        sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    if options.percentile:
        targets = ['nPercentile(%s, %d)' % (options.targets[0], options.percentile)]
    else:
        targets = options.targets

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
        sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    check_output = {}
    graphite = Graphite(options.graphite_url, targets, options.time_from, options.time_until)
    metric_data = graphite.fetch_metrics()

    if metric_data:
        for target in metric_data:
            datapoints = [x[0] for x in target.get('datapoints', []) if x]
            oob = graphite.check_datapoints(datapoints, check_func, threshold=check_threshold)
            check_output[target['target']] = graphite.generate_output(oob, datapoints,
                                                                      target=target['target'],
                                                                      threshold=check_threshold,
                                                                      critical=options.critical,
                                                                      warning=options.warning)

        return check_output
    else:
        print 'CRITICAL: No output from Graphite!'
        sys.exit(NAGIOS_STATUSES['CRITICAL'])

if __name__ == '__main__':
    output = do_checks()

    for target, messages in output.iteritems():
        if messages['CRITICAL']:
            exit_code = NAGIOS_STATUSES['CRITICAL']
        elif messages['WARNING']:
            exit_code = NAGIOS_STATUSES['WARNING']
        else:
            exit_code = NAGIOS_STATUSES['OK']

        for status_code in ['CRITICAL', 'WARNING', 'OK']:
            if messages[status_code]:
                print '\n'.join(['%s: %s' % (status_code, status) for status in messages[status_code]])

    sys.exit(exit_code)
