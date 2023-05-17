import requests
import re


class Scrape:
    @staticmethod
    def extract_email(company):
        headers = {
            'Cookie': 'drupal.samesite=1'
        }
        response = requests.request("GET", company['url'], headers=headers)
        # Define the regular expression pattern for an email address
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Search for the pattern in the given text
        match = re.search(pattern, response.text)

        # Return the email address if found, otherwise return None
        if match:
            return match.group()
        else:
            return None
