#!/usr/bin/env python3
"""
Script to extract the macOS download link from Rectangle Pro's download page.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import sys


def encode_url_path(url):
    """Properly encode URL path components."""
    parsed = urlparse(url)
    # Encode the path components
    encoded_path = '/'.join(quote(segment, safe='') for segment in parsed.path.split('/'))
    # Reconstruct URL with encoded path
    return f"{parsed.scheme}://{parsed.netloc}{encoded_path}" + (f"?{parsed.query}" if parsed.query else "") + (f"#{parsed.fragment}" if parsed.fragment else "")


def get_rectangle_production_link():
    """Fetch and parse the Rectangle Pro download page to extract macOS download link."""
    base_url = "https://rectangleapp.com/pro"
    
    try:
        # Fetch the page
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for download links
        # Strategy 1: Look for links with "Download" in the text
        download_links = soup.find_all('a', href=True, string=lambda text: text and 'download' in text.lower())
        
        # Strategy 2: Look for links containing "Download" in text (more flexible)
        if not download_links:
            all_links = soup.find_all('a', href=True)
            download_links = [link for link in all_links if 'download' in link.get_text(strip=True).lower()]
        
        # Strategy 3: Look for links with download-related href or classes
        if not download_links:
            all_links = soup.find_all('a', href=True)
            download_links = [link for link in all_links 
                            if 'download' in link.get('href', '').lower() or 
                               'dmg' in link.get('href', '').lower() or
                               'zip' in link.get('href', '').lower()]
        
        # Filter and find the actual download URL
        for link in download_links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            # Look for download links (skip anchor links, etc.)
            if href and href != '#' and ('rectangle' in href.lower() or 'download' in href.lower() or href.startswith('http') or 'dmg' in href.lower() or 'zip' in href.lower()):
                # If it's a relative URL, make it absolute
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    full_url = href
                else:
                    # Check if it's a path without leading slash
                    if not href.startswith('#'):
                        full_url = urljoin(base_url, href)
                    else:
                        continue
                
                # Properly encode the URL
                full_url = encode_url_path(full_url)
                
                # Prefer links that contain download-related terms
                if 'dmg' in href.lower() or 'zip' in href.lower() or 'download' in text:
                    print(full_url)
                    return
        
        # If no specific match found, try to find any download link
        if download_links:
            href = download_links[0].get('href', '')
            if href and href != '#':
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = urljoin(base_url, href)
                # Properly encode the URL
                full_url = encode_url_path(full_url)
                print(full_url)
                return
        
        # Fallback: Look for any link with dmg or zip extension
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            if href and ('dmg' in href.lower() or 'zip' in href.lower()):
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = urljoin(base_url, href)
                # Properly encode the URL
                full_url = encode_url_path(full_url)
                print(full_url)
                return
        
        print("Error: Could not find macOS download link", file=sys.stderr)
        sys.exit(1)
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing page: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    get_rectangle_production_link()

