# Disqus Nagios plugins

This is a collection of Nagios plugins written at Disqus.

## Scripts

* check_graphite.py

## check_graphite.py

     % ./check_graphite.py -h
     Usage: check_graphite.py [options]

     Options:
       -h, --help            show this help message and exit
       -U URL, --graphite-url=URL
                             Graphite URL [http://localhost/]
       -t TARGETS, --target=TARGETS
                             Target to check
       --from=TIME_FROM      From timestamp/date
       --until=TIME_UNTIL    Until timestamp/date [now]
       --percentile=PERCENT  Use nPercentile Graphite function on the target
                             (returns one datapoint)
       --confidence          Use holtWintersConfidenceBands Graphite function on
                             the target
       --over                Over specified WARNING or CRITICAL threshold [True]
       --under               Under specified WARNING or CRITICAL threshold [False]
       -W VALUE              Warning if datapoints beyond VALUE
       -C VALUE              Critical if datapoints beyond VALUE

Mandatory arguments: -U, [-t|--target], --from
