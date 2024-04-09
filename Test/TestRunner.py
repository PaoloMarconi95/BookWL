import unittest
from Test.Tasks.test_booking import TestBooking
from Test.Workflows.test_mainBooking import TestMainBooking

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestBooking))
    test_suite.addTest(unittest.makeSuite(TestMainBooking))

    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
