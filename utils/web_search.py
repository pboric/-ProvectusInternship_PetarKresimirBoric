import requests
import os
from dotenv import load_dotenv
import json
import re
import time

class WebSearchEngine:
    """
    Engine for searching concert information online.
    """
    
    def __init__(self):
        """Initialize the web search engine."""
        load_dotenv()
        
        # API key should be stored in .env file
        self.api_key = os.getenv("SERPAPI_KEY", None)
        
        # Check if API key is available
        self.enabled = self.api_key is not None
        
        # Set up session with retry logic
        self.session = requests.Session()
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def is_enabled(self):
        """Check if the web search is enabled (API key is available)."""
        return self.enabled
    
    def search_concert_info(self, artist_name):
        """
        Search for concert information for a specific artist.
        
        Args:
            artist_name (str): Name of the artist or band
            
        Returns:
            tuple: (success, message)
                success (bool): Whether the search was successful
                message (str): Search results or error message
        """
        if not self.enabled:
            return False, "Web search is not enabled. API key not found."
        
        try:
            # Clean artist name
            artist_name = artist_name.strip()
            
            # Formulate search query
            query = f"{artist_name} concerts 2025 2026 tour dates"
            
            # Call SerpAPI with retry logic
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
                "num": 10  # Number of results
            }
            
            # Try with retries
            for attempt in range(self.max_retries):
                try:
                    response = self.session.get(
                        "https://serpapi.com/search", 
                        params=params,
                        timeout=30  # Add timeout
                    )
                    
                    # If successful, break out of retry loop
                    if response.status_code == 200:
                        break
                    
                    # If we get a 520 error or other server error, wait and retry
                    if response.status_code >= 500:
                        if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                            time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                            continue
                    
                    # For other errors, return the error message
                    if response.status_code != 200:
                        return False, f"Error searching for concert information. Status code: {response.status_code}"
                
                except requests.exceptions.Timeout:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    else:
                        return False, "Request timed out. Please try again later."
                
                except requests.exceptions.RequestException as e:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    else:
                        return False, f"Network error: {str(e)}"
            
            # Check if we got a successful response
            if response.status_code != 200:
                return False, f"Error searching for concert information after {self.max_retries} attempts. Status code: {response.status_code}"
            
            # Parse results
            try:
                results = response.json()
            except json.JSONDecodeError:
                return False, "Error parsing search results. The API response was not valid JSON."
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            if not organic_results:
                return False, f"No concert information found for {artist_name}."
            
            # Process results
            concert_info = self._process_search_results(organic_results, artist_name)
            
            return True, concert_info
        
        except Exception as e:
            return False, f"Error searching for concert information: {str(e)}"
    
    def _process_search_results(self, results, artist_name):
        """
        Process search results to extract concert information.
        
        Args:
            results (list): List of search results
            artist_name (str): Name of the artist
            
        Returns:
            str: Processed concert information
        """
        concert_info = f"Concert Information for {artist_name} (2025-2026):\n\n"
        
        # Extract relevant information from results
        for result in results:
            title = result.get("title", "")
            link = result.get("link", "")
            snippet = result.get("snippet", "")
            
            # Check if result is about concerts and relevant years
            is_concert_related = any(keyword in title.lower() or keyword in snippet.lower() 
                                     for keyword in ["concert", "tour", "live", "show", "performance"])
            
            has_relevant_years = re.search(r"202[5-6]", title + snippet) is not None
            
            if is_concert_related and has_relevant_years:
                concert_info += f"- {title}\n"
                concert_info += f"  {snippet}\n"
                concert_info += f"  Source: {link}\n\n"
        
        if concert_info == f"Concert Information for {artist_name} (2025-2026):\n\n":
            concert_info += "No specific concert information found for 2025-2026.\n"
            concert_info += "The artist may not have announced tour dates for this period yet.\n"
        
        return concert_info 