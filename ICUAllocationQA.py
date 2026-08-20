import unittest
from ICUAllocation import Patient
from ICUAllocation import ICUAllocationSystem
class TestICUAllocationQA(unittest.TestCase):
    def test_01_critical_patient(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P001",
            70,
            80,
            140,
            70,
            40.0,
            True
        )
        result = system.add_patient(patient)
        self.assertEqual(
            result,
            "Patient added successfully"
        )
        priority, score = system.get_patient_priority("P001")
        self.assertEqual(
            priority,
            "CRITICAL"
        )
    def test_02_normal_patient(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P002",
            30,
            98,
            75,
            120,
            37.0,
            False
        )
        result = system.add_patient(patient)
        self.assertEqual(
            result,
            "Patient added successfully"
        )
        priority, score = system.get_patient_priority("P002")
        self.assertEqual(
            priority,
            "LOW"
        )
    def test_03_emergency_case(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P003",
            45,
            95,
            90,
            110,
            37.0,
            False,
            emergency=True
        )
        system.add_patient(patient)
        result = system.emergency_allocation("P003")
        self.assertEqual(
            result,
            "Emergency ICU bed allocated"
        )
        self.assertIn(
            "P003",
            system.allocated_beds
        )
    def test_04_no_icu_beds(self):
        system = ICUAllocationSystem(0)
        patient = Patient(
            "P004",
            60,
            88,
            120,
            85,
            38.0,
            True
        )
        system.add_patient(patient)
        result = system.allocate_bed("P004")
        self.assertEqual(
            result,
            "No ICU bed available: Patient placed on waiting list"
        )
        self.assertIn(
            "P004",
            system.get_waiting_list()
        )
    def test_05_duplicate_patient(self):
        system = ICUAllocationSystem(1)
        patient1 = Patient(
            "P005",
            50,
            95,
            80,
            120,
            37.0,
            False
        )
        patient2 = Patient(
            "P005",
            60,
            90,
            100,
            110,
            37.5,
            True
        )
        result1 = system.add_patient(patient1)
        result2 = system.add_patient(patient2)
        self.assertEqual(
            result1,
            "Patient added successfully"
        )
        self.assertEqual(
            result2,
            "Duplicate patient ID"
        )
    def test_06_invalid_oxygen_level(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P006",
            40,
            150,
            80,
            120,
            37.0,
            False
        )
        result = system.add_patient(patient)
        self.assertEqual(
            result,
            "Invalid oxygen level"
        )
    def test_07_invalid_heart_rate(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P007",
            40,
            95,
            0,
            120,
            37.0,
            False
        )
        result = system.add_patient(patient)
        self.assertEqual(
            result,
            "Invalid heart rate"
        )
    def test_08_priority_boundary_values(self):
        system = ICUAllocationSystem(1)
        patient = Patient(
            "P008",
            30,
            90,
            111,
            120,
            37.0,
            False
        )
        system.add_patient(patient)
        priority, score = system.get_patient_priority("P008")
        self.assertIn(
            priority,
            ["MEDIUM", "HIGH"]
        )
        self.assertGreater(
            score,
            0
        )
    def test_09_multiple_patients_competing_for_same_bed(self):
        system = ICUAllocationSystem(1)
        critical_patient = Patient(
            "P009",
            70,
            80,
            140,
            70,
            40.0,
            True
        )
        normal_patient = Patient(
            "P010",
            30,
            98,
            75,
            120,
            37.0,
            False
        )
        system.add_patient(normal_patient)
        system.add_patient(critical_patient)
        result = system.allocate_by_priority()
        self.assertIn(
            "P009",
            system.allocated_beds
        )
        self.assertIn(
            "P010",
            system.get_waiting_list()
        )
class JenkinsPipelineTextResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        test_name = (
            test._testMethodName
            .split("_", 2)[-1]
            .replace("_", " ")
            .capitalize()
        )
        self.stream.write(
            f" -> Verifying Step: {test_name:<40} "
        )
        self.stream.flush()
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln("[ PASSED ]")
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln("[ FAILED ]")
if __name__ == "__main__":
    print("=" * 65)
    print(" EXECUTING ICU ALLOCATION QA PIPELINE STAGES ")
    print("=" * 65)
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=JenkinsPipelineTextResult
    )
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestICUAllocationQA
    )
    result = runner.run(suite)
    print("=" * 65)
    if result.wasSuccessful():
        print(
            "PIPELINE STATUS: ALL 9 ICU ALLOCATION CHECKS PASSED SUCCESSFULLY"
        )
    else:
        print(
            "PIPELINE STATUS: FAILURE DETECTED IN TEST SUITE"
        )
    print("=" * 65)