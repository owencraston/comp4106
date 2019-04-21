#!/usr/bin/env python3
import json
from course import Course
from schedule import Schedule
from itertools import combinations
from random import randint
from copy import deepcopy


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

def print_combo(combo):
    for course in combo:
        course.print_course()

def test_schedule():
    schedule = Schedule([])
    course_list = populate_classes()
    combos = get_combinations(course_list, 3)
    which_combo = randint(0, len(combos)-1)
    print_combo(combos[which_combo])
    for course in combos[which_combo]:
        schedule.add_course(course)
    return schedule

def build_base_schedule():
    possible_courses = populate_classes()
    required_courses = []
    base_schedule = Schedule([])
    for course in possible_courses:
        if course.required:
            required_courses.append(course)
    # make shedule
    for req_course in required_courses:
        added = base_schedule.add_course(req_course)
        if not added:
            # this is purely based on the order the classes are parsed
            print(f"Unable to add required courses {req_course.subject}. These courses have conflicts")
    return base_schedule


def __free_day_score__(schedule):
    # give alot of points for empty days
    time_table = schedule.time_table
    score = 0
    for day, _ in time_table.items():
        if not len(time_table[day]):
            score += 100
    return score

def get_schedule_score(schedule):
    return __free_day_score__(schedule)

def remove_duplicates(master_list, possible_courses):
    duplicate_courses = []
    for course in possible_courses:
        for set_course in master_list:
            if set_course.equals(course):
                duplicate_courses.append(course)
    for c in duplicate_courses:
        possible_courses.remove(c)
    return possible_courses


def hill_climb_search(possible_courses, course_count):
    # starting state is the base schedule with all requirments
    base_schedule = build_base_schedule()
    remaining_courses = remove_duplicates(base_schedule.courses, possible_classes)
    return remaining_courses

    
        
s = build_base_schedule()
s.print_time_table()
print(f"Base wait time: {s.total_wait_time}")
print(f"Schedule score = {get_schedule_score(s)}")
print("course list")
for c in s.courses:
    c.quick_print()

possible_classes = populate_classes()
new_possible_classes = hill_climb_search(deepcopy(possible_classes), 3)
print("remaining courses")
for c in new_possible_classes:
    c.quick_print()


