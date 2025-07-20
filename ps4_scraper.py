#!/usr/bin/env python3
"""
SuperPSX PS4 Games Scraper
Scrapes PS4 game list from superpsx.com sitemaps and generates JSON file
Optimized for GitHub Actions automation
"""

import json
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Set
import sys
import os

class PS4GamesScraper:
    def __init__(self):
        self.base_url = "https://www.superpsx.com"
        self.sitemap_urls = [
            f"{self.base_url}/post-sitemap.xml",
            f"{self.base_url}/post-sitemap2.xml", 
            f"{self.base_url}/post-sitemap3.xml",
            f"{self.base_url}/post-sitemap4.xml"
        ]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_sitemap(self, url: str) -> str:
        """Fetch sitemap XML content"""
        try:
            print(f"📥 Fetching sitemap: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return ""

    def extract_ps4_urls_from_xml(self, xml_content: str) -> Set[str]:
        """Extract PS4 game URLs from sitemap XML"""
        urls = set()

        if not xml_content:
            return urls

        try:
            # Parse XML
            root = ET.fromstring(xml_content)

            # Handle different XML namespaces
            namespaces = {
                'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
            }

            # Find all URL elements
            for url_elem in root.findall('.//sitemap:url', namespaces):
                loc_elem = url_elem.find('sitemap:loc', namespaces)
                if loc_elem is not None:
                    url = loc_elem.text
                    if url and 'ps4-fpkg' in url:
                        urls.add(url)

            # Fallback for XML without namespaces
            if not urls:
                for url_elem in root.findall('.//url'):
                    loc_elem = url_elem.find('loc')
                    if loc_elem is not None:
                        url = loc_elem.text
                        if url and 'ps4-fpkg' in url:
                            urls.add(url)

        except ET.ParseError as e:
            print(f"❌ XML parsing error: {e}")

        return urls

    def extract_game_name(self, url: str) -> str:
        """Extract and clean game name from URL"""
        # Extract the slug from URL (part between last / and -ps4-fpkg/)
        slug = url.split('/')[-2]

        # Remove -ps4-fpkg suffix if exists
        if slug.endswith('-ps4-fpkg'):
            slug = slug[:-9]

        # Convert hyphens to spaces and capitalize words
        name = slug.replace('-', ' ').title()

        # Clean specific terms
        name = re.sub(r'\bPs4\b', '', name)
        name = re.sub(r'\bFpkg\b', '', name)
        name = re.sub(r'\bPkg\b', '', name)
        name = re.sub(r'\s+', ' ', name)  # Remove multiple spaces
        name = name.strip()

        # Common corrections
        corrections = {
            'P T': 'P.T.',
            'Dmc': 'DMC',
            'Nba': 'NBA',
            'Nfl': 'NFL', 
            'Nhl': 'NHL',
            'Ufc': 'UFC',
            'Vr': 'VR',
            'Hd': 'HD',
            'Dx': 'DX',
            'Xl': 'XL',
            'Ii': 'II',
            'Iii': 'III',
            'Iv': 'IV',
            'Vi': 'VI',
            'Vii': 'VII',
            'Viii': 'VIII',
            'Ix': 'IX',
            'Xv': 'XV',
            'Gta': 'GTA',
            'Rpg': 'RPG',
            'Fps': 'FPS',
            'Rts': 'RTS',
            'Mmo': 'MMO',
            'Dlc': 'DLC'
        }

        for old, new in corrections.items():
            name = re.sub(r'\b' + old + r'\b', new, name)

        return name

    def is_real_game(self, name: str, url: str) -> bool:
        """Filter out tools, homebrews and non-game content"""
        name_lower = name.lower()
        url_lower = url.lower()

        # Terms that indicate tools/homebrews/non-games
        excluded_terms = [
            'homebrew', 'tool', 'utility', 'installer', 'manager', 'browser',
            'emulator', 'exploit', 'jailbreak', 'pkg linker', 'ftp', 'multiman',
            'webman', 'hen', 'cfw', 'ofw', 'backup', 'save data', 'theme',
            'avatar', 'wallpaper', 'plugin', 'mod menu', 'cheat', 'trainer'
        ]

        # Check for excluded terms
        for term in excluded_terms:
            if term in name_lower or term in url_lower:
                return False

        # Check minimum name length
        if len(name.strip()) < 2:
            return False

        return True

    def scrape_all_games(self) -> List[Dict[str, str]]:
        """Scrape all PS4 games from sitemaps"""
        all_urls = set()

        # Fetch all sitemaps
        for sitemap_url in self.sitemap_urls:
            xml_content = self.fetch_sitemap(sitemap_url)
            urls = self.extract_ps4_urls_from_xml(xml_content)
            all_urls.update(urls)
            print(f"📊 Found {len(urls)} PS4 URLs in {sitemap_url}")

        print(f"🎯 Total unique PS4 URLs found: {len(all_urls)}")

        # Process URLs to extract game data
        games_list = []
        filtered_count = 0

        for url in all_urls:
            game_name = self.extract_game_name(url)

            if self.is_real_game(game_name, url):
                games_list.append({
                    "name": game_name,
                    "url": url
                })
            else:
                filtered_count += 1

        # Sort games alphabetically
        games_list.sort(key=lambda x: x['name'].lower())

        print(f"🎮 Real games found: {len(games_list)}")
        print(f"🚫 Filtered out (tools/homebrews): {filtered_count}")

        return games_list

    def generate_json(self, games_list: List[Dict[str, str]]) -> Dict:
        """Generate final JSON structure"""
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "source": "https://www.superpsx.com/ps4-fake-pkgs-game-list/",
            "extraction_method": "Sitemap XML parsing + URL filtering",
            "total_games": len(games_list),
            "games": games_list
        }

    def save_json(self, data: Dict, filename: str = "ps4_games_list.json") -> bool:
        """Save JSON data to file"""
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            file_size = os.path.getsize(filename)
            print(f"✅ JSON saved successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Size: {file_size:,} bytes")
            return True

        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False

    def run(self, output_file: str = "ps4_games_list.json") -> bool:
        """Main execution method"""
        print("🚀 Starting PS4 games scraping...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Scrape games
            games_list = self.scrape_all_games()

            if not games_list:
                print("❌ No games found!")
                return False

            if len(games_list) < 1200:
                print(f"⚠️  Warning: Only {len(games_list)} games found (expected at least 1200)")

            # Generate JSON
            json_data = self.generate_json(games_list)

            # Save to file
            success = self.save_json(json_data, output_file)

            if success:
                print(f"🎉 Scraping completed successfully!")
                print(f"📈 Final stats:")
                print(f"   • Total games: {json_data['total_games']}")
                print(f"   • Method: {json_data['extraction_method']}")
                print(f"   • Source: {json_data['source']}")

            return success

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

def main():
    """Main function for command line execution"""
    # Get output file from command line argument or use default
    output_file = sys.argv[1] if len(sys.argv) > 1 else "ps4_games_list.json"

    # Initialize and run scraper
    scraper = PS4GamesScraper()
    success = scraper.run(output_file)

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
