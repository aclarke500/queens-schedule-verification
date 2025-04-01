# {'course_code': 'STAT 362', 'day': 'Friday', 'time_start': '11:30AM', 'time_end': '12:30PM', 'location': 'Biosciences Complex 1102'}
# is it on west?

# is it back to back west and non west?

# required courses are CISC 102, CISC 121, CISC 124, CISC 101
# MATH courses are MATH 110 or MATH 112 or MATH 111 for lin alg
# CALC are MATH 120, 121, or 123+124


# fitting CS requirements
def get_unique_course_codes(courses:dict)->list[str]:
    return list(set([course['course_code'] for course in courses]))


def is_taking_cisc_101(unique_courses):
    return "CISC 101" in unique_courses

def programming_courses(unique_courses):
    takes_101 = is_taking_cisc_101(unique_courses)
    takes_121 = "CISC 121" in unique_courses
    takes_124 = "CISC 124" in unique_courses
    if (takes_101 and takes_121) or (takes_121 and takes_124):
        return True
    
def is_taking_cisc_102(unique_courses):
    return "CISC 102" in unique_courses

def is_taking_calc(unique_courses):
    takes_120 = "MATH 120" in unique_courses
    takes_121 = "MATH 121" in unique_courses
    takes_123 = "MATH 123" in unique_courses
    takes_124 = "MATH 124" in unique_courses
    if (takes_120 or takes_121 or (takes_123 and takes_124)):
        return True
    
def is_taking_lin_alg(unique_courses):
    takes_110 = "MATH 110" in unique_courses
    takes_111 = "MATH 111" in unique_courses
    takes_112 = "MATH 112" in unique_courses
    if takes_110 or takes_111 or takes_112:
        return True
    
def check_cs_courses(courses):
    unique_courses = get_unique_course_codes(courses)
    issues = [] # these are the schedule issues
    if not is_taking_cisc_102(unique_courses):
        issues.append('You are not taking CISC 102 (Discrete Math)')
    if not programming_courses(unique_courses):
        issues.append('You are not taking the correct programming classes. If you are new to programming you should take CISC 101 first semester and CISC 121 second semester. If you have some programming experience you should take CISC 121 first semester and CISC 124 second semester.')
    if not is_taking_calc(unique_courses):
        issues.append('You are not taking calculus. You should have either MATH 121, 120 or 123 and 124')
    if not is_taking_lin_alg(unique_courses):
        issues.append('You are not taking linear algebra. You should have either MATH 110, 111 or 112')
    
    return issues
    
    