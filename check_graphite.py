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
            return [x for x in datapoints if x and func(x, kwargs['threshold'])]

    def fetch_metrics(self):
        try:
            response = urllib2.urlopen(self.full_url)

            if response.code != 200:
                return None
            else:
                return json.loads(response.read())
        except urllib2.URLError:
            return None

    def generate_output(self, datapoints, warn_oob, crit_oob, **kwargs):
        check_output = dict(OK=[], WARNING=[], CRITICAL=[])
        warning = kwargs['warning']
        critical = kwargs['critical']
        target = kwargs.get('target', 'timeseries')

        if crit_oob:
            check_output['CRITICAL'].append('%s [crit=%f|datapoints=%s]' %\
                (target, critical, ','.join(['%s' % str(x) for x in crit_oob])))
        elif warn_oob:
            check_output['WARNING'].append('%s [warn=%f|datapoints=%s]' %\
                (target, warning, ','.join(['%s' % str(x) for x in warn_oob])))
        else:
            check_output['OK'].append('%s [warn=%0.3f|crit=%f|datapoints=%s]' %\
                (target, warning, critical, ','.join(['%s' % str(x) for x in datapoints])))

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
                      help='Over specified WARNING or CRITICAL threshold [%default]')
    parser.add_option('--under', dest='under',
                      default=False,
                      action='store_true',
                      help='Under specified WARNING or CRITICAL threshold [%default]')
    parser.add_option('-W', dest='warning',
                      metavar='VALUE',
                      help='Warning if datapoints over VALUE')
    parser.add_option('-C', dest='critical',
                      metavar='VALUE',
                      help='Critical if datapoints over VALUE')

    (options, args) = parser.parse_args()

    for mandatory in ['time_from', 'targets']:
        if not options.__dict__[mandatory]:
            print 'ERROR: missing option: --%s\n' % mandatory.replace('time_', '').replace('targets', 'target')
            parser.print_help()
            sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    if options.under:
        options.over = False

    if options.percentile:
        targets = ['nPercentile(%s, %d)' % (options.targets[0], options.percentile)]
    else:
        targets = options.targets

    try:
        warn = float(options.warning)
        crit = float(options.critical)
        if options.over:
            check_func = lambda x, y: x > y
        else:
            check_func = lambda x, y: x < y
    except ValueError:
        print 'ERROR: WARNING or CRITICAL threshold is not a number\n'
        parser.print_help()
        sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    check_output = {}
    graphite = Graphite(options.graphite_url, targets, options.time_from, options.time_until)
    metric_data = graphite.fetch_metrics()

    if metric_data:
        for target in metric_data:
            datapoints = [x[0] for x in target.get('datapoints', []) if x]
            crit_oob = graphite.check_datapoints(datapoints, check_func, threshold=crit)
            warn_oob = graphite.check_datapoints(datapoints, check_func, threshold=warn)
            check_output[target['target']] = graphite.generate_output(datapoints,
                                                                      warn_oob,
                                                                      crit_oob,
                                                                      target=target['target'],
                                                                      warning=warn,
                                                                      critical=crit)
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
