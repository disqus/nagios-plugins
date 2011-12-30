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
       -t TARGET, --target=TARGET
                             Target to check
       --from=TIME_FROM      From timestamp/date
       --until=TIME_UNTIL    Until timestamp/date [now]
       --percentile=PERCENT  Use nPercentile Graphite function on the target
                             (returns one datapoint)
       --over                Over specified threshold [True]
       --under               Under specified threshold [False]
       -W NUM                Warn on >= NUM beyond threshold [0]
       -C NUM                Critical on >= NUM beyond threshold [0]
       --threshold=VALUE     Set threshold to VALUE

Mandatory arguments: -U, [-t|--target], --from, [--percent|--threshold]
