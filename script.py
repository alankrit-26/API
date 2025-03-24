import requests
import time

# API details
BASE_URL = "http://35.200.185.69:8000"
API_VERSIONS = ["v1", "v2", "v3"]

# Tracking results
unique_names = set()
query_list = [""]
total_results = {ver: 0 for ver in API_VERSIONS}  
query_hits = {ver: {} for ver in API_VERSIONS}  
api_calls = {ver: 0 for ver in API_VERSIONS}  

def get_suggestions(prefix, version):
    """Fetch suggestions from the API for a given prefix."""
    global api_calls
    url = f"{BASE_URL}/{version}/autocomplete?query={prefix}"
    
    try:
        response = requests.get(url)
        api_calls[version] += 1  
        
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            total_results[version] += count  
            query_hits[version][prefix] = count  
            return data.get("results", [])
        
        elif response.status_code == 429:
            print(f"Oops! Too many requests for '{prefix}'. Waiting a bit...")
            time.sleep(2)
            return get_suggestions(prefix, version)
        
        else:
            print(f"Error fetching '{prefix}' (Status: {response.status_code})")
            return []
    
    except Exception as e:
        print(f"Request failed for '{prefix}': {e}")
        return []

def explore_version(version):
    """Find all possible names for a given API version."""
    global query_list
    query_list = [""]  

    while query_list:
        current_query = query_list.pop(0)
        suggestions = get_suggestions(current_query, version)
        
        if not suggestions:
            continue
        
        for name in suggestions:
            if name not in unique_names:
                unique_names.add(name)
                query_list.append(name[:len(current_query) + 1])  

        time.sleep(0.3)

    print(f" Version {version}:")
    print(f"   - Unique names found: {len(unique_names)}")
    print(f"   - Total results from API: {total_results[version]}")
    print(f"   - API requests made: {api_calls[version]}\n")
    return unique_names

if __name__ == "__main__":
    for api_version in API_VERSIONS:
        unique_names.clear()
        query_hits[api_version] = {}  
        api_calls[api_version] = 0  
        
        print(f" Searching names in API {api_version}...")
        extracted_names = explore_version(api_version)
        
        print(f" Done! Found {len(extracted_names)} unique names.")
        print(f" Total API responses for {api_version}: {total_results[api_version]}")
        print(f" Total API calls: {api_calls[api_version]}\n")
