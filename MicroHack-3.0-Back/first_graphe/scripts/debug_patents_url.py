import requests
from bs4 import BeautifulSoup
import json

def test_url(url, headers=None):
    res = []
    res.append(f"\nTesting URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        res.append(f"Status Code: {response.status_code}")
        res.append(f"Content Type: {response.headers.get('Content-Type')}")
        res.append(f"Content Length: {len(response.content)}")
        
        if response.status_code == 200:
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    data = response.json()
                    res.append(f"JSON Keys: {list(data.keys())}")
                    if 'results' in data:
                        cluster = data['results'].get('cluster', [])
                        res.append(f"Found {len(cluster)} items in cluster")
                        if cluster:
                            res.append(f"Sample item keys: {list(cluster[0].get('result', {}).keys())}")
                except:
                    res.append("Failed to parse JSON")
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                res.append(f"Title: {soup.title.string if soup.title else 'No Title'}")
                selectors = ['section.search-result-item', 'search-result-item', 'article', '[data-result]']
                for sel in selectors:
                    items = soup.select(sel)
                    if items:
                        res.append(f"Found {len(items)} items using selector: {sel}")
                
                scripts = soup.find_all('script')
                res.append(f"Found {len(scripts)} script tags")
    except Exception as e:
        res.append(f"Error: {e}")
    return "\n".join(res)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

output = []
output.append(test_url("https://patents.google.com/?q=Internet+of+Things", headers))
output.append(test_url("https://patents.google.com/xhr/query?q=Internet+of+Things", {**headers, 'Accept': 'application/json'}))
output.append(test_url("https://patents.google.com/search?q=Internet+of+Things", headers))

with open("c:/Users/CBBC/Desktop/1st-graph/graph-1-scraping/logs/debug_patents_results.txt", "w") as f:
    f.write("\n".join(output))
