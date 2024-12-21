from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import json

# Initialize WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

# Login to Amazon
def login_to_amazon(driver, email, password):
    driver.get("https://www.amazon.in")
    print("Trying logging in to Amazon for Email :", email)
    try:
        sign_in_button = driver.find_element(By.ID, "nav-link-accountList")
        sign_in_button.click()
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_input.send_keys(email)
        driver.find_element(By.ID, "continue").click()

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_input.send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()
        
        print("Logged in Successfully.")

    except TimeoutException:
        print("Login failed. Please check your credentials and try again.")
        driver.quit()
        exit()


def scrape_category(driver, category_url, max_pages=10):
    try:
        driver.get(category_url)
        category_name = driver.find_element(By.XPATH, "//div[@class='_cDEzb_card-title_2sYgw']//h1").text
        print(f"Scraping category: ",category_name)
        all_products_data = []  # List to store all product details

        # Navigate to the category page
        for page in range(max_pages):
            print(f"Scraping page {page + 1} of category: {category_name}")

            try:
                # Wait for the container to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.zg-grid-general-faceout"))
                )

                # Locate all product links within the container
                product_links = driver.find_elements(By.CSS_SELECTOR, "div.zg-grid-general-faceout a.a-link-normal.aok-block")

                # Iterate through each product link and extract data
                for i in range(1, 2, 2):        #len(product_links)+1 
                    link = product_links[i]
                    product_url = link.get_attribute("href")
                    product_name = product_url.split("/")[3]
                    # product_name = link.text
                    if product_url:  # Ensure the URL exists
                        print(f"Scraping product: {product_name}")
                        driver.execute_script("window.open(arguments[0], '_blank');", product_url)
                        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

                        try:
                            # Wait for the product page to load
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, "productTitle"))
                            )

                            condition = driver.find_element(By.XPATH, "//span[contains(@class, 'savingsPercentage')]").text if driver.find_elements(By.XPATH, "//span[contains(@class, 'savingsPercentage')]") else "0"
                            if(abs(int(condition.replace("%", ""))) <= 50):
                                continue

                            # Extract product details
                            product_data = {
                                'Product Name': driver.find_element(By.ID, "productTitle").text,
                                'Price': driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text if driver.find_elements(By.XPATH, "//span[@class='a-price-whole']") else "Not Available",
                                'Discount': condition,
                                'Best Seller Rating': driver.find_element(By.XPATH, "//span[@id='acrPopover']").get_attribute("title") if driver.find_elements(By.XPATH, "//span[@id='acrPopover']") else "Not Available",
                                'Ship From': driver.find_element(By.XPATH, "//div[@class='tabular-buybox-text' and (@tabular-attribute-name='Ships from'  or @tabular-attribute-name='Delivered by')]//span").text if driver.find_elements(By.XPATH, "//div[@class='tabular-buybox-text' and (@tabular-attribute-name='Ships from'  or @tabular-attribute-name='Delivered by')]//span") else "Not Available",
                                'Sold By': driver.find_element(By.XPATH, "//div[@class='tabular-buybox-text' and (@tabular-attribute-name='Sold by')]//span").text if driver.find_elements(By.XPATH, "//div[@class='tabular-buybox-text' and @tabular-attribute-name='Sold by']//span") else "Not Available",
                                'Product Description': driver.find_element(By.ID, "feature-bullets").text if driver.find_elements(By.ID, "feature-bullets") else "Not Available",
                                'Number Bought in Past Month': driver.find_element(By.XPATH, "//span[@id='social-proofing-faceout-title-tk_bought']").text if driver.find_elements(By.XPATH, "//span[@id='social-proofing-faceout-title-tk_bought']") else "Not Available",
                                'Category Name': driver.find_element(By.XPATH, "//option[@selected='selected']").text if driver.find_elements(By.XPATH, "//option[@selected='selected']") else "Not Available",
                                'Available Images': [img.get_attribute("src") for img in driver.find_elements(By.XPATH, "//ul[contains(@class, 'a-button-list')]//img")]
                            }

                            # Print and append the product data
                            all_products_data.append(product_data)

                        except Exception as e:
                            print(f"Error extracting product details: {e}")

                        finally:
                            # Close the product tab and switch back to the main tab
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error on page {page + 1}: {e}")

            # Navigate to the next page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "ul.a-pagination li.a-last a")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)  # Pause to allow the next page to load
            except Exception:
                print("No more pages available.")
                break

    except Exception as e:
        print(f"Error scraping category {category_url}: {e}")

    return all_products_data



# Save data to file
def save_data(data, file_name, file_type="json"):
    if file_type == "json":
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    elif file_type == "csv":
        keys = data[0].keys()
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

# Main function
def main():
    email = "your-email@example.com"  # Replace with your Amazon email
    password = "your-password"        # Replace with your Amazon password

    categories = [
        "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
        "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0",
        "https://www.amazon.in/gp/bestsellers/home-improvement/ref=zg_bs_home-improvement_sm",
        "https://www.amazon.in/gp/bestsellers/apparel/ref=zg_bs_apparel_sm",
        "https://www.amazon.in/gp/bestsellers/luggage/ref=zg_bs_luggage_sm",
        "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_beauty_sm",
        "https://www.amazon.in/gp/bestsellers/automotive/ref=zg_bs_automotive_sm",
        "https://www.amazon.in/gp/bestsellers/grocery/?ie=UTF8&ref_=sv_topnav_storetab_gourmet_1"
    ]

    driver = init_driver()
    login_to_amazon(driver, email, password)

    all_products = []
    for category_url in categories:
        driver.get(category_url)
        category_products = scrape_category(driver, category_url)
        all_products.extend(category_products)

    driver.quit()

    save_data(all_products, "amazon_best_sellers.json", file_type="json")
    print("Data saved successfully.")

if __name__ == "__main__":
    main()
