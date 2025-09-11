#!/usr/bin/env python3
"""
Link Test Script - Tests favorite/unfavorite links on PythonAnywhere site
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
import json

BASE_URL = "https://engomaressam.pythonanywhere.com"
LOGIN_URL = f"{BASE_URL}/accounts/login/"
ADS_URL = f"{BASE_URL}/ads/"

USERNAME = "dj4e_user1"
PASSWORD = "Meow_f53aa7_41"

def debug_print(message):
    """Print debug message"""
    print(f"[DEBUG] {message}")

def get_csrf_token(html_content):
    """Extract CSRF token from form"""
    soup = BeautifulSoup(html_content, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        return csrf_input['value']
    return None

def login(session):
    """Login to the application"""
    debug_print(f"Attempting to login as {USERNAME}")
    
    # Get login page
    response = session.get(LOGIN_URL)
    csrf_token = get_csrf_token(response.text)
    
    if not csrf_token:
        debug_print("Error: No CSRF token found")
        return False
    
    # Submit login form
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
    debug_print(f"Login response status: {response.status_code}")
    
    # Check if login was successful by looking for logout link
    soup = BeautifulSoup(response.text, 'html.parser')
    logout_link = soup.find('a', string='Logout')
    
    if logout_link:
        debug_print("Login successful - found 'Logout' link")
        return True
    else:
        debug_print("Login failed - no 'Logout' link found")
        
        # Save login response HTML for inspection
        with open("login_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        return False

def get_ad_list(session):
    """Get the ad list page and extract ad IDs"""
    debug_print("Fetching ad list page")
    response = session.get(ADS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all ad links
    ad_links = soup.find_all('a', href=re.compile(r'/ads/ad/\d+$'))
    ads = []
    
    for link in ad_links:
        href = link.get('href', '')
        match = re.search(r'/ads/ad/(\d+)$', href)
        if match:
            ad_id = match.group(1)
            title = link.get_text(strip=True)
            ads.append({
                'id': ad_id,
                'title': title,
                'url': f"{BASE_URL}{href}"
            })
    
    debug_print(f"Found {len(ads)} ads")
    return ads

def favorite_ad(session, ad_id):
    """Favorite an ad"""
    favorite_url = f"{BASE_URL}/ads/ad/{ad_id}/favorite"
    debug_print(f"Favoriting ad {ad_id} at {favorite_url}")
    response = session.get(favorite_url, allow_redirects=True)
    debug_print(f"Favorite response: {response.status_code}")
    return response.status_code == 200

def check_unfavorite_links(session, ad_id):
    """Check for unfavorite links for a specific ad after favoriting it"""
    debug_print(f"Checking for unfavorite links for ad {ad_id}")
    
    # Get the ads list page after favoriting
    response = session.get(ADS_URL)
    
    # Save the response for inspection
    with open("ads_page_after_favorite.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check different patterns of unfavorite links
    patterns = [
        f'href=".*?ad/{ad_id}/unfavorite"',
        f'href=".*?/ads/ad/{ad_id}/unfavorite"',
        f'href=".*?unfavorite.*?{ad_id}"',
    ]
    
    for pattern in patterns:
        links = soup.find_all('a', href=re.compile(pattern))
        debug_print(f"Found {len(links)} links matching pattern: {pattern}")
        
        for link in links:
            debug_print(f"Link: {link.get('href')} - Text: {link.get_text(strip=True)}")
    
    # Search for any link with "unfavorite" text
    all_unfav_links = soup.find_all('a', string=re.compile("unfavorite", re.IGNORECASE))
    debug_print(f"Found {len(all_unfav_links)} links with 'unfavorite' text:")
    
    for link in all_unfav_links:
        debug_print(f"Link: {link.get('href')} - Text: {link.get_text(strip=True)}")

    # Save link info to file
    all_links = soup.find_all('a')
    link_data = [{
        'href': link.get('href', ''), 
        'text': link.get_text(strip=True)
    } for link in all_links]
    
    with open("link_info.json", "w") as f:
        json.dump(link_data, f, indent=2)

def main():
    session = requests.Session()
    
    # Login
    if not login(session):
        debug_print("Login failed, exiting.")
        sys.exit(1)
    
    # Get ad list
    ads = get_ad_list(session)
    if not ads:
        debug_print("No ads found, exiting.")
        sys.exit(1)
    
    # Use the first ad for testing
    test_ad = ads[0]
    debug_print(f"Using ad for testing: ID={test_ad['id']}, Title={test_ad['title']}")
    
    # Favorite the ad
    if favorite_ad(session, test_ad['id']):
        debug_print("Successfully favorited the ad")
    else:
        debug_print("Failed to favorite the ad")
    
    # Check for unfavorite links
    check_unfavorite_links(session, test_ad['id'])
    debug_print("Test completed.")

if __name__ == "__main__":
    main()
