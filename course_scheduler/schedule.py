#!/usr/bin/env python3
"""
This class contains a lsit of courses
"""
from course import Course
import time

class Schedule:
    def __init__(self, courses):
        self.courses = courses
        self.course_count = len(courses)
        self.time_table = __get_timetable__(self.courses)

    def add_course(self, course):
        self.courses.append(course)
        self.course_count = len(self.courses)
        self.time_table =  __get_timetable__(self.courses)

    def sort(self):
        sorted_courses = sorted(self.courses, key=lambda c: __parse_time__(c["start_time"]))
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



def __get_timetable__(course_list):
    if len(course_list):
        time_table = {"mon":[], "tue":[], "wed":[], "thu":[], "fri":[]}
        for c in course_list:
            for day in c.days:
                time_table[day].append(c)
        return time_table

def __parse_time__(time_string):
        t = time.strptime(time_string, '%H:%M')
        return t

