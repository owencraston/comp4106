#!/usr/bin/env python3
"""
This class contains a lsit of classes
"""
from course import Course
import time

class Schedule:
    def __init__(self, class1, class2, class3):
        self.class1 = class1
        self.class2 = class2
        self.class3 = class3
        self.class_schedule = [class1, class2, class3]

    def sort(self):
        sorted_classes = sorted(self.class_schedule, key=lambda c: __parse_time__(c["start_time"]))
        self.class_schedule = sorted_classes


def __parse_time__(time_string):
        t = time.strptime(time_string, '%H:%M')
        return t

