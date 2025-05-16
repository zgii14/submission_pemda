import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import simpan_ke_csv, simpan_ke_google_sheets, simpan_ke_postgresql

class TestLoad(unittest.TestCase):

    def test_simpan_ke_csv(self):
        df = pd.DataFrame({'col1': [1,2], 'col2': [3,4]})
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            simpan_ke_csv(df, "dummy.csv")
            mock_to_csv.assert_called_once_with("dummy.csv", index=False)

    @patch('os.path.exists')
    @patch('utils.load.build')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_simpan_ke_google_sheets_berhasil(self, mock_creds, mock_build, mock_exists):
        mock_exists.return_value = True
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheets
        mock_sheets.values.return_value.update.return_value.execute.return_value = None

        df = pd.DataFrame({'col1': [1], 'col2': [2]})

        simpan_ke_google_sheets(df, 'spreadsheet_id', 'Sheet1!A1')

        mock_build.assert_called_once()
        mock_sheets.values.return_value.update.assert_called_once()

    @patch('os.path.exists')
    def test_simpan_ke_google_sheets_file_key_tidak_ada(self, mock_exists):
        mock_exists.return_value = False
        df = pd.DataFrame({'col1': [1]})

        with patch('builtins.print') as mock_print:
            simpan_ke_google_sheets(df, 'spreadsheet_id', 'Sheet1!A1')
            mock_print.assert_any_call("❌ File key_api.json tidak ditemukan, lewati upload ke Google Sheets.")

    @patch('os.path.exists')
    @patch('utils.load.build')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_simpan_ke_google_sheets_gagal(self, mock_creds, mock_build, mock_exists):
        mock_exists.return_value = True
        mock_build.side_effect = Exception("API error")

        df = pd.DataFrame({'col1': [1]})

        with patch('builtins.print') as mock_print:
            simpan_ke_google_sheets(df, 'spreadsheet_id', 'Sheet1!A1')
            printed_messages = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertTrue(any("❌ Gagal simpan ke Google Sheets:" in msg for msg in printed_messages))

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_berhasil(self, mock_create_engine):
        df = pd.DataFrame({'col1': [1], 'col2': [2]})
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch.object(df, 'to_sql') as mock_to_sql, patch('builtins.print') as mock_print:
            simpan_ke_postgresql(df, 'products')
            mock_create_engine.assert_called_once_with(
                'postgresql+psycopg2://postgres:rozagiro12@localhost:5432/product_db'
            )
            mock_to_sql.assert_called_once_with('products', mock_engine, if_exists='replace', index=False)
            mock_print.assert_any_call("✅ Data berhasil disimpan ke tabel PostgreSQL 'products'.")

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_gagal(self, mock_create_engine):
        df = pd.DataFrame({'col1': [1]})
        mock_create_engine.side_effect = Exception("Koneksi gagal")

        with patch('builtins.print') as mock_print:
            simpan_ke_postgresql(df, 'products')
            printed_messages = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertTrue(any("❌Gagal menyimpan data ke PostgreSQL:" in msg for msg in printed_messages))


if __name__ == '__main__':
    unittest.main()
