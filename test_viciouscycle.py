import unittest
import viciouscycle
from unittest.mock import patch
from viciouscycle import handle_measurement

class TestVC(unittest.TestCase):

    def setUp(self):
        from collections import deque
        viciouscycle.buffer = deque(maxlen=10)  # Adjust maxlen as needed; here it's 10 for example
        viciouscycle.cadence=0

    def test_cadence(self):
        handle_measurement(1,0)
        cadence=handle_measurement(2,1024)
        # Assertions to check if values are parsed correctly
        self.assertEqual(cadence,60)

    def test_handle_measurement_cadence_calculation(self):
        value=handle_measurement(1, 1000)  
        self.assertEqual(value,None) #Because you only have one calculation

    def test_handle_measurement_cadence_calculation2(self):
        handle_measurement(1,0)
        cadence=handle_measurement(1,0) #What happens if you get two the same? 
        self.assertEqual(cadence,None) 

    def test_handle_measurement_cadence_calculation3(self):
        value=handle_measurement(0, 1000)  
        self.assertEqual(value,0) 

    def test_handle_measurement_cadence_calculation3(self):
        handle_measurement(1,0)
        cadence=handle_measurement(21,1024)
        self.assertEqual(cadence,1200)

if __name__ == '__main__':
    unittest.main()

