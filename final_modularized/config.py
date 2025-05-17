#config.py

LOCATION_CSV_PATH = '/Users/macbookair/.cursor-tutor/project/scrapping_googlemaps/wilayah_bni_scrap.csv'
CSV_HEADERS = [
    'province_name', 
    'regency_name', 
    'district_name'
    ]
OUTPUT_CSV_PATH = '/Users/macbookair/.cursor-tutor/project/scrapping_googlemaps/wilayah_bni_scrap_clean.csv'

CSV_OUTPUT_HEADERS = [
    'Provinsi',
    'Kabupaten',
    'Kecamatan',
    'Name_with_Street',
    'Original_Name',
    'Street_Detail',
    'Full Address Info',
    'Latitude',
    'Longitude'
]

BASE_QUERY = 'ATM BNI'
GOOGLE_MAPS_URL = 'https://www.google.com/maps'
MAX_SCROLL_ATTEMPT = 50 #hARUS tinggi biar dapet semua data
SCROLL_PAUSE_TIME = 1 #udah ga ush diubah ubah
PAGE_LOAD_TIMEOUT = 20 #udah ga ush diubah ubah
SEARCH_BOX_TIMEOUT = 10
EOL_TEXT = 'Anda telah mencapai akhir daftar.'  #bawaan dari google ga ush diubah ubah

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
BROWSER_LANG = 'id-ID'
HEADLESS_BROWSER = False 

#multiprocess berapa chroome tab berjalan bersamaan
MAX_WORKERS = 5




