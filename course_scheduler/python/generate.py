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
            course = Course(c['subject'], c['title'], c["required"],\
                c['instructor'], c['start_date'], c['end_date'], c['days'],\
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

def build_base_schedule(possible_courses):
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
            score += 200
    return score

def get_schedule_score(schedule):
    free_days = __free_day_score__(schedule)
    # if there are any free days it is positive, we subtract the wait time from this score
    return free_days - schedule.total_wait_time

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

def __guess_classes_per_day__(course_count, days_off):
    day_with_courses = 5-days_off
    total_number_of_classes_to_attend_a_week = course_count * 2
    classes_per_day = [0]*day_with_courses
    total_class_list  = [1]*total_number_of_classes_to_attend_a_week

    day = 0
    for i in total_class_list:
        classes_per_day[day] += i
        if day == len(classes_per_day)-1:
            day = 0
        day += 1
    return classes_per_day
    

def guess_total_wait_time(course_count, days_off, average_wait_time):
    classes_per_day = __guess_classes_per_day__(course_count, days_off)
    estimated_total_wait_time = 0
    for classes in classes_per_day:
        estimated_total_wait_time += ((classes - 1) * average_wait_time)
    return estimated_total_wait_time


def search(possible_courses, course_count):
    # starting state is the base schedule with all required courses
    base_schedule = build_base_schedule(possible_courses)
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


def hill_climb_search(possible_courses, course_count, target_free_days, target_wait_time):
    # starting state is the base schedule with all required courses
    base_schedule = build_base_schedule(deepcopy(possible_courses))
    remaining_courses = remove_duplicates(base_schedule.courses, possible_courses)
    current_node = base_schedule
    remaining_courses = remove_time_collisions(current_node, remaining_courses)
    goal_score = (target_free_days * 200) - (guess_total_wait_time(course_count, target_free_days, target_wait_time))
    print(f"goal score {goal_score}")

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

        # we need to return if we have reached our goal, a schedule that has the desired amount of classes and meets the users goals
        if current_node.course_count == course_count and get_schedule_score(current_node) >= goal_score:
            print("found a schedule that meets your goals")
            return current_node
        
    # at this point we should have a full schedule adn we'll return it
    return current_node
    

# possible_classes = populate_classes()
# # possible_classes, 4 class schedule, ideally 1 free break, target 30 minutes of wait time
# schedule = hill_climb_search(deepcopy(possible_classes), 4, 1, 30)

# schedule.print_time_table()
# print(f"shedule score {get_schedule_score(schedule)}")
# print(f"wait_time {schedule.total_wait_time}")



