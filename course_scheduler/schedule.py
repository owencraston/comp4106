#!/usr/bin/env python3
"""
This class contains a lsit of courses
"""
from course import Course
from datetime import datetime
from copy import deepcopy

class Schedule:
    def __init__(self, courses):
        self.courses = courses
        self.course_count = len(courses)
        self.time_table = self.generate_timetable(self.courses)
        self.total_wait_time = self.get_wait_time()

    def add_course(self, course):
        if self.is_in_schedule(course):
            return False
        temp_timetable = self.update_timetable(deepcopy(self.time_table), course)
        if self.valid_timetable(temp_timetable):
            self.courses.append(course)
            self.course_count = len(self.courses)
            self.time_table = temp_timetable
            self.total_wait_time = self.get_wait_time()
            # return true since class was successfully addedd
            return True
        else:
            # print(f"Failed to add {course.subject} at {course.start_time}")
            # return false since class was not added
            return False
            
    def update_timetable(self, time_table, course):
        for day in course.days:
            time_table[day].append(course)
            time_table[day] = self.sort(time_table[day])
        return time_table

    def generate_timetable(self, courses):
        if len(courses):
            time_table = {"mon":[], "tue":[], "wed":[], "thu":[], "fri":[]}
            for c in courses:
                for day in c.days:
                    time_table[day].append(c)
                    time_table[day] = self.sort(time_table[day])
            if self.valid_timetable(time_table):
                return time_table
        else:
            return {"mon":[], "tue":[], "wed":[], "thu":[], "fri":[]}
    
    def valid_timetable(self, timetable):
        # assume the courses list is sorted
        for _, courses in timetable.items():
            if len(courses):
                prev_course = courses[0]
                for course in courses[1:]:
                    if __parse_time__(course.start_time) < __parse_time__(prev_course.end_time):
                        # print(f"error in timetable. collision with {prev_course.subject} ends at {prev_course.end_time} and {course.subject} starts at {course.start_time}\n")
                        return False
                    prev_course = course
        return True
    
    def is_in_schedule(self, course):
        for c in self.courses:
            if c.equals(course):
                return True
        return False

    def get_wait_time(self):
        total_time = 0
        for _, courses in self.time_table.items():
            if len(courses) >= 2:
                prev_course = courses[0]
                for course in courses[1:]:
                    total_time += self.get_wait_time_between_classes(prev_course, course)
        return total_time

    def get_wait_time_between_classes(self, course1, course2):
        # course 2 - course 1
        time_delta = __parse_time__(course2.start_time) - __parse_time__(course1.end_time)
        return int(time_delta.total_seconds()/60)



    def sort(self, courses):
        sorted_courses = sorted(courses, key=lambda c: __parse_time__(c.start_time))
        return sorted_courses
    
    def print_time_table(self):
        for day, courses in self.time_table.items():
            course_info = []
            if len(courses):
                for course in courses:
                    course_info.append(f"subject: {course.subject}, time: {course.start_time} - {course.end_time}")
            print(day, course_info)
        print("number of courses: ", self.course_count)

    
    def print_courses(self):
        for course in self.courses:
            course.print_course()


def __parse_time__(time_string):
        t = datetime.strptime(time_string, '%H:%M')
        return t

