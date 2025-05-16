import unittest
import pandas as pd
from utils.transform import bersihkan_dan_ubah

class TestTransform(unittest.TestCase):

    def test_transform_data_normal(self):
        data_input = [
            {'title': 'Baju Keren', 'price': '100.00', 'rating': 'Rating: 4.5', 'colors': 'Colors: 3', 'size': 'Size: L', 'gender': 'Gender: Male'},
            {'title': 'Unknown Title', 'price': '50.00', 'rating': 'Rating: 3.5', 'colors': 'Colors: 2', 'size': 'Size: M', 'gender': 'Gender: Female'}
        ]
        df = bersihkan_dan_ubah(data_input)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertNotIn('Unknown Title', df['title'].values)
        self.assertTrue('timestamp' in df.columns)
        self.assertEqual(len(df), 1)  # Unknown Title harus di filter

    def test_transform_data_empty(self):
        df = bersihkan_dan_ubah([])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 0)
        self.assertListEqual(
            list(df.columns),
            ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        )

if __name__ == '__main__':
    unittest.main()
