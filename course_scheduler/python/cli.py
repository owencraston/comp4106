#!/usr/bin/env python3

from course import Course
import generate as gen
from copy import deepcopy


def get_course_info():
    subject = input("What is the course code?: ")
    if not subject:
        print("Please enter a valid subject.")
        return None
    title = input("What is course title?: ")
    if not title:
        print("Please enter a valid title.")
        return None
    required = input("Is this course required? Type 1 for yes and 0 for no: ")
    if int(required) != 0 and int(required) != 1:
        print("Please enter a value that is 0 or 1 for required.")
        return None
    required = int(required)
    instructor = input("Who is the instructor?: ")
    if not instructor:
        print("Please enter a valid instructir name.")
        return None
    start_date = input("What is the start date? Write in the same form as Jan 07, 2019: ")
    if not start_date:
        print("Please enter a valid start date.")
        return None
    end_date = input("What is the end date? Write in the same form as Apr 09, 2019: ")
    if not end_date:
        print("Please enter a valid end date.")
        return None
    days = input("What days of the week are the classes? Please write in in the abbreviated and separated by commas. Ex: Mon, Wed: ")
    if not end_date:
        print("Please enter a valid days.")
        return None
    start_time = input("What time do these classes start? Use a 24hr clock. Ex: 18:05: ")
    if not start_time:
        print("Please enter a valid start date.")
        return None
    end_time = input("What time do these classes end? Use a 24hr clock. Ex: 18:05: ")
    if not start_time:
        print("Please enter a valid end date.")
        return None
    building = input("What building is the course in?: ")
    if not building:
        print("Please enter a valid room")
        return None
    room = input("What room is the course in?: ")
    if not int(room):
        print("Please enter a valid room")
        return None
    room = int(room)

    if required == 1:
         required = True
    elif required == 0:
        required = False

    course = Course(subject, title, required, instructor, start_date, end_date, days, start_time, end_time, building, room)
    return course
    
def get_user_schedule(possible_courses, course_count, free_days, wait_time):
    schedule = gen.hill_climb_search(deepcopy(possible_courses), course_count, free_days, wait_time)
    schedule.print_time_table()
    print(f"shedule score: {gen.get_schedule_score(schedule)}")
    print(f"wait time: {schedule.total_wait_time}")

running = 1
while running == 1:
    print("Welcome to the course selector")

    # get course count 
    course_count = input("How many courses would you like to take this semester?: ")
    try: 
        int(course_count)
    except ValueError:
        print("Please type an integer value geater than 1")
        course_count = input("How many courses would you like to take this semester?: ")
    course_count = int(course_count)

    wait_time = input("On average, how many minutes would you mind waiting between classes? Please enter a number greater than 10: ")
    try: 
        int(wait_time)
    except ValueError:
        print("Please type an integer representing minutes")
        wait_time = input("On average, how many minutes do at would you mind waiting between classes? Please enter a number greater than 10: ")
    if int(wait_time) < 10 and int(wait_time) > 500:
        print("Please type an integer value geater than 10 and less than 500")
        wait_time = input("On average, how many minutes do at would you mind waiting between classes? Please enter a number greater than 10: ")
    wait_time = int(wait_time)

    free_days = input("How many free days a week would you like to have? Usually don't pick more than 2 since it is very unrealistic: ")
    try: 
        int(free_days)
    except ValueError:
        print("Please type an integer value geater than between less than 4")
        free_days = input("How many free days a week would you like to have? Usually don't pick more than 2 since it is very unrealistic: ")
    if int(free_days) > 5 and int(free_days) < 1:
        print("Please type an integer value geater than between less than 4")
        free_days = input("How many free days a week would you like to have? Usually don't pick more than 2 since it is very unrealistic: ")
    free_days = int(free_days)


    choice = input("Would you like to use the json file to populate your classes? Type 1 for yes and 0 for no: ")
    choice = int(choice)
    if choice == 0:        
        # get course count to choose from
        possible_course_count = input("How many courses would you like to input and choose from?: ")
        try: 
            int(possible_course_count)
        except ValueError:
            print("Please type an integer value geater than 1")
            possible_course_count = input("How many courses would you like to input and choose from?: ")
        possible_course_count = int(possible_course_count)
        possible_courses = []

        if (course_count >= 1) and (possible_course_count > course_count):
            for i in range(possible_course_count):
                print("please fill out the follwoing course information \n")
                course = get_course_info()
                while not course:
                    print("the course did not work please try again")
                    course = get_course_info()
                possible_courses.append(course)
                print(f"successfully added \n{course.to_string()}")
            # we are done and can get the schedule
            get_user_schedule(possible_courses, course_count, free_days, wait_time)
    elif choice == 1:
        possible_courses = gen.populate_classes()
        get_user_schedule(possible_courses, course_count, free_days, wait_time)

    
    cont = input("Do you want to continue? Type 1 for yes and 0 for no: ")
    if int(cont) != 0 and int(cont) != 1:
        print("Please enter a value that is 0 or 1")
        cont = input("Do you want to continue? Type 1 for yes and 0 for no: ")
    running = int(cont)

            
            
