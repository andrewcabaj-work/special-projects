from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
from datetime import datetime
import argparse

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 8)

# --- ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description="Scrape EWG Talc product data.")
parser.add_argument("--start", type=int, required=True, help="Start page number")
parser.add_argument("--end", type=int, required=True, help="End page number")
args = parser.parse_args()

start_page = args.start
end_page = args.end

# --- CONFIG ---
downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
output_csv = os.path.join(downloads_path, f"ewg_product_data_p{start_page}_to_p{end_page}.csv")

# --- SCRAPE LOOP ---
results = []

for page_num in range(start_page, end_page + 1):
    print(f"\n🔎 Loading listing page {page_num}...")
    url = f"https://www.ewg.org/skindeep/browse/ingredients/706427-talc/?ingredient_id=706427-talc&page={page_num}&sort=score"
    driver.get(url)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-tile")))

        # 🔧 DEFINE `tiles` HERE
        tiles = driver.find_elements(By.CLASS_NAME, "product-tile")
        print(f"📦 Found {len(tiles)} product tiles.")

        for i in range(len(tiles)):
            try:
                # Re-fetch tiles to avoid stale references
                tiles = driver.find_elements(By.CLASS_NAME, "product-tile")
                links = tiles[i].find_elements(By.TAG_NAME, "a")
                product_url = links[-1].get_attribute("href")
                print(f"  → [{i+1}] {product_url}")

                # Set a per-page timeout and load product page
                try:
                    driver.set_page_load_timeout(20)  # 20 seconds max
                    driver.get(product_url)
                except Exception as e:
                    print(f"❌ Timed out loading product page: {product_url} — {e}")
                    continue


                # === Your scraping logic here ===
                name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-name"))).text.strip()

                try:
                    img_tag = driver.find_element(By.CSS_SELECTOR, "div.product-image img")
                    image_url = img_tag.get_attribute("src")
                except:
                    image_url = ""

                talc_score = ""
                try:
                    rows = driver.find_elements(By.CLASS_NAME, "ingredient-overview-tr")
                    for row in rows:
                        try:
                            ing_name = row.find_element(By.CLASS_NAME, "td-ingredient-interior").text.strip().upper()
                            if ing_name == "TALC":
                                img = row.find_element(By.CLASS_NAME, "score-popup")
                                talc_score = img.get_attribute("alt")
                                break
                        except:
                            continue
                except:
                    pass
                
                try:
                    brand = driver.find_element(By.CSS_SELECTOR, ".product-lower p.title:nth-of-type(2) + a").text.strip()
                except:
                    brand = ""

                try:
                    category = ""
                    titles = driver.find_elements(By.CSS_SELECTOR, ".product-lower p.title")
                    for t in titles:
                        if t.text.strip().upper() == "CATEGORY":
                            siblings = t.find_elements(By.XPATH, "./following-sibling::a[div]")
                            category = "; ".join([s.find_element(By.TAG_NAME, "div").text.strip() for s in siblings])
                            break
                except Exception as e:
                    print(f"⚠️ Category scrape error on {product_url}: {e}")
                    category = ""

                try:
                    updated_date = driver.find_element(By.CSS_SELECTOR, "div.data-updated p:nth-of-type(2)").text.strip()
                except:
                    updated_date = ""

                try:
                    label_tab = driver.find_element(By.ID, "nav-label-info")
                    if "active" not in label_tab.get_attribute("class"):
                        label_tab.click()
                        time.sleep(0.5)  # Wait briefly for transition
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#label-information p")))
                    ingredients = driver.find_element(By.CSS_SELECTOR, "#label-information p").text.strip()
                except:
                    ingredients = ""

                results.append({
                    "Product_Name": name,
                    "URL": product_url,
                    "Talc_Score": talc_score,
                    "Ingredients": ingredients,
                    "Brand": brand,
                    "Category": category,
                    "Date_Updated": updated_date,
                    "Image_URL": image_url
                })

                # Go back to product list page
                driver.back()
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-tile")))
                time.sleep(1)

            except Exception as e:
                print(f"Error scraping tile {i+1} on page {page_num}: {e}")
    
    except Exception as e:
        print(f"Failed to load page {page_num}: {e}")

# --- WRITE RESULTS ---
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Product_Name","Brand","Category","Talc_Score","Ingredients","Date_Updated","URL","Image_URL",])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Done. Scraped {len(results)} products from pages {start_page}–{end_page}.")