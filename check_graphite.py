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

    def __init__(self, url, targets, _from, _until):
        self.url = url.rstrip('/')
        self.targets = targets
        self._from = _from
        self._until = _until
        params = [('target', t) for t in self.targets] +\
            [('from', self._from)] +\
            [('until', self._until)] +\
            [('format', 'json')]
        self.full_url = self.url + '/render?' +\
            urllib.urlencode(params)

    def check_datapoints(self, datapoints, func, **kwargs):
        """Find alerting datapoints

        Args:
            datapoints (list): The list of datapoints to check
            func (function): The comparator function to call on each datapoint

        Kwargs:
            bounds (list): Compare against `datapoints` to find out of bounds list
            compare (list): Used for comparison if `datapoints` is out of bounds
            threshold (float): `func` is called for each datapoint against `threshold`

        Returns:
            The list of out of bounds datapoints
        """
        if 'threshold' in kwargs:
            return [x for x in datapoints if x and func(x, kwargs['threshold'])]
        elif 'bounds' in kwargs:
            if 'compare' in kwargs:
                return [datapoints[x] for x in xrange(len(datapoints)) if func(datapoints[x], kwargs['bounds'][x]) and func(datapoints[x], kwargs['compare'][x])]
            else:
                return [datapoints[x] for x in xrange(len(datapoints)) if func(datapoints[x], kwargs['bounds'][x])]

    def fetch_metrics(self):
        try:
            response = urllib2.urlopen(self.full_url)

            if response.code != 200:
                return None
            else:
                return json.loads(response.read())
        except urllib2.URLError, TypeError:
            return None

    def generate_output(self, datapoints, *args, **kwargs):
        """Generate check output

        Args:
            datapoints (list): The list of datapoints to check
            warn_oob (list): Optional list of datapoints considered in warning state
            crit_oob (list): Mandatory list of datapoints considered in warning state

        Kwargs:
            count (int): Number of metrics that would generate an alert
            warning (float): The check's warning threshold
            critical (float): The check's critical threshold
            target (str): The target for `datapoints`

        Returns:
            A dictionary of datapoints grouped by their status ('CRITICAL', 'WARNING', 'OK')
        """
        check_output = dict(OK=[], WARNING=[], CRITICAL=[])
        count = kwargs['count']
        warning = kwargs.get('warning', 0)
        critical = kwargs.get('critical', 0)
        target = kwargs.get('target', 'timeseries')

        if len(args) > 1:
            (warn_oob, crit_oob) = args
        else:
            crit_oob = [x for x in args[0] if x]
            warn_oob = []

        if crit_oob and len(crit_oob) >= count:
            check_output['CRITICAL'].append('%s [crit=%f|datapoints=%s]' %\
                (target, critical, ','.join(['%s' % str(x) for x in crit_oob])))
        elif warn_oob and len(warn_oob) >= count:
            check_output['WARNING'].append('%s [warn=%f|datapoints=%s]' %\
                (target, warning, ','.join(['%s' % str(x) for x in warn_oob])))
        else:
            check_output['OK'].append('%s [warn=%0.3f|crit=%f|datapoints=%s]' %\
                (target, warning, critical, ','.join(['%s' % str(x) for x in datapoints])))

        return check_output


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-U', '--graphite-url', dest='graphite_url',
                      default='http://localhost/',
                      metavar='URL',
                      help='Graphite URL [%default]')
    parser.add_option('-t', '--target', dest='target',
                      action='append',
                      help='Target to check')
    parser.add_option('--compare', dest='compare',
                      metavar='SERIES',
                      help='Compare TARGET against SERIES')
    parser.add_option('--from', dest='_from',
                      help='From timestamp/date')
    parser.add_option('--until', dest='_until',
                      default='now',
                      help='Until timestamp/date [%default]')
    parser.add_option('-c', '--count', dest='count',
                      default=0,
                      type='int',
                      help='Alert on at least COUNT metrics [%default]')
    parser.add_option('--percentile', dest='percentile',
                      default=0,
                      type='int',
                      metavar='PERCENT',
                      help='Use nPercentile Graphite function on the target (returns one datapoint)')
    parser.add_option('--empty-ok', dest='empty_ok',
                      default=False,
                      action='store_true',
                      help='Empty data from Graphite is OK')
    parser.add_option('--confidence', dest='confidence_bands',
                      default=False,
                      action='store_true',
                      help='Use holtWintersConfidenceBands Graphite function on the target')
    parser.add_option('--over', dest='over',
                      default=True,
                      action='store_true',
                      help='Over specified WARNING or CRITICAL threshold [%default]')
    parser.add_option('--under', dest='under',
                      default=False,
                      action='store_true',
                      help='Under specified WARNING or CRITICAL threshold [%default]')
    parser.add_option('-W', dest='warning',
                      type='float',
                      metavar='VALUE',
                      help='Warning if datapoints beyond VALUE')
    parser.add_option('-C', dest='critical',
                      type='float',
                      metavar='VALUE',
                      help='Critical if datapoints beyond VALUE')

    (options, args) = parser.parse_args()

    if not all([getattr(options, option) for option in ('_from', 'target')]):
        parser.print_help()
        sys.exit(NAGIOS_STATUSES['UNKNOWN'])

    real_from = options._from

    if options.under:
        options.over = False

    if options.confidence_bands:
        targets = [options.target[0], 'holtWintersConfidenceBands(%s)' % options.target[0]]
        if options.over:
            check_func = lambda x, y: x > y
        else:
            check_func = lambda x, y: x < y
        check_threshold = None
        from_slice = int(options._from) * -1
        real_from = '-2w'

        if options.compare:
            targets.append(options.compare)
    else:
        if not all([getattr(options, option) for option in ('critical', 'warning')]):
            parser.print_help()
            sys.exit(NAGIOS_STATUSES['UNKNOWN'])

        if options.percentile:
            targets = ['nPercentile(%s, %d)' % (options.target[0], options.percentile)]
        else:
            targets = options.target

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
    graphite = Graphite(options.graphite_url, targets, real_from, options._until)
    metric_data = graphite.fetch_metrics()

    if metric_data:
        if options.confidence_bands:
            actual = [x[0] for x in metric_data[0].get('datapoints', [])][from_slice:]
            target_name = metric_data[0]['target']
            kwargs = {}

            if options.over:
                kwargs['bounds'] = [x[0] for x in metric_data[1].get('datapoints', [])][from_slice:]
            elif options.under:
                kwargs['bounds'] = [x[0] for x in metric_data[2].get('datapoints', [])][from_slice:]

            if options.compare:
                kwargs['compare'] = [x[0] for x in metric_data[3].get('datapoints', [])][from_slice:]
                if not any(kwargs['compare']):
                    print 'CRITICAL: No compare target output from Graphite!'
                    sys.exit(NAGIOS_STATUSES['CRITICAL'])

            if all(actual) and all(kwargs['bounds']):
                points_oob = graphite.check_datapoints(actual, check_func, **kwargs)
                check_output[target_name] = graphite.generate_output(actual,
                                                                     points_oob,
                                                                     count=options.count,
                                                                     target=target_name)

            else:
                print 'CRITICAL: No output from Graphite for target(s): %s' % ', '.join(targets)
                sys.exit(NAGIOS_STATUSES['CRITICAL'])
        else:
            for target in metric_data:
                datapoints = [x[0] for x in target.get('datapoints', []) if x]
                if not any(datapoints) and not options.empty_ok:
                    print 'CRITICAL: No output from Graphite for target(s): %s' % ', '.join(targets)
                    sys.exit(NAGIOS_STATUSES['CRITICAL'])

                crit_oob = graphite.check_datapoints(datapoints, check_func, threshold=crit)
                warn_oob = graphite.check_datapoints(datapoints, check_func, threshold=warn)
                check_output[target['target']] = graphite.generate_output(datapoints,
                                                                          warn_oob,
                                                                          crit_oob,
                                                                          count=options.count,
                                                                          target=target['target'],
                                                                          warning=warn,
                                                                          critical=crit)
    else:
        if options.empty_ok and isinstance(metric_data, list):
            print 'OK: No output from Graphite for target(s): %s' % ', '.join(targets)
            sys.exit(NAGIOS_STATUSES['OK'])

        print 'CRITICAL: No output from Graphite for target(s): %s' % ', '.join(targets)
        sys.exit(NAGIOS_STATUSES['CRITICAL'])

    for target, messages in check_output.iteritems():
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
