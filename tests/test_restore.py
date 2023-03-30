import unittest
import io
import mock
from unittest.mock import patch
from datetime import datetime, timedelta
import utils

class TestFunctions(unittest.TestCase):

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_db_default(self, mock_stdout):
        with patch('builtins.input', side_effect=['Fracture Case','Snakebite case', 'dreams and nightmares', 'FAZE holo 2022 antwerp', 'G2 holo 2022 antwerp', ' ak47 anubis Field tested', 'driver gloves overtake battle scarred', 'huntsman tiger tooth facory new', 'q']):
            utils.add_items_by_user_input()
            self.assertIn("Fracture Case", mock_stdout.getvalue())
        utils.display_stored_items()
        self.assertIn("Fracture Case", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)