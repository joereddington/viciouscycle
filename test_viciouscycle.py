import unittest
from unittest.mock import patch

# Assuming the handle_measurement function is in a file named 'sensor.py'
from viciouscycle import handle_measurement

class TestVC(unittest.TestCase):

    def setUp(self):
        # Set up any required state or variables
        global prev_cumulative_crank_revolutions, prev_last_crank_event_time
        prev_cumulative_crank_revolutions = None
        prev_last_crank_event_time = None

    @patch('viciouscycle.prev_cumulative_crank_revolutions', None)
    @patch('viciouscycle.prev_last_crank_event_time', None)
    def test_handle_measurement_wheel_data(self):

        # Simulate data with only wheel revolution data
        data = bytearray([0x01, 0x78, 0x56, 0x34, 0x12, 0x01, 0x00])
        result=handle_measurement(None, data)
        self.assertEqual(result,0) 
        # Assertions to check if values are parsed correctly
        self.assertEqual(prev_cumulative_crank_revolutions, None)
        self.assertEqual(prev_last_crank_event_time, None)

    @patch('viciouscycle.prev_cumulative_crank_revolutions', None)
    @patch('viciouscycle.prev_last_crank_event_time', None)
    def test_handle_measurement_crank_data(self):
        # Simulate data with only crank revolution data
        data = bytearray([0x02, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00])
        handle_measurement(None, data)

        # Assertions to check if values are parsed correctly
        self.assertEqual(prev_cumulative_crank_revolutions, 1)
        self.assertEqual(prev_last_crank_event_time, 2)

    @patch('viciouscycle.prev_cumulative_crank_revolutions', None)
    @patch('viciouscycle.prev_last_crank_event_time', None)
    def test_handle_measurement_wheel_and_crank_data(self):
        # Simulate data with both wheel and crank revolution data
        data = bytearray([0x03, 0x78, 0x56, 0x34, 0x12, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00])
        handle_measurement(None, data)

        # Assertions to check if values are parsed correctly
        self.assertEqual(prev_cumulative_crank_revolutions, 2)
        self.assertEqual(prev_last_crank_event_time, 3)

    @patch('viciouscycle.prev_cumulative_crank_revolutions', 0)
    @patch('viciouscycle.prev_last_crank_event_time', 0)
    def test_handle_measurement_cadence_calculation(self):
        value=handle_measurement(0,0,1, 1000)  
        self.assertEqual(value,61.44) 

    @patch('viciouscycle.prev_cumulative_crank_revolutions', 0)
    @patch('viciouscycle.prev_last_crank_event_time', 0)
    def test_handle_measurement_cadence_calculation2(self):
        value=handle_measurement(0,0,2, 1000)  
        self.assertEqual(value,122.88) 

    @patch('viciouscycle.prev_cumulative_crank_revolutions', 0)
    @patch('viciouscycle.prev_last_crank_event_time', 0)
    def test_handle_measurement_cadence_calculation3(self):
        value=handle_measurement(0,0,0, 1000)  
        self.assertEqual(value,0) 

    @patch('viciouscycle.prev_cumulative_crank_revolutions', 1)
    @patch('viciouscycle.prev_last_crank_event_time', 0)
    def test_handle_measurement_cadence_calculation3(self):
        value=handle_measurement(0,0,1, 1000)  
        self.assertEqual(value,0) 

if __name__ == '__main__':
    unittest.main()

