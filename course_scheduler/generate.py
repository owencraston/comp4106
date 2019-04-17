#!/usr/bin/env python3
import json
from course import Course
from schedule import Schedule
from itertools import combinations

courses = []

with open('sample_classes.json') as sample_classes:
    data = json.load(sample_classes)
    for c in data['courses']:
        course = Course(c['subject'], c['crn'], c['title'], c['description'], c['prerequisites'],\
                    c['credit'], c['instructor'], c['start_date'], c['end_date'], c['days'],\
                    c['time'], c['building'], c['room'])
        courses.append(course)


def get_combinations(class_options, n):
    combos = combinations(class_options, n)
    return combos

def print_combos(cmb):
    for c in cmb:
        for crs in c:
            crs.print_course()
