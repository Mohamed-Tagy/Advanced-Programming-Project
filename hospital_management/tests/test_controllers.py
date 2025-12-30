import unittest
from hospital_management.controllers.hospital_controller import HospitalController

class TestControllers(unittest.TestCase):
    def setUp(self):
        self.controller = HospitalController()

    def test_dummy(self):
        # Placeholder test so unittest runs
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
