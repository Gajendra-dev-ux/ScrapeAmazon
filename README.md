# Amazon Best Sellers Scraper

This script is designed to scrape product information from the best sellers' pages of various categories on Amazon India. It uses **Selenium** to automate the browser for web scraping.

---

## Features

- **Automated Login**: Logs into Amazon using provided credentials.
- **Category Scraping**: Scrapes product data from multiple categories.
- **Pagination Support**: Handles multiple pages of product listings.
- **Detailed Product Information**: Extracts:
  - Product Name
  - Price
  - Discount
  - Best Seller Rating
  - Ship From and Sold By details
  - Product Description
  - Number Bought in Past Month
  - Category Name
  - Available Images
- **Data Export**: Saves the scraped data in JSON or CSV format.

---

## Prerequisites

1. **Python**: Ensure Python 3.7+ is installed.
2. **Google Chrome**: Install the latest version of Google Chrome.
3. **ChromeDriver**: Download the ChromeDriver compatible with your Chrome version.
   - [Download ChromeDriver](https://chromedriver.chromium.org/downloads)
4. **Selenium**: Install the Selenium library using pip:
   ```bash
   pip install selenium

---

## Setup Instructions

1. Clone or download the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install selenium
3. Place the ChromeDriver executable in a directory included in your system's PATH or in the same folder as the script.
4. Update the script with your Amazon login credentials
   ```python
   email = "your-email@example.com"  # Replace with your Amazon email
   password = "your-password"        # Replace with your Amazon password
5. Optionally, modify the list of categories in the categories variable to include/exclude URLs of Amazon best sellers' pages.

---

## Usage

1. Run the script:
   ```bash
   python amazon_scraper.py
2. The script will:
   - Log in to Amazon using the provided credentials.
   - Scrape data from the specified categories.
   - Save the results to a JSON/CSV file (amazon_best_sellers.json).

---

## OUTPUT

- FORMAT:
  ```json
  [
      {
          "Product Name": "Sample Product",
          "Price": "1,999",
          "Discount": "20%",
          "Best Seller Rating": "4.5 out of 5 stars",
          "Ship From": "Amazon Warehouse",
          "Sold By": "Amazon Seller",
          "Product Description": "Detailed description of the product.",
          "Number Bought in Past Month": "120",
          "Category Name": "Electronics",
          "Available Images": [
              "image1.jpg",
              "image2.jpg"
          ]
      },
      ...
  ]

---

## Notes
- **Headless Mode**: To run the script without opening the browser window, uncomment the following line in init_driver:
  ```python
  options.add_argument("--headless")
- **Error Handling**: The script handles common exceptions like timeouts and missing elements but may need further adjustments for unexpected scenarios.
- **Amazon Account**: Ensure your Amazon account is active and does not require additional verification.

---

## Limitations
- **IP Blocking**: Frequent scraping might result in temporary IP blocks by Amazon. Use delays or proxies to avoid this.
- **Dynamic Changes**: Amazon's website structure might change, requiring updates to the script.
