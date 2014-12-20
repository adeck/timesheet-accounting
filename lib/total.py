#!/usr/bin/env python2.7
#
# A simple script to calculate the number of hours logged
#   in a timesheet formatted as a JSON map of strings to
#   lists of floats, or strings to lists of lists of floats.
# Each list of floats is a 2-tuple; (start time, end time).
# No explicit error handling; if you mess up, stack trace.
# Additionally, if you accidentally put the times in backwards,
#   this won't check for that. So, it'll just _subtract_ that
#   time. Good rule of thumb? Make no mistakes.
#

from json import loads, dumps
from sys import argv

def money(num):
  return float(int(100 * num + 0.5)) / 100
def total(data):
  timesheet = data["timesheet"]
  hours = 0
  for date in timesheet:
    times = timesheet[date]
    try:
      hours += float(times[1]) - float(times[0])
    except TypeError:
      for time in times:
        hours += float(time[1]) - float(time[0])
  return hours;
data = loads(open(argv[1]).read())
pay_rate = data["hourly pay"]
tax = data["income tax"]
hours = total(data)
pay = money(pay_rate * hours)
taxed = money(pay * (1 - tax))
print "You've worked " + str(hours) + " hours."
if (len(argv) > 2):
  print "Before taxes, you'll be paid $" + str(pay) + "."
  print "After "+str(tax)+" tax, you'll be paid $" + str(taxed) + "."

