from playwright.sync_api import sync_playwright
import os

def download_trimmed_data():
    project_folder = os.path.abspath(os.path.dirname(__file__))
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            url = "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release"
            print(f"Navigating to CPI release page...")
            page.goto(url, timeout=60000)
            
            print("Scrolling down to the Trimmed Mean section...")
            page.evaluate("window.scrollTo(0, 1400)")
            page.wait_for_timeout(1000)

            print("\n" + "="*50)
            print("BROWSER IS READY!")
            print("1. Locate the 'All groups CPI and Trimmed mean' chart/table.")
            print("2. Click the 'Table' tab.")
            print("3. Click 'Download' -> 'Download table as CSV'.")
            print("="*50 + "\n")

            with page.expect_download(timeout=120000) as download_info:
                print("Waiting for you to download the file...")
            
            download = download_info.value
            file_path = os.path.join(project_folder, "trimmed_data.csv")
            download.save_as(file_path)
            
            print(f"\n[SUCCESS] Trimmed mean file saved to: {file_path}")

        except Exception as e:
            print(f"\n[ERROR] Download failed: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    download_trimmed_data()