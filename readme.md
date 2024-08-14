# Real Estate Data Scraper

### Overview

This project contains a Python script that automates the process of downloading real estate tax data from a specific county tax website and extracting detailed property information from the target property appraiser website based on unpaid taxes. The script is divided into two main parts:

1. **Downloading the CSV file**: 
   - The script navigates to the real estate reports page on the county tax website, selects the desired report (unpaid taxes), filters by a specific tax year, and downloads the corresponding CSV file.
   - The CSV file is saved in a directory named `TD_files` within the current working directory.

2. **Extracting property data**:
   - The script reads the downloaded CSV file, drop unnecessary columns, iterates through the records, and for each property, it retrieves detailed information such as the owner’s name, property address, and additional property details from the target website.
   - The extracted information is then appended to the DataFrame and saved as a new CSV file named `unpaid_taxes.csv`.

### Dependencies

- **Python 3.x**
- **Selenium**
- **Pandas**
- **chromedriver_autoinstaller**

### Installation

1. **Install Python 3.x:** Ensure that Python 3.x is installed on your system.
2. **Install Required Libraries:** Run the following command to install the necessary Python libraries:
    ```bash
    pip install selenium pandas chromedriver-autoinstaller
    ```
3. **Clone the Repository:** Download or clone this repository to your local machine.

## Usage

1. **Set the Tax Year**:
   - Modify the `tax_year_input` variable at the beginning of the script to specify the desired tax year for which the CSV file should be downloaded.

2. **Run the Script**:
    ```bash
    python real_estate.py
    ```

3. **Output**:
   - The final output will be a CSV file containing the original data along with additional property details such as owner name, property address, year built, living area, etc.


## Customization

- **Target Year**: 
  - Change the `tax_year_input` variable to download data for different tax years.
  
- **Additional Data Fields**:
  - Modify the code to extract and include more data fields as needed.

## Notes

- Ensure that the website's structure or elements haven't changed. If the website updates, you might need to adjust the XPaths or CSS selectors used in the script.
- The script currently waits for 30 seconds before performing certain actions. This can be adjusted depending on your network speed and website response time.




### Disclaimer

"This script is provided for educational purposes only and Please note that the use of this code in real-world applications should be done with careful consideration. The author cannot be held responsible for any misuse, potential damages, or legal implications that may result from its use. It is advised to ensure that you have the appropriate permissions and that your use of this script is in full compliance with relevant laws and regulations."
