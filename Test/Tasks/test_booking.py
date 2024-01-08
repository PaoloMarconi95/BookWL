import unittest
from Workflows import WEBDRIVERFACTORY
from Exceptions import NoReservationFoundException
import os
from Tasks.Booking import *
from pathlib import Path

wd = WEBDRIVERFACTORY.get_driver()
wd.get('file://' + os.path.join(Path(__file__).parent.parent, 'html_pages', 'booking_test.html'))

class TestBooking(unittest.TestCase):

    def test_get_all_classes(self):
        result = get_all_classes_for_date(wd, '2024-01-03')
        self.assertEqual(len(result), 7)


    def test_get_booked_class(self):
        result = get_booked_row_for_datetime(wd, '2024-01-03', '18')
        class_name = result.text.split('\n')[0]
        class_program = result.text.split('\n')[3]
        class_time = result.text.split('\n')[4]
        self.assertEqual(class_name, '18:00 WOD')
        self.assertEqual(class_program, 'CrossFit WOD')
        self.assertEqual(class_time, '18:00')


    def test_find_booking_row_by_class_name_correct(self):
        # Already booked class
        classes = get_all_classes_for_date(wd, '2024-01-03')
        row = find_row_for_class_name(classes, '18:00 WOD')
        self.assertNotEqual(row, None)
        el = find_clickable_booking_element(row[0])
        self.assertEqual(el, None)


    def test_find_booking_row_by_class_name_correct_exception(self):
        classes = get_all_classes_for_date(wd, '2024-01-03')
        with self.assertRaises(NoReservationFoundException):
            find_row_for_class_name(classes, '22:00 WOD')


    def test_get_booked_row_for_datetime(self):
        booked_crossfit_class = CrossFitClass(date='2024-01-03', id=None, name='18:00 WOD', program='CrossFit WOD', time='18:00')
        non_booked_crossfit_class = CrossFitClass(date='2024-01-03', id=None, name='17:00 WOD', program='CrossFit WOD', time='18:00')
        result_booked = is_still_booked(booked_crossfit_class, wd)
        result_non_booked = is_still_booked(non_booked_crossfit_class, wd)
        self.assertTrue(result_booked)
        self.assertFalse(result_non_booked)


if __name__ == '__main__':
    unittest.main()