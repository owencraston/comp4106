#!/usr/bin/env python3
import json
from course import Course
from schedule import Schedule
from itertools import combinations


def populate_classes():
    courses = []
    with open('sample_classes.json') as sample_classes:
        data = json.load(sample_classes)
        for c in data['courses']:
            course = Course(c['subject'], c['crn'], c['title'], c["required"],c['description'], c['prerequisites'],\
                        c['credit'], c['instructor'], c['start_date'], c['end_date'], c['days'],\
                        c['start_time'], c["end_time"], c['building'], c['room'])
            courses.append(course)
    return courses


def get_combinations(class_options, n):
    combos = combinations(class_options, n)
    return list(combos)

def print_combos(cmb):
    for c in cmb:
        for crs in c:
            crs.print_course()

def test_schedule():
    schedule = Schedule([])
    course_list = populate_classes()
    combos = get_combinations(course_list, 3)
    for course in combos[1]:
        schedule.add_course(course)
    return schedule

schedule = test_schedule()

schedule.print_time_table()



# for c in course_list:
#     c.print_course()

