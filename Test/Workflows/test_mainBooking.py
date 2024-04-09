import unittest
from Workflows import WEBDRIVERFACTORY
from Exceptions import NoReservationFoundException
import os
from Tasks.Booking import *
from pathlib import Path

wd = WEBDRIVERFACTORY.get_driver()
wd.get('file://' + os.path.join(Path(__file__).parent.parent, 'html_pages', 'booking_test.html'))

class TestMainBooking(unittest.TestCase):

    def test_get_row_and_clickable_calendar(self):
        book: FutureBooking = FutureBooking(class_name='12:30 WOD', class_program='CrossFit WOD', class_time='12:30', user_id=0, week_day=0)

        classes = get_all_classes_for_date(wd, '03-01-2024')
        self.assertEqual(len(classes), 7)

        booked_row = find_row_for_class_name(classes, book.class_name)
        self.assertIsNotNone(booked_row)
        self.assertEqual(len(booked_row), 1)

        booking_button = find_clickable_booking_element(booked_row[0])
        self.assertIsNotNone(booking_button)


    def test_analyze_result_booked(self):
        book: FutureBooking = FutureBooking(class_name='18:00 WOD', class_program='CrossFit WOD', class_time='12:30', user_id=0, week_day=0)
        classes = get_all_classes_for_date(wd, '03-01-2024')
        booked_row = find_row_for_class_name(classes, book.class_name)
        result = analyze_booking_result(booked_row[0])
        self.assertEqual(result, BookingResult.SUCCESS)


    def test_analyze_result_non_booked(self):
        book: FutureBooking = FutureBooking(class_name='12:30 WOD', class_program='CrossFit WOD', class_time='12:30', user_id=0, week_day=0)
        classes = get_all_classes_for_date(wd, '03-01-2024')
        booked_row = find_row_for_class_name(classes, book.class_name)
        result = analyze_booking_result(booked_row[0])
        self.assertEqual(result, BookingResult.FAIL)



if __name__ == '__main__':
    unittest.main()