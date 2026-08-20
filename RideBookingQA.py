import unittest
from RideBooking import RideBooking
class TestRideBookingQA(unittest.TestCase):
    def setUp(self):
        self.booking = RideBooking(
            customer_id="C001",
            pickup_location="VIT Vellore",
            drop_location="Katpadi",
            distance=10,
            passengers=2,
            vehicle_type="Sedan",
            booking_time="10:00",
            driver_available=True
        )
    def test_01_normal_booking(self):
        result = self.booking.calculate_fare()
        self.assertEqual(result, 210)
    def test_02_peak_hour_booking(self):
        normal_booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            10,
            2,
            "Sedan",
            "10:00",
            True
        )
        peak_booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            10,
            2,
            "Sedan",
            "18:00",
            True
        )
        normal_fare = normal_booking.calculate_fare()
        peak_fare = peak_booking.calculate_fare()
        self.assertGreater(peak_fare, normal_fare)
    def test_03_night_booking(self):
        night_booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            10,
            2,
            "Sedan",
            "23:00",
            True
        )
        result = night_booking.calculate_fare()
        self.assertEqual(result, 250)
    def test_04_invalid_distance(self):
        booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            0,
            2,
            "Sedan",
            "10:00",
            True
        )
        result = booking.calculate_fare()
        self.assertEqual(
            result,
            "Invalid booking: Zero or negative distance"
        )
    def test_05_invalid_passenger_count(self):
        booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            10,
            0,
            "Sedan",
            "10:00",
            True
        )
        result = booking.calculate_fare()
        self.assertEqual(
            result,
            "Invalid booking: Invalid passenger count"
        )
    def test_06_unavailable_driver(self):
        booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            10,
            2,
            "Sedan",
            "10:00",
            False
        )
        result = booking.calculate_fare()
        self.assertEqual(
            result,
            "Invalid booking: Driver unavailable"
        )
    def test_07_maximum_discount(self):
        booking = RideBooking(
            "C001",
            "VIT",
            "Chennai",
            20,
            2,
            "Sedan",
            "10:00",
            True
        )
        result = booking.calculate_fare()
        expected = 60 + (20 * 15) - 50
        self.assertEqual(result, expected)
    def test_08_multiple_vehicle_types(self):
        bike = RideBooking(
            "C001", "VIT", "Katpadi",
            10, 2, "Bike", "10:00", True
        )
        sedan = RideBooking(
            "C001", "VIT", "Katpadi",
            10, 2, "Sedan", "10:00", True
        )
        suv = RideBooking(
            "C001", "VIT", "Katpadi",
            10, 2, "SUV", "10:00", True
        )
        premium = RideBooking(
            "C001", "VIT", "Katpadi",
            10, 2, "Premium", "10:00", True
        )
        bike_fare = bike.calculate_fare()
        sedan_fare = sedan.calculate_fare()
        suv_fare = suv.calculate_fare()
        premium_fare = premium.calculate_fare()
        self.assertLess(bike_fare, sedan_fare)
        self.assertLess(sedan_fare, suv_fare)
        self.assertLess(suv_fare, premium_fare)
    def test_09_boundary_values(self):
        booking = RideBooking(
            "C001",
            "VIT",
            "Katpadi",
            1,
            1,
            "Bike",
            "10:00",
            True
        )
        result = booking.calculate_fare()
        self.assertEqual(result, 40)
    def test_10_driver_allocation_logic(self):
        result = self.booking.allocate_driver()
        self.assertEqual(
            result,
            "Driver allocated successfully"
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
            f" -> Verifying Step: {test_name:<30} "
        )
        self.stream.flush()
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln("[ PASSED ]")
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln("[ FAILED ]")
if __name__ == "__main__":
    print("=" * 60)
    print(" EXECUTING RIDE BOOKING QA PIPELINE STAGES ")
    print("=" * 60)
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=JenkinsPipelineTextResult
    )
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestRideBookingQA
    )
    result = runner.run(suite)
    print("=" * 60)
    if result.wasSuccessful():
        print(
            "PIPELINE STATUS: ALL 10 RIDE BOOKING CHECKS PASSED SUCCESSFULLY"
        )
    else:
        print(
            "PIPELINE STATUS: FAILURE DETECTED IN TEST SUITE"
        )