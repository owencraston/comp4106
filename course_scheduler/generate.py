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

def __wait_time_score__(schedule):
    return -1 * (schedule.total_wait_time)

def get_schedule_score(schedule):
    free_days = __free_day_score__(schedule)
    # wait_time = __wait_time_score__(Schedule)
    # if there are any free days it is positive, we subtract the wait time from this score
    return free_days

def remove_duplicates(master_list, possible_courses):
    duplicate_courses = []
    for course in possible_courses:
        for set_course in master_list:
            if set_course.equals(course):
                duplicate_courses.append(course)
    for c in duplicate_courses:
        possible_courses.remove(c)
    return possible_courses

def remove_time_collisions(schedule, potential_courses):
    invalid_courses = []
    for course in potential_courses:
        test_schedule = deepcopy(schedule)
        added = test_schedule.add_course(course)
        if not added:
            invalid_courses.append(course)
    
    for course in invalid_courses:
        potential_courses.remove(course)
    return potential_courses


def search(possible_courses, course_count):
    # starting state is the base schedule with all required courses
    base_schedule = build_base_schedule()
    remaining_courses = remove_duplicates(base_schedule.courses, possible_classes)
    current_node = base_schedule
    remaining_courses = remove_time_collisions(current_node, remaining_courses)
    # check if we have a full schedule yet or there are no more options
    while current_node.course_count < course_count and remaining_courses:
        # this will be our next addition to the schedule
        next_node = None
        next_score = -100000000
        # value for storing the max score from an added course
        remaining_courses = remove_time_collisions(current_node, remaining_courses)
        # get the next best addition to the schedule
        for potential_course in remaining_courses:
            temp_schedule = deepcopy(current_node)
            # add the course to the temp schedule
            added = temp_schedule.add_course(potential_course)
            # if the course was valid and added
            if added:
                # get the score of the schedule with the potential course addition
                temp_score = get_schedule_score(temp_schedule)
                # if the new score is better than the previous keep it and that node
                if temp_score > next_score:
                    # keep this score to track it
                    next_score = temp_score
                    # keep this node
                    next_node = deepcopy(potential_course)
        # add the next_node as the next course in the schedule
        current_node.add_course(next_node)
        # remove next_node from the remaining courses
        remaining_courses = list(set(remove_time_collisions(current_node, remaining_courses)))
    # at this point we should have a full schedule adn we'll return it
    return current_node

possible_classes = populate_classes()
schedule = search(deepcopy(possible_classes), 5)

schedule.print_time_table()
print(f"shedule score {get_schedule_score(schedule)}")



