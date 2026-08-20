import unittest
from CourseRegistration import Course
from CourseRegistration import CourseRegistration
class TestCourseRegistrationQA(unittest.TestCase):
    def setUp(self):
        self.registration=CourseRegistration("S001","B.Tech CSE",3,12)
        self.registration.add_completed_course("Programming")
        self.registration.add_completed_course("Data Structures")
        self.registration.add_completed_course("Statistics")
        self.registration.add_completed_course("Networking")
        self.registration.add_course(Course("DBMS",4,"Programming","MON-09:00",2))
        self.registration.add_course(Course("AI",4,"Data Structures","TUE-10:00",2))
        self.registration.add_course(Course("ML",3,"Statistics","WED-11:00",2))
        self.registration.add_course(Course("Cloud",3,"Networking","THU-12:00",2))
    def test_01_valid_registration(self):
        result=self.registration.register_course("DBMS")
        self.assertEqual(result,"Registration successful")
    def test_02_missing_prerequisite(self):
        registration=CourseRegistration("S002","B.Tech CSE",3,12)
        registration.add_course(Course("AI",4,"Data Structures","TUE-10:00",2))
        result=registration.register_course("AI")
        self.assertEqual(result,"Missing prerequisite")
    def test_03_credit_limit_violation(self):
        registration=CourseRegistration("S003","B.Tech CSE",3,6)
        registration.add_completed_course("Programming")
        registration.add_completed_course("Data Structures")
        registration.add_course(Course("DBMS",4,"Programming","MON-09:00",2))
        registration.add_course(Course("AI",4,"Data Structures","TUE-10:00",2))
        registration.register_course("DBMS")
        result=registration.register_course("AI")
        self.assertEqual(result,"Credit limit exceeded")
    def test_04_timetable_conflict(self):
        self.registration.add_course(Course("OS",3,"Programming","MON-09:00",2))
        self.registration.register_course("DBMS")
        result=self.registration.register_course("OS")
        self.assertEqual(result,"Timetable conflict")
    def test_05_full_course(self):
        course=self.registration.courses["DBMS"]
        course.registered_students.append("S002")
        course.registered_students.append("S003")
        result=self.registration.register_course("DBMS")
        self.assertEqual(result,"Course is full")
    def test_06_duplicate_registration(self):
        self.registration.register_course("DBMS")
        result=self.registration.register_course("DBMS")
        self.assertEqual(result,"Duplicate registration")
    def test_07_invalid_course(self):
        result=self.registration.register_course("INVALID")
        self.assertEqual(result,"Invalid course")
    def test_08_semester_restriction(self):
        registration=CourseRegistration("S004","B.Tech CSE",9,12)
        registration.add_completed_course("Programming")
        registration.add_course(Course("DBMS",4,"Programming","MON-09:00",2))
        result=registration.register_course("DBMS")
        self.assertEqual(result,"Semester restriction")
    def test_09_boundary_credit_values(self):
        registration=CourseRegistration("S005","B.Tech CSE",3,4)
        registration.add_completed_course("Programming")
        registration.add_course(Course("DBMS",4,"Programming","MON-09:00",2))
        result=registration.register_course("DBMS")
        self.assertEqual(result,"Registration successful")
        self.assertEqual(registration.calculate_registered_credits(),4)
class JenkinsPipelineTextResult(unittest.TextTestResult):
    def startTest(self,test):
        super().startTest(test)
        test_name=test._testMethodName.split("_",2)[-1].replace("_"," ").capitalize()
        self.stream.write(f" -> Verifying Step: {test_name:<35} ")
        self.stream.flush()
    def addSuccess(self,test):
        super().addSuccess(test)
        self.stream.writeln("[ PASSED ]")
    def addFailure(self,test,err):
        super().addFailure(test,err)
        self.stream.writeln("[ FAILED ]")
if __name__=="__main__":
    print("="*65)
    print(" EXECUTING COURSE REGISTRATION QA PIPELINE STAGES ")
    print("="*65)
    runner=unittest.TextTestRunner(verbosity=2,resultclass=JenkinsPipelineTextResult)
    suite=unittest.TestLoader().loadTestsFromTestCase(TestCourseRegistrationQA)
    result=runner.run(suite)
    print("="*65)
    if result.wasSuccessful():
        print("PIPELINE STATUS: ALL 9 COURSE REGISTRATION CHECKS PASSED SUCCESSFULLY")
    else:
        print("PIPELINE STATUS: FAILURE DETECTED IN TEST SUITE")
    print("="*65)