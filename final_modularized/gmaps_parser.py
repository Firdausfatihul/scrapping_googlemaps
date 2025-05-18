import re 
from bs4 import BeautifulSoup, Tag 

def extract_name_from_container(
    item_container, process_id="Parser"
    ):
    name = "N/A"

    name_tag_link = item_container.find('a', class_=re.compile(r'\bhfpxzc\b'))
    if name_tag_link and name_tag_link.get('aria-label'):
        name = name_tag_link.get('aria-label').strip()
        return name
    
    name_tag_headline = item_container.find(
        [
            'div',
            'span'
        ],
        class_=re.compile(r'fontHeadSmall')
    )
    if name_tag_headline:
        name = name_tag_headline.get_text(strip=True)

        return name

    if name_tag_link:
        inner_div_name = name_tag_link.find(
            'div',
            class_=re.compile(r'fontBodyMedium')
        )

        if inner_div_name and inner_div_name.get_text(strip=True):
            name = inner_div_name.get_text(strip=True)

            return name
        
        link_text = name_tag_link.get_text(strip=True)
        if link_text:
            name = link_text

            return name

    return name

def extract_coordinates_from_container(
    item_container, process_id="Parser"
    ):
    lat, lon = "N/A", "N/A"

    main_link = item_container.find(
        'a',
        class_=re.compile(r'\bhfpxzc\b'),
        href=True
    )

    if not main_link:
        return lat, lon
    
    href = main_link.get['href']

    match_at_zoom = re.search(r'/@(-?\d+\.\d+),(-?\d+\.\d+),\d+z', href)

    if match_at_zoom:
        lat, lon = match_at_zoom.group(1), match_at_zoom.group(2)

        return lat, lon

    match_at = re.search(r'/@(-?\d+\.\d+),(-?\d+\.\d+)', href)
    if match_at:
        lat, lon = match_at.group(1), match_at.group(2)

        return lat, lon

    match_data_3d4d = re.search(r'data=.*!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', href)
    if match_data_3d4d:
        lat, lon = match_data_3d4d.group(1), match_data_3d4d.group(2)

        return lat, lon 

    return lat, lon

def extract_address_details_from_container(
    item_container, process_id="Parser"
    ):
    street_detail_parts = []
    full_address_lines = []

    details_block = item_container.find(
        'div',
        class_=re.compile(r'\bUaQhfb\b')
    )

    address_candidate_elements = []

    if details_block:
        address_candidate_elements = details_block.find_all(
            'div', class_=re.compile(r'\bW4Efsd\b')
        )

    if not address_candidate_elements:
        address_candidate_elements = item_container.find_all(
            'div',
            class_=re.compile(r'\bW4Efsd\b')
        )
    
    for element in address_candidate_elements:

        line_parts=[]

        for child in element.children:
            if isinstance(child, Tag) and child.name == "span":
                text = child.get_text(strip=True)
                if text:
                    line_parts.append(text)
            elif isinstance(child, str):
                text = child.strip()
                if text == "." and line_parts:
                    pass
                elif text:
                    line_parts.append(text)
        if line_parts:
            current_line = " ".join(line_parts).strip()
            
            current_line_cleaned = re.sub(r'\s*\(\d{3,4}\)\s*[\d\s-]+\d\s*$', '', current_line).strip() # (021) 123-456
            current_line_cleaned = re.sub(r'\s*\d{8,}\s*$', '', current_line_cleaned).strip() # Standalone long numbers
            current_line_cleaned = re.sub(r'\s*(Buka|Tutup|Open|Closed).*$', '', current_line_cleaned, flags=re.IGNORECASE).strip() # Buka / Tutup
            
            if current_line_cleaned:
                full_address_lines.append(current_line_cleaned)

                if not street_detail_parts:
                    if "Jl." in current_line_cleaned or \
                       "Jalan" in current_line_cleaned or \
                       "RT." in current_line_cleaned.upper() or \
                       "RW." in current_line_cleaned.upper() or \
                       re.search(r'\b[A-Z0-9]{4}\+[A-Z0-9]{2,3}\b', current_line_cleaned): # Plus code

                        temp_street_detail = current_line_cleaned
                        if "Jl." in temp_street_detail:
                            temp_street_detail = temp_street_detail[temp_street_detail.find("JL."):]
                        elif "Jalan" in temp_street_detail:
                            temp_street_detail = temp_street_detail[temp_street_detail.find("Jalan"):]
                        elif "RT." in temp_street_detail.upper():
                            words = temp_street_detail.split()
                            for i, word in enumerate(words):
                                if word.upper() == "RT.":
                                    temp_street_detail = " ".join(words[i:])
                                    break
                        street_detail_parts.append(temp_street_detail.strip())

    final_street_detail = " ".join(street_detail_parts).strip()
    final_full_address = " | ".join(line for line in full_address_lines if line).strip()
    return final_street_detail if final_street_detail else "N/A", \
           final_full_address if final_full_address else "N/A"

def parse_place_from_html(
    html_content,
    province,
    kabupaten_kota,
    kecamatan,
    process_id="Parser"
    ):
    soup = BeautifulSoup(html_content, 'html.parser')
    scrapped_places = []

    feed_div = soup.find(
        'div',
        {
            'role': 'feed',
            'aria-label': True
        }
    )
    if not feed_div:
        feed_div = soup.find(
            'div', 
            {
                'role': 'feed',
            }
        )
    
    if not feed_div:
        print(f"[{process_id}] ERROR: Feed div not found in HTML. Cannot extract places for {kecamatan}.")
        return [] #

    place_item_containers = feed_div.find_all(
        'div',
        class_='Nv2PK', 
        recursive=True
    )

    if not place_item_containers:
        place_item_containers = feed_div.find_all(
            'div', 
            {
                'role': 'article'
            }, 
            recursive=True
        )

    
    if not place_item_containers:
        print(f"[{process_id}] WARNING: No place item containers found within the feed div for {kecamatan}. HTML might have changed or no results.")


    for item_container in place_item_containers:
        original_name = extract_name_from_container(item_container, process_id)

        if not original_name or original_name == "N/A":
            print(f"[{process_id}] Name not found or N/A for an item. Skipping. HTML snippet: {str(item_container)[:200]}")
            continue 

        lat, lon = extract_coordinates_from_container(item_container, process_id)
        street_detail, full_address_info = extract_address_details_from_container(item_container, process_id)

        name_with_street = original_name
        if street_detail and street_detail != "N/A":
            name_with_street = f"{original_name} - {street_detail}"

        place_data = {
            "Provinsi": province,
            "Kabupaten/Kota": kabupaten_kota,
            "Kecamatan": kecamatan,
            "Name with Street": name_with_street.strip(),
            "Original Name": original_name.strip(),
            "Street Detail": street_detail.strip(), # Already stripped in helper
            "Full Address Info": full_address_info.strip(), # Already stripped in helper
            "Latitude": lat,
            "Longitude": lon
        }
        scrapped_places.append(place_data)

    return scrapped_places


        
        
