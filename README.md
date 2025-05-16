# Google Maps Scraper - ATM BNI (Jakarta Selatan)

This Python script automates the process of scraping information about BNI ATM locations in various sub-districts (Kecamatan) of South Jakarta (Jakarta Selatan) from Google Maps. It uses Selenium for browser automation to interact with the Google Maps interface, BeautifulSoup for parsing HTML content, and `multiprocessing` for parallel scraping of multiple queries to speed up the process. The scraped data is then saved into a CSV file.

## Features

*   **Automated Searching:** Searches Google Maps for "ATM BNI" in specified sub-districts.
*   **Dynamic Scrolling:** Scrolls through the search results to load as many places as possible.
*   **Data Extraction:** Extracts the following details for each place:
    *   Provinsi (Province)
    *   Kabupaten/Kota (City/Regency)
    *   Kecamatan (Sub-district)
    *   Name with Street (Concatenated name and detailed street address)
    *   Original Name (As listed on Google Maps)
    *   Street Detail (Parsed street address component)
    *   Full Address Info (Other address lines or details)
    *   Latitude
    *   Longitude
*   **Parallel Processing:** Utilizes Python's `multiprocessing` module to run multiple scraping tasks concurrently, significantly reducing total scraping time.
*   **CSV Output:** Saves the collected data in a structured CSV file.
*   **Deduplication:** Removes duplicate entries based on Original Name, Latitude, and Longitude.
*   **Configurable:** Allows easy modification of target sub-districts, search query, and scraping parameters.

## Requirements

*   **Python 3.8+**
*   **Google Chrome Browser** (the script uses `ChromeDriverManager` to automatically manage the ChromeDriver)
*   **Python Libraries:**
    *   `selenium`
    *   `webdriver-manager`
    *   `beautifulsoup4`
    *   (Standard libraries: `multiprocessing`, `os`, `csv`, `time`, `re`)

## Setup and Installation

1.  **Clone the Repository (or download the script):**
    ```bash
    # If it were in a git repository:
    # git clone <repository-url>
    # cd <repository-directory>
    # For now, just ensure you have the script (e.g., maintest.py) in a directory.
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    source venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Required Libraries:**
    Create a `requirements.txt` file with the following content:
    ```txt
    selenium
    webdriver-manager
    beautifulsoup4
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, you can install them one by one:
    ```bash
    pip install selenium webdriver-manager beautifulsoup4
    ```

## Usage

1.  **Configure the Script (Optional):**
    Open the script (`maintest.py` or your script name) and modify the following variables near the top or in the `if __name__ == "__main__":` block if needed:
    *   `PROVINSI_DEFAULT`: Default province (currently "DKI Jakarta").
    *   `KABUPATEN_KOTA_DEFAULT`: Default city/regency (currently "Kota Administrasi Jakarta Selatan").
    *   `kecamatan_jakarta_selatan`: A list of sub-districts to search within.
    *   `base_query_subject`: The main item to search for (e.g., 'ATM BNI').
    *   `num_processes`: Number of parallel processes to use. Capped at 5 by default, and also by CPU count and number of queries.
    *   `max_scroll_attempts` (in `worker` function call): Maximum times to scroll down the results page.
    *   `scroll_pause_time` (in `worker` function call): Time to wait between scrolls.
    *   `output_csv_filename`: Name of the output CSV file.

2.  **Run the Script:**
    Execute the script from your terminal:
    ```bash
    python maintest.py
    ```

3.  **Monitor Progress:**
    The script will print progress information to the console, including which queries are being processed, scroll attempts, and any errors encountered.

4.  **Output:**
    Once the script completes, it will generate a CSV file (e.g., `scraped_bni_atm_jakarta_selatan.csv`) in the same directory. This file will contain the scraped data with the following columns:
    *   `Provinsi`
    *   `Kabupaten/Kota`
    *   `Kecamatan`
    *   `Name with Street`
    *   `Original Name`
    *   `Street Detail`
    *   `Full Address Info`
    *   `Latitude`
    *   `Longitude`

## Important Notes

*   **Web Scraping Ethics:**
    *   Web scraping can be resource-intensive for the target website. Use the script responsibly.
    *   Google Maps' terms of service may restrict automated access. Be aware of these terms.
    *   Frequent, aggressive scraping can lead to your IP address being temporarily or permanently blocked.
*   **Dynamic Content:**
    *   Websites like Google Maps frequently update their HTML structure. This scraper relies on specific class names and HTML tags. If Google Maps changes its layout, the script may break and will require updates to the selectors in the `scrapping_maps` function.
*   **Multiprocessing:**
    *   The script includes `multiprocessing.freeze_support()` which is necessary for running multiprocessing code that has been frozen to produce an executable (e.g., with PyInstaller), especially on Windows.
    *   For macOS, the multiprocessing start method is explicitly set to `'fork'` to avoid potential issues.
*   **Headless Mode:**
    *   By default, the script runs with a visible Chrome browser window for each process. To run in headless mode (without a visible UI), you can uncomment the `options.add_argument("--headless")` line and related arguments in the `scrapping_maps` function. This can be useful for servers or for less intrusive scraping.
*   **Error Handling:**
    *   The script includes basic error handling (e.g., for `TimeoutException`, `NoSuchElementException`). However, web scraping can be unpredictable, and other errors might occur.
*   **Resource Usage:**
    *   Running multiple browser instances simultaneously (due to multiprocessing) can be memory and CPU intensive. Adjust the `num_processes` variable based on your system's capabilities.

---

