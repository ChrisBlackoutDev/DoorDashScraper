#  _____                      _           _        _____                                
# |  __ \                    | |         | |      / ____|                               
# | |  | | ___   ___  _ __ __| | __ _ ___| |__   | (___   ___ _ __ __ _ _ __   ___ _ __ 
# | |  | |/ _ \ / _ \| '__/ _` |/ _` / __| '_ \   \___ \ / __| '__/ _` | '_ \ / _ \ '__|
# | |__| | (_) | (_) | | | (_| | (_| \__ \ | | |  ____) | (__| | | (_| | |_) |  __/ |   
# |_____/ \___/ \___/|_|  \__,_|\__,_|___/_| |_| |_____/ \___|_|  \__,_| .__/ \___|_|   
#                                                                      | |              
#                                                                      |_|              

########################### CHANGE TAB NAMES AND VARIABLES HERE ###########################

prefix = "SB_"

###########################################################################################


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import os
import sys
import pyautogui
import sqlite3

ascii_art = r"""
     _____                      _           _        _____                                
    |  __ \                    | |         | |      / ____|                               
    | |  | | ___   ___  _ __ __| | __ _ ___| |__   | (___   ___ _ __ __ _ _ __   ___ _ __ 
    | |  | |/ _ \ / _ \| '__/ _` |/ _` / __| '_ \   \___ \ / __| '__/ _` | '_ \ / _ \ '__|
    | |__| | (_) | (_) | | | (_| | (_| \__ \ | | |  ____) | (__| | | (_| | |_) |  __/ |   
    |_____/ \___/ \___/|_|  \__,_|\__,_|___/_| |_| |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                         | |              
                                                                         |_|              
"""

print(ascii_art)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths
DB_PATH = os.path.join(script_dir, "menu_data.db")
COOKIES_PATH = os.path.join(script_dir, "cookies.pkl")
LOGIN_URL = "https://www.doordash.com"
TARGET_URL = "https://www.doordash.com/store/starbucks-allen-altos-24585333/"

# Initialize SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_items (
    Item TEXT UNIQUE,
    Price TEXT,
    Description TEXT,
    image_link TEXT,
    "Modifier Key 1" TEXT, "Modifier Key 2" TEXT, "Modifier Key 3" TEXT, "Modifier Key 4" TEXT, "Modifier Key 5" TEXT,
    "Modifier Key 6" TEXT, "Modifier Key 7" TEXT, "Modifier Key 8" TEXT, "Modifier Key 9" TEXT, "Modifier Key 10" TEXT,
    "Modifier Key 11" TEXT, "Modifier Key 12" TEXT, "Modifier Key 13" TEXT, "Modifier Key 14" TEXT, "Modifier Key 15" TEXT,
    "Modifier Key 16" TEXT, "Modifier Key 17" TEXT, "Modifier Key 18" TEXT, "Modifier Key 19" TEXT, "Modifier Key 20" TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS modifiers_options (
    "Modifier Option" TEXT UNIQUE,
    "Price adjustment" TEXT,
    "Modifier Key" TEXT,
    "Modifier Type" TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS filters (
    "Modifier Keys" TEXT UNIQUE
)
''')

conn.commit()

# Launch undetected Chrome driver with a static user-agent
options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
driver = uc.Chrome(options=options)

# Open Doordash login page first
driver.get(LOGIN_URL)
time.sleep(3)  # Wait for the page to load

# Load cookies if the file exists; otherwise, prompt for manual login and save cookies
if os.path.exists(COOKIES_PATH):
    with open(COOKIES_PATH, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            # Ensure the cookie domain matches Doordash
            if "doordash" in cookie["domain"]:
                driver.add_cookie(cookie)
    print("Cookies loaded successfully!")
else:
    input("Please sign in manually in the browser window that opened, then press Enter to continue...")
    confirmation = input("Are you signed in? Type 'yes' to save cookies and proceed: ").strip().lower()
    if confirmation == 'yes':
        with open(COOKIES_PATH, "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("Cookies saved successfully!")
    else:
        print("Login not confirmed. Exiting.")
        driver.quit()
        conn.close()
        sys.exit(1)

# Refresh to apply cookies
driver.refresh()
time.sleep(5)  # Allow session to load

# Verify if login was successful
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
    print("Not logged in! You may need to re-save cookies.")
except:
    print("Login successful! Proceeding to target page...")


# Zoom out 3 times
for _ in range(6):
    pyautogui.hotkey('ctrl', '-')  # Simulate "CTRL + -"
    time.sleep(0.1)  # Short delay for keypress to register


# Now, navigate to the target page
driver.get(TARGET_URL)
time.sleep(5)  # Allow for edits

wait = WebDriverWait(driver, 4)
divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'eexYYc')]")))

header_text = []

for div in divs:
    try:
        h2_element = div.find_element(By.XPATH, ".//h2")
        header_text.append(h2_element.text)
    except Exception as e:
        print(f"Error finding h2 element: {e}")

if "Most Ordered" in header_text:
    header_text.remove("Most Ordered")

master_data = []
aggregate_master_data = []

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def process_spans(spans_list):
    result_list = []  # List to store prices
    modifiers = []  # List to store removed coffee names
    i = 0
    while i < len(spans_list):
        if '$' not in spans_list[i]:  # This is a coffee name (no '$' in it)
            modifiers.append(spans_list[i])  # Add the coffee name to the modifiers list
            # Check if it's followed by another coffee name or a price
            if i + 1 < len(spans_list) and '$' not in spans_list[i + 1]:  # Followed by another coffee name
                result_list.append('+0.00')  # Default price
        elif '$' in spans_list[i]:  # This is a price
            result_list.append(spans_list[i].replace('$', ''))  # Add the price to the result list without the '$' sign
        i += 1  # Move to the next element

    # Ensure every modifier has a price
    while len(result_list) < len(modifiers):
        result_list.append('+0.00')

    return result_list, modifiers




def print_header_and_span_contents(driver):
    wait = WebDriverWait(driver, 10)

    master_data = {}  # Stores all collected data with unique headers
    processed_headers = set()  # Stores headers already processed from dpngOO divs
    image_src = None  # Store image link separately

    def process_divs(divs, header_storage):
        """Extracts information from div elements and updates header storage."""
        header_dict = {}

        for div in divs:
            try:
                header_hBnZXN = div.find_element(By.CLASS_NAME, "hBnZXN")
                modifier_name = header_hBnZXN.text.strip()

                # If this modifier was already processed, skip it
                if modifier_name in header_storage:
                    print(f"Skipping duplicate modifier: {modifier_name}")
                    continue

                print(f"Processing modifier: {modifier_name}")
                header_storage.add(modifier_name)  # Mark as processed
                spans_list = []  
                
                # Find relevant span elements
                znlaC_spans = div.find_elements(By.CLASS_NAME, "ZNLaC")
                dcneXH_spans = div.find_elements(By.CLASS_NAME, "dCneXH")

                # Check for "(Optional)" in dCneXH spans
                optionality = any("(Optional)" in span.text for span in dcneXH_spans)

                # Filter out dCneXH spans without "$" symbol
                dcneXH_spans_with_price = [span for span in dcneXH_spans if "$" in span.text]

                # Combine the ZNLaC spans and filtered dCneXH spans
                all_spans = znlaC_spans + dcneXH_spans_with_price

                # Sort spans by vertical position
                all_spans_sorted = sorted(all_spans, key=lambda span: span.location['y'])

                # Extract text
                for span in all_spans_sorted:
                    spans_list.append(span.text.strip())

                # Process span list into final format
                final_spans, modifiers_list = process_spans(spans_list)

                # Store data with Optionality flag
                header_dict[modifier_name] = {
                    'prices': final_spans,
                    'modifiers': modifiers_list,
                    'Optionality': "true" if optionality else "false"
                }

            except Exception as e:
                print(f"Error processing div: {e}")

        return header_dict

    # **Extract Image Link (Only Once Per Product)**
    try:
        image_element = driver.find_element(By.CLASS_NAME, "hpTRGL")  # Find the <img> directly
        image_src = image_element.get_attribute("src")  # Extract src attribute
        print(f"✅ Found product image: {image_src}")
    except Exception as e:
        print(f"⚠️ No image found for this product: {e}")

    # **First Pass - Process `dpngOO` divs**
    try:
        dpngOO_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "dpngOO")))
        dpngOO_data = process_divs(dpngOO_divs, processed_headers)
    except Exception as e:
        print("No dpngOO divs found")
        dpngOO_data = {}

    try:
        # Extract `dtvoNG` header text (Product Name)
        dtvoNG_headers = driver.find_elements(By.CLASS_NAME, "dtvoNG")
        product_name = dtvoNG_headers[0].find_element(By.TAG_NAME, "span").text.strip() if dtvoNG_headers else ""

        # If this product already exists, update its dictionary instead of adding a new one
        if product_name in master_data:
            master_data[product_name].update(dpngOO_data)
        else:
            master_data[product_name] = dpngOO_data

    except Exception as e:
        print(f"Error finding 'dtvoNG' header: {e}")

    # **Extract Product Description (Only Once)**
    try:
        description_element = driver.find_element(By.XPATH, "//span[@data-testid='nestedItemHeader_subtitle']")
        product_description = description_element.text.strip()
        print(f"Product Description: {product_description}")

        master_data["description"] = product_description  # Add description to master_data

    except Exception as e:
        print(f"Error finding product description: {e}")

    # **Check and Click Radio Button (If Exists)**
    radio_button_found = False  # Flag to track if a radio button is found
    try:
        radio_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio']"))
        )
        radio_button.click()
        print("✅ First available radio button clicked successfully!")
        radio_button_found = True  # Mark as found

    except Exception:
        print("⚠️ No radio button found, skipping second pass of div scanning....")

    # **Skip second pass if no radio button found**
    if radio_button_found:
        try:
            iJNVQM_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "iJNVQM")))
            iJNVQM_data = process_divs(iJNVQM_divs, processed_headers)

            # Instead of adding a duplicate entry, merge with the existing one
            if product_name in master_data:
                master_data[product_name].update(iJNVQM_data)
            else:
                master_data[product_name] = iJNVQM_data

        except Exception as e:
            print(f"Error processing 'iJNVQM' divs: {e}")

    # **Extract Product Price (Only Once)**
    try:
        add_to_cart_span = driver.find_element(By.XPATH, "//span[contains(text(), 'Add to cart') or contains(text(), 'Make 1 required selection')]")
        product_price = add_to_cart_span.text.split('$')[-1]  

        print(f"Product Price: {product_price}")

        master_data["product_price"] = product_price  # Add product price to master_data

    except Exception as e:
        print(f"Error finding product price: {e}")

    # **Reorder Dictionary - Move image_link to End**
    if product_name in master_data:
        master_data[product_name]["description"] = master_data.pop("description", "")
        master_data[product_name]["product_price"] = master_data.pop("product_price", "")
        if image_src:
            master_data[product_name]["image_link"] = image_src  # Add image link last

    # **Final Output**
    print(master_data)

    # Append to aggregate_master_data list
    aggregate_master_data.append(master_data)
    print("✅ Added to aggregate_master_data!")


def save_menu_items():
    """Saves the latest product data from aggregate_master_data to the database.
       If the menu item already exists, it prints a message and skips updating.
    """
    
    if not aggregate_master_data:
        print("⚠️ No data available to upload.")
        return
    
    latest_data = aggregate_master_data[-1]  # Get the most recent scraped entry

    # Extract product name (first key in the dictionary)
    product_name = next(iter(latest_data.keys()))

    # Extract nested data (description, price, image link)
    product_info = latest_data.get(product_name, {})  # Get the product dictionary
    product_price = product_info.get("product_price", "N/A")
    product_description = product_info.get("description", "No description available")
    product_image_link = product_info.get("image_link", "")

    # Check if the item is already in the table
    cursor.execute("SELECT Item FROM menu_items WHERE Item = ?", (product_name,))
    if cursor.fetchone():
        print(f"✅ '{product_name}' is already in the database. Skipping update.")
        return

    # Insert the new item
    cursor.execute('''
    INSERT INTO menu_items (Item, Price, Description, image_link)
    VALUES (?, ?, ?, ?)
    ''', (product_name, product_price, product_description, product_image_link))
    conn.commit()

    print(f"✅ Added '{product_name}' to menu_items table.")


#def save_menu_items_modifiers():
    """Saves the latest product's modifier categories to the database
       under existing 'Modifier Key' columns.
    """

    if not aggregate_master_data:
        print("⚠️ No data available in aggregate_master_data.")
        return
    
    latest_data = aggregate_master_data[-1]  # Get the most recent scraped entry

    # Extract the product name (first key in latest_data)
    product_name = next(iter(latest_data.keys()))

    # Extract modifier categories (keys of the modifiers dictionary)
    product_info = latest_data.get(product_name, {})  # Get the product dictionary
    
    modifier_categories = [
        f"{prefix}{modifier_name}" if not modifier_name.startswith(prefix) else modifier_name 
        for modifier_name in product_info.keys()
        if isinstance(product_info[modifier_name], dict) and 'modifiers' in product_info[modifier_name]
    ]

    # Find the row for the product
    cursor.execute("SELECT rowid FROM menu_items WHERE Item = ?", (product_name,))
    row = cursor.fetchone()
    if not row:
        print("⚠️ No matching item found in database.")
        return
    row_id = row[0]

    # Prepare update query for up to 20 modifier keys
    update_query = "UPDATE menu_items SET "
    params = []
    for i, cat in enumerate(modifier_categories[:20], 1):
        update_query += f'"Modifier Key {i}" = ?, '
        params.append(cat)
    if params:
        update_query = update_query.rstrip(', ') + " WHERE rowid = ?"
        params.append(row_id)
        cursor.execute(update_query, params)
        conn.commit()
        print(f"✅ Updated {len(params)-1} modifier categories for '{product_name}'.")
    else:
        print("✅ No modifiers to update.")





def save_modifiers():
    """Updates database with unique modifier keys prefixed."""
    
    # Collect unique modifiers from the latest iteration of aggregate_master_data
    new_modifiers = set()
    
    if not aggregate_master_data:
        print("⚠️ No data available in aggregate_master_data.")
        return
    
    latest_data = aggregate_master_data[-1]  # Get the most recent scraped data

    for item, details in latest_data.items():
        if isinstance(details, dict):  # Ensure it's a dictionary (i.e., a menu item)
            for modifier_name, modifier_details in details.items():
                if isinstance(modifier_details, dict) and 'modifiers' in modifier_details:
                    sb_modifier = f"{prefix}{modifier_name}"  # Use the prefix variable
                    new_modifiers.add(sb_modifier)


    # Get existing modifiers
    cursor.execute('SELECT "Modifier Keys" FROM filters')
    existing_modifiers = set(row[0] for row in cursor.fetchall())

    # Find modifiers that are not yet in the table
    modifiers_to_add = new_modifiers - existing_modifiers

    if modifiers_to_add:
        
        # Insert new modifiers
        for mod in sorted(modifiers_to_add):
            cursor.execute('INSERT INTO filters ("Modifier Keys") VALUES (?)', (mod,))
        conn.commit()

        print(f"✅ Added {len(modifiers_to_add)} new modifiers to filters table.")
    else:
        print("✅ No new modifiers to add.")






def save_modifier_options():
    """Adds unique modifier options, their price adjustments, modifier types, and optionality to modifiers_options table.
       Ensures no duplicates are added.
    """

    if not aggregate_master_data:
        print("⚠️ No data available in aggregate_master_data.")
        return

    latest_data = aggregate_master_data[-1]  # Get the most recent scraped entry

    # Extract modifiers, prices, categories, and optionality
    modifiers_data = []

    for product_name, product_info in latest_data.items():
        if isinstance(product_info, dict):
            for category, details in product_info.items():
                if isinstance(details, dict) and "modifiers" in details and "prices" in details:
                    optionality = details.get("Optionality", "false")  # Get optionality status (default to "false")
                    modifier_type = "Addition" if optionality.lower() == "true" else "Option"  # Set Modifier Type
                    for modifier, price in zip(details["modifiers"], details["prices"]):
                        modifiers_data.append([modifier, price, f"{prefix}{category}", modifier_type])  # Use prefix variable

    if not modifiers_data:
        print("⚠️ No modifiers found in the latest data.")
        return

    # Get all existing modifiers to prevent duplicates
    cursor.execute('SELECT "Modifier Option" FROM modifiers_options')
    existing_modifiers = set(row[0] for row in cursor.fetchall())

    # Prepare new entries, skipping duplicates
    new_entries = [
        entry
        for entry in modifiers_data
        if entry[0] not in existing_modifiers
    ]

    if not new_entries:
        print("✅ No new modifiers to add.")
        return

    # Insert new entries
    for entry in new_entries:
        cursor.execute('''
        INSERT INTO modifiers_options ("Modifier Option", "Price adjustment", "Modifier Key", "Modifier Type")
        VALUES (?, ?, ?, ?)
        ''', (entry[0], entry[1], entry[2], entry[3]))
    conn.commit()

    print(f"✅ Added {len(new_entries)} new modifiers to modifiers_options table.")

print(header_text)
#header_text = ['Bottled Beverages']

for text in header_text:
    try:
        print(f"Processing text: {text}")  # Debugging print
        
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[contains(@class, 'iaJjPj') and @aria-label='{text}']")))
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)  # Allow modal to open

        div = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class, 'eexYYc') and .//h2[text()='{text}']]")))

        buttons = div.find_elements(By.XPATH, ".//div[contains(@class, 'jXhKue') and @role='button']")
        print(f"Found {len(buttons)} buttons under {text}")

        for btn in buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(5)

                # Try to extract the headers & spans
                print_header_and_span_contents(driver)
                save_menu_items()  # Save data to database
                save_modifiers()
                #save_menu_items_modifiers()
                save_modifier_options()

            except Exception as inner_exception:
                print(f"❌ Error in print_header_and_span_contents for '{text}': {inner_exception}")

            # Click exit button
            try:
                svg_button = wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(@class, 'cvFqUQ') and not(@aria-label='Search stores, dishes, products')]"
                )))
                driver.execute_script("arguments[0].click();", svg_button)
                time.sleep(3)  # Small delay after closing

            except Exception as e:
                print(f"⚠️ Error clicking the exit button after processing '{text}': {e}")
            
        print("\n" + "-"*50 + "\n")  # Separator for readability

    except Exception as e:
        print(f"❌ Error processing text '{text}': {e}")

        # Click the exit button if it exists
        try:
            svg_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button//*[name()='svg']//*[local-name()='path' and contains(@d, 'M17.2929')]/ancestor::button")
            ))
            driver.execute_script("arguments[0].click();", svg_button)
            time.sleep(3)

        except Exception as exit_error:
            print(f"⚠️ Error clicking exit button while handling error for '{text}': {exit_error}")

        continue  # Skip to the next item

driver.quit()
conn.close()