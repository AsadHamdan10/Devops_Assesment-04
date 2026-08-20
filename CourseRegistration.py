class Course:
    def __init__(self,code,credits,prerequisite,timetable,capacity=2):
        self.code=code
        self.credits=credits
        self.prerequisite=prerequisite
        self.timetable=timetable
        self.capacity=capacity
        self.registered_students=[]
class CourseRegistration:
    def __init__(self,student_id,program,semester,credit_limit=12):
        self.student_id=student_id
        self.program=program
        self.semester=semester
        self.credit_limit=credit_limit
        self.courses={}
        self.completed_courses=[]
        self.registered_courses=[]
    def add_course(self,course):
        self.courses[course.code]=course
    def add_completed_course(self,course_code):
        self.completed_courses.append(course_code)
    def register_course(self,course_code):
        if course_code not in self.courses:
            return "Invalid course"
        course=self.courses[course_code]
        if course_code in self.registered_courses:
            return "Duplicate registration"
        if course.prerequisite and course.prerequisite not in self.completed_courses:
            return "Missing prerequisite"
        current_credits=self.calculate_registered_credits()
        if current_credits+course.credits>self.credit_limit:
            return "Credit limit exceeded"
        for registered_code in self.registered_courses:
            registered_course=self.courses[registered_code]
            if registered_course.timetable==course.timetable:
                return "Timetable conflict"
        if len(course.registered_students)>=course.capacity:
            return "Course is full"
        if self.semester<1 or self.semester>8:
            return "Semester restriction"
        course.registered_students.append(self.student_id)
        self.registered_courses.append(course_code)
        return "Registration successful"
    def calculate_registered_credits(self):
        total=0
        for course_code in self.registered_courses:
            total+=self.courses[course_code].credits
        return total
    def get_registered_courses(self):
        return self.registered_courses
if __name__=="__main__":
    registration=CourseRegistration("S001","B.Tech CSE",3,12)
    registration.add_completed_course("Programming")
    registration.add_course(Course("DBMS",4,"Programming","MON-09:00"))
    registration.add_course(Course("AI",4,"Data Structures","TUE-10:00"))
    registration.add_course(Course("ML",3,"Statistics","WED-11:00"))
    registration.add_course(Course("Cloud",3,"Networking","THU-12:00"))
    print("="*60)
    print(" UNIVERSITY COURSE REGISTRATION SYSTEM ")
    print("="*60)
    print(registration.register_course("DBMS"))
    print("Registered Courses:",registration.get_registered_courses())
    print("Total Registered Credits:",registration.calculate_registered_credits())
    print("="*60)