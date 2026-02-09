#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pack incoming messages within a specified time window as list, much like the Max object 'thresh'.

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@license: GPL
"""

import time

class PyThresh:
    """
    Pack incoming messages within a specified time window as list, much like the Max object 'thresh'.
    """

    def __init__(self, timeThresh):
        """
        Class constructor.

        @param self: The object pointer.
        """
        self.timethen = time.time()
        self.timeThresh = timeThresh
        """Time window size, in seconds."""
        self.poly = 5
        """The maximum length of the threshed list, overflow will be discarded with last event priority."""
        self.threshlist = []

    def thresh(self, value):
        """
        Pack incoming messages within a specified time window as list, much like the Max object 'thresh'.

        @param self: The object pointer.
        @param value: The value to be thresh\'ed.
        @return: The list of events that was received within the time window.
        """
        timenow = time.time()
        timespan = timenow - self.timethen
        if timespan < self.timeThresh:
            self.threshlist.append(value)
        else:
            self.threshlist = [value]
            self.timethen = timenow
        # polyphony limiter, if too many items: discard the oldest items
        while len(self.threshlist) > self.poly:
             self.threshlist.pop(0)
        return self.threshlist

    def setThreshTime(self, value):
        """
        Set the size of the time window.

        @param self: The object pointer.
        @param value: The size of the time window, in seconds.
        """
        self.timeThresh = value

def test():
    t = PyThresh(10)
    inp = ''
    print('collect input messages recevied within a time window into a list')
    print('type quit to stop, other messages are thresh\'ed')
    while inp != 'quit':
        inp = input()
        testlist = t.thresh(inp)
        print(testlist)

if __name__ == '__main__':
    test()
