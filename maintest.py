import multiprocessing
import os
from bs4 import Comment
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv

PROVINSI_DEFAULT = "DKI Jakarta"
KABUPATEN_KOTA_DEFAULT = "Kota Administrasi Jakarta Selatan"

def scrapping_maps(query,kecamatan_name, max_scroll_attempts=15, process_id="Main", scroll_pause_time=2):
    options = webdriver.ChromeOptions() 

    options.add_argument('--lang=id-ID')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        ),
        options=options
    )

    driver.get("https://www.google.com/maps")

    scrapped_places = []

    try:
        """
        <form class="NhWQq" id="XmI62e" spellcheck="false" jsaction="submit:omnibox.searchboxFormSubmit">
        <input class="fontBodyMedium searchboxinput xiQnY " role="combobox" jslog="11886" aria-controls="ydp1wd-haAclf" aria-expanded="false" aria-haspopup="grid" autocomplete="off" id="searchboxinput" name="q" jsaction="keyup:omnibox.keyUp; input:omnibox.inputDetected; keydown:omnibox.keyDown; focus:omnibox.focus; blur:omnibox.blur"></form>
        """
        #we want to get by id inside form that contain searchboxinput id
        search_box = WebDriverWait(
            driver, 10
        ).until(
            EC.presence_of_element_located(
                (By.ID, "searchboxinput")
            )
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        """
        <div class="Nv2PK tH5CWc THOPZb " jsaction="mouseover:pane.wfvdle73;mouseout:pane.wfvdle73">
        <a class="hfpxzc" aria-label="BNI ATM" href="https://www.google.com/maps/place/BNI+ATM/data=!4m7!3m6!1s0x2e69ee2d5a97f3f1:0xe6fa3c3c2fd15d18!8m2!3d-6.3105218!4d106.7714204!16s%2Fg%2F1pzt__prr!19sChIJ8fOXWi3uaS4RGF3RLzw8-uY?authuser=0&amp;hl=id&amp;rclk=1" jsaction="pane.wfvdle73;focus:pane.wfvdle73;blur:pane.wfvdle73;auxclick:pane.wfvdle73;keydown:pane.wfvdle73;clickmod:pane.wfvdle73" jslog="12690;track:click,contextmenu;mutable:true;metadata:WyIwYWhVS0V3aXhfZURyeGFlTkF4WHk5emdHSFQ5Rk4yY1E4QmNJZHlnSSIsbnVsbCwzXQ=="></a><div class="rWbY0d"></div><div class="bfdHYd Ppzolf OFBs3e  "><div class="rgFiGf OyjIsf "></div><div class="hHbUWd"></div><div class="rSy5If"></div><div class="lI9IFe "><div class="y7PRA"><div class="Lui3Od T7Wufd "><div class="Z8fK3b"><div class="OyjIsf "></div><div class="UaQhfb fontBodyMedium"><div class="NrDZNb"><div class="dIDW9d"></div><span class="HTCGSb"></span><div class="qBF1Pd fontHeadlineSmall ">BNI ATM</div> <span class="muMOJe"></span></div><div class="HAthLd"></div><div class="W4Efsd"><div class="AJB7ye"><span class="wZrhX"></span> <span class="e4rVHe fontBodyMedium"><span role="img" class="ZkP5Je" aria-label="4,6 bintang 7 Ulasan"><span class="MW4etd" aria-hidden="true">4,6</span><div class="QBUL8c "></div><div class="QBUL8c "></div><div class="QBUL8c "></div><div class="QBUL8c "></div><div class="QBUL8c vIBWLc "></div><span class="UY7F9" aria-hidden="true">(7)</span></span></span></div></div><div class="W4Efsd"><div class="W4Efsd"><span><span>ATM</span></span><span> <span aria-hidden="true">·</span> <span>Jl. Raya Cirendeu, RT.14/RW.3</span></span></div><div class="W4Efsd"><span><span><span style="font-weight: 400; color: rgba(25,134,57,1.00);">Buka</span><span style="font-weight: 400;"> ⋅ Tutup pukul 23.00</span></span></span><span> <span aria-hidden="true">·</span> <span class="UsdlK">(021) 57899999</span></span></div></div></div></div></div></div><div class="Rwjeuc"><div class="etWJQ jym1ob kdfrQc k17Vqe NUqjXc"><a class="lcr4fd S9kvJb " jsaction="pane.wfvdle75;keydown:pane.wfvdle75;mouseover:pane.wfvdle75;mouseout:pane.wfvdle75" aria-label="Kunjungi situs BNI ATM" data-value="Situs Web" jslog="84919;track:click;mutable:true;metadata:WyIwYWhVS0V3aXhfZURyeGFlTkF4WHk5emdHSFQ5Rk4yY1E4QmNJZHlnSSIsIixBT3ZWYXcyWlpTb2N1UW16TEJJY2VZUkJaNFlnLCwwYWhVS0V3aXhfZURyeGFlTkF4WHk5emdHSFQ5Rk4yY1E2MWdJaWdFb0VRLCJd" href="http://www.bni.co.id/"><span class="DVeyrd "><div class="OyjIsf zemfqc"></div><span class="Cw1rxd google-symbols PHazN" aria-hidden="true" style="font-size: 18px;"></span></span><div class="R8c4Qb fontLabelMedium">Situs Web</div></a></div><div class="etWJQ jym1ob kdfrQc k17Vqe NUqjXc"><button class="g88MCb S9kvJb " jsaction="pane.wfvdle76;keydown:pane.wfvdle76;mouseover:pane.wfvdle76;mouseout:pane.wfvdle76" aria-label="Lihat rute ke BNI ATM" data-value="Rute" jslog="80860;track:click;mutable:true;metadata:WyIwYWhVS0V3aXhfZURyeGFlTkF4WHk5emdHSFQ5Rk4yY1E4QmNJZHlnSSJd"><span class="DVeyrd "><div class="OyjIsf zemfqc"></div><span class="Cw1rxd google-symbols G47vBd PHazN" aria-hidden="true" style="font-size: 18px;"></span></span><div class="R8c4Qb fontLabelMedium">Rute</div></button></div></div><div class="SpFAAb"></div></div><div class="qty3Ue"></div><div class="gwQ6lc" jsaction="click:mLt3mc"></div></div></div>
        """
        #we want to get a class inside div that contain hfpxzc class
        # WebDriverWait(
        #     driver, 20
        # ).until(
        #     EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, "a.hfpxzc")
        #     )
        # )
        # time.sleep(3)

        """
        <div class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd" aria-label="Hasil untuk atm bca di cilandak" role="feed" tabindex="-1" style="">
        """
        feed_xpath = "//div[@role='feed']"
        #we want to get by role inside div that contain role feed
        WebDriverWait(
            driver, 20
        ).until(
            EC.presence_of_element_located(
                (By.XPATH, feed_xpath)
            )
        )

        time.sleep(3)

        scrollable_div_xpath = "//div[@role='feed' and @aria-label]" # More general

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, scrollable_div_xpath)))
            print(f"[{process_id}] Scrollable feed div (xpath: {scrollable_div_xpath}) found for query: {query}")
        except TimeoutException:
            print(f"[{process_id}] Scrollable feed div (xpath: {scrollable_div_xpath}) not found for query: {query}. Scraping might fail or be incomplete.")
            # Attempt to find any feed div if the specific one fails
            alt_feed_xpath = "//div[@role='feed']"
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, alt_feed_xpath)))
                scrollable_div_xpath = alt_feed_xpath # Use the alternative
                print(f"[{process_id}] Using alternative scrollable feed div (xpath: {alt_feed_xpath}) for query: {query}")
            except TimeoutException:
                print(f"[{process_id}] Alternative scrollable feed div also not found for query: {query}. Aborting this query.")
                if driver: driver.quit()
                return [] # Return empty if no scrollable feed found

        time.sleep(2) # Allow initial items in feed to render

        end_of_list_text = "Anda telah mencapai akhir daftar."
        scroll_attempts = 0
        
        try:
            scrollable_element = driver.find_element(By.XPATH, scrollable_div_xpath)
            last_scroll_height = 0
            no_change_count = 0

            while scroll_attempts < max_scroll_attempts:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
                time.sleep(scroll_pause_time) # Wait for content to load

                page_html_after_scroll = driver.page_source
                if end_of_list_text in page_html_after_scroll:
                    print(f"[{process_id}] '{end_of_list_text}' found for query: {query}. Stopping scroll.")
                    break

                current_scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
                if current_scroll_height == last_scroll_height:
                    no_change_count +=1
                    print(f"[{process_id}] Scroll height unchanged for query: {query} (Attempt {no_change_count}/2)")
                else:
                    no_change_count = 0
                
                if no_change_count >= 2: # If scroll height hasn't changed for 2 consecutive tries
                    print(f"[{process_id}] Scroll height stable for query: {query}. Assuming end of list or no new content.")
                    break
                last_scroll_height = current_scroll_height

                scroll_attempts += 1
                print(f"[{process_id}] Scroll attempt {scroll_attempts} for query: {query}")

            if scroll_attempts >= max_scroll_attempts:
                print(f"[{process_id}] Max scroll attempts reached for query: {query}.")

        except NoSuchElementException:
            print(f"[{process_id}] Could not find the scrollable element for scrolling for query: {query}. Proceeding with current view.")
        except Exception as e_scroll:
            print(f"[{process_id}] Error during scrolling for query: {query}: {e_scroll}")

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        feed_div = soup.find(
            'div', 
            {
                'role': 'feed'
            }
        )

        if not feed_div:
            print("Feed div not found.")
            return []  # Return an empty list if feed div is not found  

        place_item_containers = feed_div.find_all(
            'div',
            class_='Nv2PK',
            recursive=False
        )
        print(f"Attempt 1 (class_='Nv2PK'): Found {len(place_item_containers)} containers.")

        if not place_item_containers:
            print("Debug place_item_containers activated in role:article")
            place_item_containers = feed_div.find_all('div', {'role': 'article'}, recursive=False)
        if not place_item_containers:
            print("Debug place_item_containers activated in div")
            place_item_containers = feed_div.find_all('div', recursive=False)

        print(f"Found {len(place_item_containers)} potential place item containers.")

        for item_container in place_item_containers:
            name = "N/A"
            lat, lon = "N/A", "N/A"
            street_address_sufix = ""
            full_address = []

            name_tag = item_container.find('a', class_=re.compile(r'\bhfpxzc\b'))
            if name_tag:
                name = name_tag.get('aria-label', 'N/A').strip()
            else:
                name_tag = item_container.find(['div', 'span'], class_=re.compile(r'fontHeadlineSmall'))
                if name_tag:
                    name = name_tag.get_text(strip=True)
            
            if not name or name == "N/A":
                print(f"Name not found for an item. HTML snippet: {str(item_container)[:200]}")
                continue

            details_block = item_container.find(
                'div',
                class_=re.compile(r'UaQhfb')
            )

            if details_block:
                detail_spans = details_block.find_all(
                    'span',
                    string=True
                )

                current_line_parts = []
                for span in detail_spans:
                    text = span.text.strip()
                    if not text:
                        print("Empty span found.")
                        continue

                    if text == "." and current_line_parts:
                        full_address.append(" ".join(current_line_parts))
                        current_line_parts = []
                        continue
                        
                    current_line_parts.append(text)

                    if ("Jl." in text or "Jalan" in text or "rt." in text.lower() or "rw." in text.lower()) and not street_address_sufix:
                        if "Jl." in text:
                            street_address_sufix = text[text.find("Jl."):]
                        elif "Jalan" in text:
                             street_address_sufix = text[text.find("Jalan"):]
                        elif "RT." in text.upper(): 
                            words = text.split()
                            for i, word in enumerate(words):
                                if "RT." in word.upper():
                                    street_address_sufix = " ".join(words[i:])
                                    break
                        elif street_address_sufix:
                            street_address_sufix += " " + text

                if current_line_parts:
                    full_address.append(" ".join(current_line_parts))

            if street_address_sufix:
                # Example: "MQQJ+FH3, Indomaret Plus, Jl. Karang Tengah Raya, RT.4/RW.3"
                if "Jl." in street_address_sufix:
                    street_address_sufix = street_address_sufix[street_address_sufix.find("Jl."):]
                elif "Jalan" in street_address_sufix:
                    street_address_sufix = street_address_sufix[street_address_sufix.find("Jalan"):]
                
                street_address_sufix = re.sub(r'\s*(Buka|Tutup).*$', '', street_address_sufix, flags=re.IGNORECASE).strip()

            main_link_for_coords = item_container.find(
                'a',
                class_=re.compile(r'hfpxzc'),
                href=True
            )

            if main_link_for_coords:
                href = main_link_for_coords.get('href')
                if href:
                    match_at = re.search(r'/@(-?\d+\.\d+),(-?\d+\.\d+)', href)
                    if match_at:
                        lat, lon = match_at.group(1), match_at.group(2)
                    else: 
                        match_3d = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', href)
                        if match_3d:
                            lat, lon = match_3d.group(1), match_3d.group(2)

            final_name = name
            if street_address_sufix:
                if "Jl." in street_address_sufix or "Jalan" in street_address_sufix or \
                   "RT." in street_address_sufix.upper() or "RW." in street_address_sufix.upper():
                    final_name += f" - {street_address_sufix}"

            place_data = {
                "Provinsi": PROVINSI_DEFAULT,
                "Kabupaten/Kota": KABUPATEN_KOTA_DEFAULT,
                "Kecamatan": kecamatan_name,
                "Name with Street": final_name,
                "Original Name": name.strip(),
                "Street Detail": street_address_sufix.strip(),
                "Full Address Info": " | ".join(full_address).strip(),
                "Latitude": lat,
                "Longitude": lon
            }
            
            scrapped_places.append(place_data)
    except Exception as e:
        print(f"Overall error: {e}")
    finally:
        driver.quit()

    return scrapped_places

if __name__ == "__main__":
    multiprocessing.freeze_support() # MUST be the first line inside this block

    # On macOS, Python 3.8+ defaults to 'spawn'.
    # Setting start method to 'fork' can resolve the "RuntimeError: An attempt has been made..."
    # This must be done before any Pool or Process is created.
    if os.name == 'posix': # 'posix' includes macOS and Linux
        try:
            current_method = multiprocessing.get_start_method(allow_none=True)
            if current_method != 'fork': # Only set if not already fork or if it's spawn/default
                multiprocessing.set_start_method('fork')
                print(f"INFO: Multiprocessing start method set to 'fork'.")
        except RuntimeError as e:
            # This can happen if it's already been set or if processes have started.
            print(f"WARNING: Could not set multiprocessing start method to 'fork': {e}. Current method: {multiprocessing.get_start_method(allow_none=True)}")

        kecamatan_jakarta_selatan = [
            "Cilandak", "Jagakarsa", "Kebayoran Baru", "Kebayoran Lama",
            "Mampang Prapatan", "Pancoran", "Pasar Minggu", "Pesanggrahan",
            "Setiabudi", "Tebet"
        ]

        base_query_subject = 'ATM BNI'


        all_scraped_data = []
        tasks_with_ids = []

        for i, kec in enumerate(kecamatan_jakarta_selatan):
            query = f"{base_query_subject} di kecamatan {kec}"
            tasks_with_ids.append((query, f"Worker-{i+1}", kec))

        num_processes = min(len(tasks_with_ids), os.cpu_count() or 1, 5)
        print(f"Starting parallel scraping with {num_processes} processes for {len(tasks_with_ids)} queries...")


        def worker(query, process_id, kecamatan):
            return scrapping_maps(
                query=query, 
                kecamatan_name=kecamatan,
                process_id=process_id, 
                max_scroll_attempts=50, 
                scroll_pause_time=2
            )

        start_time = time.time()
        with multiprocessing.Pool(processes=num_processes) as pool:
            results_list_of_lists = pool.starmap(worker, tasks_with_ids)

        for single_query_result in results_list_of_lists:
            all_scraped_data.extend(single_query_result)

        end_time = time.time()
        print(f"\n--- Total scraping time: {end_time - start_time:.2f} seconds ---")
        print(f"--- Scraped {len(all_scraped_data)} Places in Total ---")


        #search_query = "atm bca di kecamatan cilandak"
        #data = scrapping_maps(search_query) 

        print(f"\n--- Scraped {len(all_scraped_data)} Places ---")
        for i, place in enumerate(all_scraped_data):
                print(f"\nPlace {i+1}:")
                print(f"  Provinsi: {place['Provinsi']}")
                print(f"  Kabupaten/Kota: {place['Kabupaten/Kota']}")
                print(f"  Kecamatan: {place['Kecamatan']}")
                print(f"  Name with Street: {place['Name with Street']}")
                print(f"  Original Name: {place['Original Name']}")
                print(f"  Street Detail: {place['Street Detail']}")
                print(f"  Full Address Info: {place['Full Address Info']}")
                print(f"  Latitude: {place['Latitude']}")
                print(f"  Longitude: {place['Longitude']}")


        output_csv_filename = "scraped_bni_atm_jakarta_selatan.csv"
        csv_headers = [
            "Provinsi", "Kabupaten/Kota", "Kecamatan",
            "Name with Street", "Original Name", "Street Detail",
            "Full Address Info", "Latitude", "Longitude"
        ]

        try:
            with open(output_csv_filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=csv_headers)
                writer.writeheader()
                for place_data in all_scraped_data:
                    # Ensure all keys exist, defaulting to "N/A" if not (though they should exist)
                    row_to_write = {header: place_data.get(header, "N/A") for header in csv_headers}
                    writer.writerow(row_to_write)
            print(f"\n--- Successfully saved {len(all_scraped_data)} unique places to {output_csv_filename} ---")
        except Exception as e:
            print(f"\n--- Error saving data to CSV: {e} ---")


                
                    