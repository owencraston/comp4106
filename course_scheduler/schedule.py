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
        self.time_table = self.generate_timetable()

    def add_course(self, course):
        self.courses.append(course)
        self.course_count = len(self.courses)
        self.time_table =  self.generate_timetable()
    
    def generate_timetable(self):
        if len(self.courses):
            time_table = {"mon":[], "tue":[], "wed":[], "thu":[], "fri":[]}
            for c in self.courses:
                for day in c.days:
                    time_table[day].append(c)
                    time_table[day] = self.sort(time_table[day])
            return time_table

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
        t = time.strptime(time_string, '%H:%M')
        return t

