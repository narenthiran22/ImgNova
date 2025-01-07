import logging
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def home(request):
    return render(request, 'index.html')

def analyze_image(request):
    # If URL does not end with slash, redirect to the same URL with slash
    if not request.path.endswith('/'):
        return HttpResponseRedirect(request.path + '/')
    
    # Your existing logic
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        filter_type = request.POST.get('filter_type', '').strip()

        if not input_text:
            logging.warning("Search attempted with no text entered.")
            error_message = "No text entered for the search"
            return render(request, 'index.html', {'error': error_message})

        # Fetch related links and images using Google Custom Search API
        search_results = fetch_related_search(input_text, filter_type=filter_type)

        if not search_results:
            logging.error(f"No results found for query: {input_text}")
            error_message = "No images found for the search query."
            return render(request, 'index.html', {'error': error_message})

        return render(request, 'index.html', {'search_query': input_text, 'search_results': search_results})
    else:
        return render(request, 'index.html')

def fetch_related_search(query, filter_type='', max_results=30):
    if not query:
        return []

    filter_query = query
    if filter_type:
        filter_query += f" {filter_type}"

    results = []
    results_per_page = 5
    try:
        for start_index in range(1, min(max_results, 50), results_per_page):
            url = (
                f"https://www.googleapis.com/customsearch/v1"
                f"?key={settings.GOOGLE_API_KEY}&cx={settings.SEARCH_ENGINE_ID}&q={filter_query}&searchType=image"
                f"&start={start_index}&num={results_per_page}"
            )

            # Log the URL for debugging purposes
            logging.info(f"Making request to: {url}")

            response = requests.get(url)

            if response.status_code != 200:
                logging.error(f"API request failed with status code: {response.status_code} for query: {filter_query}")
                logging.error(f"Response body: {response.text}")
                return []

            data = response.json()

            # Log the full response data for debugging
            logging.info(f"API response: {data}")

            for item in data.get("items", []):
                if "link" in item:
                    results.append(item["link"])

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching search results: {e}")
        return []

    return results
