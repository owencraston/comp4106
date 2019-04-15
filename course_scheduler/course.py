#!/usr/bin/env python3
# This is a class meant to store all attributes oertaining to a course and any information or methods a course would need
# The below is a 

from string import Template
"""
Registration Term:	Summer 2019 (May-August)
CRN:	21184
Subject:	COMP 1406 A
Long Title:	Introduction to Computer Science II
Title:	Intro to Computer Science II
Course Description:	A second course in programming for BCS students, emphasizing problem solving and computational thinking in an object-oriented language. Topics include abstraction, mutable data structures, methods, inheritance, polymorphism, recursion, program efficiency, testing and debugging.
Precludes additional credit for COMP 1006, SYSC 1101 (no longer offered), SYSC 2004.
Prerequisite(s): one of COMP 1405, COMP 1005, ECOR 1606, SYSC 1005, BIT 1400. Restricted to students registered in the B.C.S. program, combined Honours in Computer Science and Mathematics, Honours Computer Mathematics, and Honours Computer Statistics. Students in the industrial applications internship option register in COMP 1406 Z*.
Course Credit Value:	.5
Schedule Type:	Lecture
Full Session Info:	
Status:	Open
Section Information:	Precludes additional credit for COMP 1006, SYSC 1101 (no
longer offered), SYSC 2004.
Year in Program:	{None}\n
Level Restriction:	{None}\n
Degree Restriction:	Bachelor of Computer Science (Include)
Bachelor of Comp Sci General (Include)
Bac of Computer Science Major (Include)
Major Restriction:	{None}\n
Program Restrictions:	{None}\n
Department Restriction:	{None}\n
Faculty Restriction:	{None}\n

Meeting Date	Days	Time	Building	Room	Schedule	Instructor
Jul 02, 2019 to Aug 14, 2019	Tue Thu	18:05 - 20:55	Azrieli Theatre	101	Lecture	Jason Hinek (Primary)
"""
class Course:
    def __init__(self, subject, crn, title, description, prerequisites, credit, instructor, start_date, end_date, days, time, building, room):
        self.subject = subject
        self.crn = crn
        self.title = title
        self.description = description
        self.prerequisites = prerequisites
        self.credit = credit
        self.instructor = instructor
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.time = time
        self.building = building
        self.room = room

    def to_string(self):
        str = (
                f"subject: {self.subject}\n"
                f"crn: {self.crn}\n"
                f"title: {self.title}\n"
                f"description: {self.description}\n"
                f"prerequisites: {self.prerequisites}\n"
                f"credit: {self.credit}\n"
                f"instructor: {self.instructor}\n"
                f"start_date: {self.start_date}\n"
                f"end_date: {self.end_date}\n"
                f"days: {self.days}\n"
                f"time: {self.time}\n"
                f"building: {self.building}\n"
                f"room: {self.room}\n"
            )
                
        return str

    def print_course(self):
        str = self.to_string()
        print(str)
