import unittest
import io
import sys
import mock
from unittest.mock import patch
from datetime import datetime, timedelta
import db
import api
import main

class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        self.test_item = ('test_item', 'http://example.com')
        self.test_price = 1.99
        
    def test_get_item_by_index(self):
        db.store_item(self.test_item[0], self.test_item[1], self.test_price)
        self.assertEqual(db.get_item_by_index(0), self.test_item)
        self.assertIsNone(db.get_item_by_index(1))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_stored_items(self, mock_stdout):
        db.store_item(self.test_item[0], self.test_item[1], self.test_price)
        main.display_stored_items()
        self.assertIn(self.test_item[0], mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_items_by_user_input(self, mock_stdout):
        with patch('builtins.input', side_effect=['0', 'q']):
            db.store_item(self.test_item[0], self.test_item[1], self.test_price)
            main.remove_items_by_user_input()
            self.assertNotIn(self.test_item[0], mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add_items_by_user_input(self, mock_stdout):
        with patch('builtins.input', side_effect=['test_item', 'q']):
            main.add_items_by_user_input()
            db_item = db.get_item_by_index(0)
            self.assertEqual(db_item[0], 'test_item')
            self.assertEqual(db_item[1], api.build_steam_url('test_item'))

    def test_get_currency_symbol(self):
        self.assertEqual(main.get_currency_symbol(1), '$')
        self.assertEqual(main.get_currency_symbol(2), '£')
        self.assertEqual(main.get_currency_symbol(100), '')

    def test_update_currency(self):
        db.store_item(self.test_item[0], self.test_item[1], self.test_price)
        main.update_currency(2)
        db_item = db.get_item_by_index(0)
        self.assertIn('£', os.getenv('CURRENCY'))
        self.assertIn('2', os.getenv('CODE'))
        self.assertIn('http://steamcommunity.com/market/priceoverview/?appid=730&currency=2', db_item[1])
        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)