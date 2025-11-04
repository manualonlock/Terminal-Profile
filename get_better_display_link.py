#!/usr/bin/env python3
"""
Script to extract the macOS download link from BetterDisplay's GitHub page.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import sys
import re


def encode_url_path(url):
    """Properly encode URL path components."""
    parsed = urlparse(url)
    # Encode the path components
    encoded_path = '/'.join(quote(segment, safe='') for segment in parsed.path.split('/'))
    # Reconstruct URL with encoded path
    return f"{parsed.scheme}://{parsed.netloc}{encoded_path}" + (f"?{parsed.query}" if parsed.query else "") + (f"#{parsed.fragment}" if parsed.fragment else "")


def get_better_display_link():
    """Fetch and parse the BetterDisplay GitHub page to extract macOS download link."""
    base_url = "https://github.com/waydabber/BetterDisplay"
    url = f"{base_url}?tab=readme-ov-file"
    
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Strategy 1: Look for links with "Download" and "macOS" or "Mac" in the text
        download_links = soup.find_all('a', href=True)
        macos_download_links = []
        
        for link in download_links:
            text = link.get_text(strip=True).lower()
            href = link.get('href', '')
            
            # Look for "Download" and "macOS" or "Mac" in text
            if ('download' in text and ('macos' in text or 'mac' in text)) or \
               ('download' in text and ('app' in text or 'for' in text)):
                macos_download_links.append(link)
        
        # Strategy 2: Look for links pointing to releases or assets
        if not macos_download_links:
            for link in download_links:
                href = link.get('href', '')
                text = link.get_text(strip=True).lower()
                
                # Check for GitHub releases links or asset downloads
                if '/releases' in href or '/download' in href or 'dmg' in href.lower():
                    if 'macos' in text or 'mac' in text or 'download' in text:
                        macos_download_links.append(link)
        
        # Strategy 3: Look for links with .dmg extension
        if not macos_download_links:
            for link in download_links:
                href = link.get('href', '')
                if 'dmg' in href.lower():
                    macos_download_links.append(link)
        
        # Process found links
        for link in macos_download_links:
            href = link.get('href', '')
            if not href or href == '#':
                continue
            
            # If it's a relative URL, make it absolute
            if href.startswith('/'):
                full_url = urljoin('https://github.com', href)
            elif href.startswith('http'):
                full_url = href
            else:
                # Relative URL from current page
                full_url = urljoin(base_url, href)
            
            # If it's a GitHub releases page link, we need to get the latest release
            if '/releases' in full_url and '/tag/' not in full_url and '/download/' not in full_url:
                # Try to get the latest release download link
                releases_url = full_url if '/releases' in full_url else f"{base_url}/releases/latest"
                try:
                    releases_response = requests.get(releases_url, timeout=10, allow_redirects=True)
                    releases_response.raise_for_status()
                    releases_soup = BeautifulSoup(releases_response.content, 'html.parser')
                    
                    # Look for .dmg download links in the releases page
                    release_links = releases_soup.find_all('a', href=True)
                    for release_link in release_links:
                        release_href = release_link.get('href', '')
                        if '.dmg' in release_href.lower() and '/download/' in release_href:
                            if release_href.startswith('/'):
                                download_url = urljoin('https://github.com', release_href)
                            elif release_href.startswith('http'):
                                download_url = release_href
                            else:
                                download_url = urljoin('https://github.com', release_href)
                            
                            # Properly encode the URL
                            download_url = encode_url_path(download_url)
                            print(download_url)
                            return
                except:
                    pass
            
            # If it's already a direct download link (contains /download/ or ends with .dmg)
            if '/download/' in full_url or full_url.endswith('.dmg') or '.dmg' in full_url:
                # Properly encode the URL
                full_url = encode_url_path(full_url)
                print(full_url)
                return
        
        # Fallback: Try to get the latest release directly
        try:
            latest_release_url = f"{base_url}/releases/latest"
            releases_response = requests.get(latest_release_url, timeout=10, allow_redirects=True)
            releases_response.raise_for_status()
            releases_soup = BeautifulSoup(releases_response.content, 'html.parser')
            
            # Look for .dmg download links
            release_links = releases_soup.find_all('a', href=True)
            for release_link in release_links:
                release_href = release_link.get('href', '')
                if '.dmg' in release_href.lower() and '/download/' in release_href:
                    if release_href.startswith('/'):
                        download_url = urljoin('https://github.com', release_href)
                    elif release_href.startswith('http'):
                        download_url = release_href
                    else:
                        download_url = urljoin('https://github.com', release_href)
                    
                    # Properly encode the URL
                    download_url = encode_url_path(download_url)
                    print(download_url)
                    return
        except:
            pass
        
        print("Error: Could not find macOS download link", file=sys.stderr)
        sys.exit(1)
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing page: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    get_better_display_link()

