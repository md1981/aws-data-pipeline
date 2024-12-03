import unittest
from app.main import process_data

class TestMain(unittest.TestCase):
    def test_process_data(self):
        input_data = "hello world"
        expected_output = "HELLO WORLD"
        self.assertEqual(process_data(input_data), expected_output)

    def test_process_data_empty_string(self):
        input_data = ""
        expected_output = ""
        self.assertEqual(process_data(input_data), expected_output)

if __name__ == '__main__':
    unittest.main()
