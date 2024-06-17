import requests
import json
from collections import defaultdict


class BreweryData:
    def __init__(self):
        self.base_url = "https://api.openbrewerydb.org/breweries"
        self.data = []

    def fetch_data(self, state):
        response = requests.get(f"{self.base_url}?by_state={state}")
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(f"Failed to fetch data for state: {state}")

    def list_breweries(self):
        return [brewery['name'] for brewery in self.data]

    def count_breweries(self):
        return len(self.data)

    def count_types_by_city(self):
        city_brewery_types = defaultdict(lambda: defaultdict(int))
        for brewery in self.data:
            city = brewery['city']
            brewery_type = brewery['brewery_type']
            city_brewery_types[city][brewery_type] += 1
        return city_brewery_types

    def count_breweries_with_websites(self):
        return len([brewery for brewery in self.data if brewery.get('website_url')])


def main():
    states = ['Alaska', 'Maine', 'New York']
    state_brewery_data = {}

    for state in states:
        brewery_data = BreweryData()
        brewery_data.fetch_data(state)
        state_brewery_data[state] = brewery_data

    for state, brewery_data in state_brewery_data.items():
        print(f"\nBreweries in {state}:")
        for name in brewery_data.list_breweries():
            print(name)

        print(f"\nTotal number of breweries in {state}: {brewery_data.count_breweries()}")

        print(f"\nNumber of types of breweries in each city in {state}:")
        city_brewery_types = brewery_data.count_types_by_city()
        for city, types in city_brewery_types.items():
            print(f"{city}:")
            for type, count in types.items():
                print(f"  {type}: {count}")

        print(f"\nNumber of breweries with websites in {state}: {brewery_data.count_breweries_with_websites()}")


if __name__ == "__main__":
    main()
