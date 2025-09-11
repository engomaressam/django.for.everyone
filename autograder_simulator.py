#!/usr/bin/env python3
"""
Autograder Simulator for Django Ads App
Simulates the autograder behavior to debug the unfavorite link issue
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

class AutograderSimulator:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AutograderSimulator/1.0'
        })
    
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")
    
    def get_csrf_token(self, soup):
        """Extract CSRF token from form"""
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        return csrf_input['value'] if csrf_input else None
    
    def login(self, username, password):
        """Login to the application"""
        self.log(f"Attempting to login as {username}")
        
        # Get login page
        login_url = f"{self.base_url}/accounts/login/"
        response = self.session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find login form
        form = soup.find('form')
        if not form:
            self.log("ERROR: No login form found", "ERROR")
            return False
        
        csrf_token = self.get_csrf_token(soup)
        if not csrf_token:
            self.log("ERROR: No CSRF token found", "ERROR")
            return False
        
        # Submit login form
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = self.session.post(login_url, data=login_data, allow_redirects=True)
        
        # Debug authentication status
        self.log(f"Login response status: {response.status_code}")
        self.log(f"Final URL after login: {response.url}")
        
        if "Your username and password didn't match" in response.text:
            self.log("ERROR: Login failed", "ERROR")
            return False
        
        # Check if we're actually logged in by looking for logout link
        soup = BeautifulSoup(response.text, 'html.parser')
        logout_link = soup.find('a', href=re.compile(r'.*logout.*'))
        
        if logout_link:
            self.log("Login successful - found logout link")
            return True
        else:
            self.log("WARNING: Login may have failed - no logout link found")
            # Save login response for debugging
            with open('login_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            return False
    
    def get_ads_list(self):
        """Get the ads list page"""
        ads_url = f"{self.base_url}/ads/"
        response = self.session.get(ads_url)
        self.log(f"Retrieved ads list: {len(response.text)} characters")
        return BeautifulSoup(response.text, 'html.parser')
    
    def analyze_favorite_links(self, soup):
        """Analyze favorite/unfavorite links in the page"""
        self.log("=== ANALYZING FAVORITE LINKS ===")
        
        # Find all links containing 'favorite' or 'unfavorite'
        favorite_links = soup.find_all('a', href=re.compile(r'.*(favorite|unfavorite).*'))
        
        self.log(f"Found {len(favorite_links)} favorite-related links:")
        
        for i, link in enumerate(favorite_links, 1):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            self.log(f"  {i}. Text: '{text}' | Href: '{href}'")
        
        return favorite_links
    
    def favorite_ad(self, ad_id):
        """Favorite a specific ad"""
        favorite_url = f"{self.base_url}/ads/ad/{ad_id}/favorite"
        self.log(f"Attempting to favorite ad {ad_id}")
        
        response = self.session.get(favorite_url)
        self.log(f"Favorite response status: {response.status_code}")
        
        return response.status_code == 200 or response.status_code == 302
    
    def find_ads_with_ids(self, soup):
        """Find all ads and their IDs from the page"""
        ads = []
        
        # Look for links to ad detail pages
        ad_links = soup.find_all('a', href=re.compile(r'/ads/ad/\d+$'))
        
        for link in ad_links:
            href = link.get('href', '')
            match = re.search(r'/ads/ad/(\d+)$', href)
            if match:
                ad_id = match.group(1)
                title = link.get_text(strip=True)
                ads.append({
                    'id': ad_id,
                    'title': title,
                    'link': href
                })
        
        self.log(f"Found {len(ads)} ads on the page:")
        for ad in ads:
            self.log(f"  ID: {ad['id']} | Title: '{ad['title']}'")
        
        return ads
    
    def simulate_autograder_flow(self):
        """Simulate the complete autograder flow"""
        self.log("=== STARTING AUTOGRADER SIMULATION ===")
        
        # Step 1: Login
        if not self.login('dj4e_user1', 'Meow_f53aa7_41'):
            return False
        
        # Step 2: Get initial ads list
        soup = self.get_ads_list()
        
        # Step 3: Find ads
        ads = self.find_ads_with_ids(soup)
        if not ads:
            self.log("ERROR: No ads found", "ERROR")
            return False
        
        # Step 4: Analyze current favorite links
        self.analyze_favorite_links(soup)
        
        # Step 5: Try to favorite the first ad
        first_ad = ads[0]
        self.log(f"\n=== TESTING FAVORITE/UNFAVORITE CYCLE ===")
        self.log(f"Testing with ad {first_ad['id']}: '{first_ad['title']}'")
        
        if not self.favorite_ad(first_ad['id']):
            self.log("ERROR: Failed to favorite ad", "ERROR")
            return False
        
        # Step 6: Get updated ads list and check for unfavorite link
        self.log("Getting updated ads list after favoriting...")
        soup = self.get_ads_list()
        
        # Step 7: Analyze favorite links after favoriting
        favorite_links = self.analyze_favorite_links(soup)
        
        # Step 8: Look specifically for unfavorite link for this ad
        unfavorite_pattern = f"/ads/ad/{first_ad['id']}/unfavorite"
        unfavorite_links = [link for link in favorite_links 
                          if unfavorite_pattern in link.get('href', '')]
        
        self.log(f"\n=== UNFAVORITE LINK CHECK ===")
        self.log(f"Looking for unfavorite link pattern: {unfavorite_pattern}")
        self.log(f"Found {len(unfavorite_links)} matching unfavorite links:")
        
        for link in unfavorite_links:
            text = link.get_text(strip=True)
            href = link.get('href', '')
            self.log(f"  Found: Text='{text}' Href='{href}'")
        
        # Step 9: Save HTML for inspection
        with open('ads_page_after_favorite.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        self.log("Saved ads page HTML to 'ads_page_after_favorite.html' for inspection")
        
        if unfavorite_links:
            self.log("SUCCESS: Unfavorite link found!", "SUCCESS")
            return True
        else:
            self.log("ERROR: No unfavorite link found - this matches autograder failure", "ERROR")
            
            # Debug: Show the entire <li> element for the favorited ad
            self.debug_ad_element(soup, first_ad['id'])
            return False
    
    def debug_ad_element(self, soup, ad_id):
        """Debug the specific ad element to see what's wrong"""
        self.log(f"\n=== DEBUGGING AD {ad_id} ELEMENT ===")
        
        # Find the ad link
        ad_link = soup.find('a', href=f"/ads/ad/{ad_id}")
        if ad_link:
            # Find the parent <li> element
            li_element = ad_link.find_parent('li')
            if li_element:
                self.log("Complete <li> element for this ad:")
                self.log(li_element.prettify())
            else:
                self.log("Could not find parent <li> element")
        else:
            self.log(f"Could not find ad link for ad {ad_id}")

def main():
    base_url = "https://engomaressam.pythonanywhere.com"
    simulator = AutograderSimulator(base_url)
    
    try:
        success = simulator.simulate_autograder_flow()
        if success:
            print("\n✅ SIMULATION PASSED - Unfavorite link found!")
        else:
            print("\n❌ SIMULATION FAILED - Unfavorite link not found!")
    except Exception as e:
        print(f"\nERROR: Simulation failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
