#!/usr/bin/env python3
"""
Script to extract the macOS download link from Cursor's download page.
"""

import requests
from bs4 import BeautifulSoup
import sys


def get_cursor_macos_download_link():
    """Fetch and parse the Cursor download page to extract macOS download link."""
    url = "https://cursor.com/download"
    
    try:
        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for macOS download links
        # Try multiple strategies to find the link
        
        # Strategy 1: Look for links with "macOS" or "Mac" in the text
        macos_links = soup.find_all('a', href=True, string=lambda text: text and ('macOS' in text.lower() or 'mac' in text.lower()))
        
        # Strategy 2: Look for download buttons/links containing "Mac"
        if not macos_links:
            macos_links = soup.find_all('a', href=True)
            macos_links = [link for link in macos_links if link.get_text(strip=True).lower().startswith('mac')]
        
        # Strategy 3: Look for links with download-related attributes or classes
        if not macos_links:
            macos_links = soup.find_all('a', href=True)
            macos_links = [link for link in macos_links 
                          if 'mac' in link.get('href', '').lower() or 
                             'mac' in link.get_text(strip=True).lower()]
        
        # Filter out non-download links and find the actual download URL
        for link in macos_links:
            href = link.get('href', '')
            if href and ('cursor' in href.lower() or 'download' in href.lower() or href.startswith('http')):
                # If it's a relative URL, make it absolute
                if href.startswith('/'):
                    full_url = f"https://cursor.com{href}"
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = f"https://cursor.com/{href}"
                
                # Prefer universal or ARM64 builds
                text = link.get_text(strip=True).lower()
                if 'universal' in text or 'arm64' in text:
                    print(full_url)
                    return
        
        # If no specific match found, print the first macOS link found
        if macos_links:
            href = macos_links[0].get('href', '')
            if href:
                if href.startswith('/'):
                    full_url = f"https://cursor.com{href}"
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = f"https://cursor.com/{href}"
                print(full_url)
                return
        
        # If still not found, try to find any download link
        download_links = soup.find_all('a', href=True)
        for link in download_links:
            href = link.get('href', '')
            if href and ('cursor' in href.lower() and ('dmg' in href.lower() or 'zip' in href.lower())):
                if href.startswith('/'):
                    full_url = f"https://cursor.com{href}"
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = f"https://cursor.com/{href}"
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
    get_cursor_macos_download_link()

