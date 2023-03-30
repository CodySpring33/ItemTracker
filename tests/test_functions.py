import unittest
import io
import mock
from unittest.mock import patch
from datetime import datetime, timedelta
import db
import api
import utils
import os

class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        self.test_item = ('test_item', 'http://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=Fracture%20Case')
        self.test_price = 1.99
        db.init_db()
        db.clear_database()
        
    def test_get_item_by_index(self):
        db.add_item(self.test_item[0], self.test_item[1])
        self.assertEqual(utils.get_item_by_index(0), self.test_item)
        self.assertIsNone(utils.get_item_by_index(1))
        db.clear_database()

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_stored_items(self, mock_stdout):
        db.add_item(self.test_item[0], self.test_item[1])
        utils.display_stored_items()
        self.assertIn(self.test_item[0], mock_stdout.getvalue())
        db.clear_database()

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_items_by_user_input(self, mock_stdout):
        with patch('builtins.input', side_effect=['0', 'q']):
            db.add_item(self.test_item[0], self.test_item[1])
            utils.remove_items_by_user_input()
            self.assertNotIn(self.test_item[0], mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add_items_by_user_input(self, mock_stdout):
        with patch('builtins.input', side_effect=['Fracture Case', 'q']):
            utils.add_items_by_user_input()
            db_item = utils.get_item_by_index(0)
            self.assertEqual(db_item[0], 'Fracture Case')
            self.assertEqual(db_item[1], api.search_item_url('Fracture Case'))
            db.clear_database()

    def test_get_currency_symbol(self):
        self.assertEqual(utils.get_currency_symbol(1), '$')
        self.assertEqual(utils.get_currency_symbol(2), '£')
        self.assertEqual(utils.get_currency_symbol(100), '')

    def test_update_currency(self):
        db.add_item(self.test_item[0], self.test_item[1])
        utils.update_currency(2)
        db_item = utils.get_item_by_index(0)
        self.assertIn('£', os.getenv('CURRENCY'))
        self.assertIn('2', os.getenv('CODE'))
        self.assertIn(f"http://steamcommunity.com/market/priceoverview/?appid=730&currency={os.getenv('CODE')}", db_item[1])
        db.clear_database()
        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)