# DoorDash Bot

## ⚠️ DEPRECATED (2024)

**This project is DEPRECATED as of 2024. The DoorDash website has changed significantly, and this bot no longer works with the current site structure.**

This repository is kept for reference only. Below is the only video I have of it working:

<video src="Video.mp4" controls width="800">
  Your browser does not support the video tag. [Download the video](Video.mp4) instead.
</video>

---

A Python bot that scrapes menu items and modifiers from DoorDash and uploads them to Google Sheets.

## Setup

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser installed
- Google Sheets API credentials file (`ardent-anthem-450618-r9-92bc8c0d8ef9.json`)

### Installation

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets:**
   - Make sure you have the credentials JSON file (`ardent-anthem-450618-r9-92bc8c0d8ef9.json`) in the project root
   - Share your Google Sheet with the service account email: `myaccount@ardent-anthem-450618-r9.iam.gserviceaccount.com`
   - **Important:** If the sheet is in a shared drive, only share the specific sheet, not the entire drive

4. **Configure the script:**
   - Edit the variables at the top of `FinalDoordash.py`:
     - `menu_item_sheet`: Name of the menu items sheet tab
     - `modifiers_items_sheet`: Name of the modifiers options sheet tab
     - `filters_sheet`: Name of the filters sheet tab
     - `prefix`: Prefix for modifier keys (default: "SB_")

## Usage

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On Linux/Mac
   ```

2. **Run the script:**
   ```bash
   python FinalDoordash.py
   ```

3. **When prompted, enter the name of your Google Sheet**

## Notes

- The script uses cookies stored in `cookies.pkl` for authentication. If you need to re-authenticate, delete this file and the script will prompt you to log in.
- The script will automatically zoom out the browser window 6 times for better visibility.
- Make sure your Google Sheet has the following columns:
  - **Menu Items sheet:** Item, Price, Description, image_link, and Modifier Key columns (at least 20 recommended)
  - **Modifiers Options sheet:** Modifier Option, Price adjustment, Modifier Key, Modifier Type
  - **Filters sheet:** Modifier Keys

## Troubleshooting

- If you get authentication errors, verify the credentials JSON file is in the project root
- If the Google Sheet isn't found, make sure it's shared with the service account email
- If Chrome driver fails, make sure Google Chrome is installed and up to date

