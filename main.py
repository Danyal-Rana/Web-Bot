import random
import time
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from stem import Signal
from stem.control import Controller

TOR_ENABLED = False  # Set True to use Tor
PROXIES = [
    # Add your proxies or load from API
    # "http://username:password@proxy1.com:port"
]

def rotate_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_tor_password')  # Set in torrc
        controller.signal(Signal.NEWNYM)
        print("[Tor] New identity requested.")

def get_random_user_agent():
    return UserAgent().random

def get_random_screen_size():
    sizes = [(1920,1080), (1366,768), (1440,900), (1536,864), (1280,800)]
    return random.choice(sizes)

def get_article_links(blog_url):
    headers = {'User-Agent': get_random_user_agent()}
    response = requests.get(blog_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('article') or soup.find('div', class_='blog-content')
    links = [a['href'] for a in content.find_all('a', href=True)] if content else []
    return links

def simulate_scrolling(driver):
    for _ in range(random.randint(3, 7)):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(random.uniform(0.5, 1.5))

def visit_link(link, referer=None):
    user_agent = get_random_user_agent()
    width, height = get_random_screen_size()
    proxy = random.choice(PROXIES) if PROXIES else None

    options = uc.ChromeOptions()
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument(f'--window-size={width},{height}')
    options.add_argument(f'--lang={random.choice(["en-US", "fr-FR", "de-DE"])}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    if referer:
        options.add_argument(f'--referer={referer}')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = uc.Chrome(options=options)

    try:
        print(f"[+] Visiting: {link} with UA: {user_agent}")
        driver.get(link)
        simulate_scrolling(driver)

        # Example: inject cookie/localStorage
        driver.execute_script("localStorage.setItem('visitor_id', '" + str(random.randint(1000,9999)) + "');")

        time.sleep(random.randint(6, 12))
    except Exception as e:
        print(f"[!] Error visiting {link}: {e}")
    finally:
        driver.quit()

def main(blog_url):
    if TOR_ENABLED:
        rotate_tor_ip()

    links = get_article_links(blog_url)
    print(f"[+] Found {len(links)} links.")

    for link in links:
        visit_link(link, referer=blog_url)
        time.sleep(random.uniform(4, 8))

if __name__ == "__main__":
    blog_url = input("Enter blog article URL: ")
    main(blog_url)