import csv

def get_unique_locations(csv_file):
    """
    Reads a CSV file and returns a dictionary of unique locations.
    """
    cities = set()
    districts = set()
    localities = set()

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'city' in row:
                cities.add(row['city'])
            if 'district' in row:
                districts.add(row['district'])
            if 'locality' in row:
                localities.add(row['locality'])

    return {
        'cities': sorted(list(cities)),
        'districts': sorted(list(districts)),
        'localities': sorted(list(localities))
    }

if __name__ == '__main__':
    locations = get_unique_locations('output.csv')
    print("Unique Cities:")
    for city in locations['cities']:
        print(f"- {city}")

    print("\nUnique Districts:")
    for district in locations['districts']:
        print(f"- {district}")

    print("\nUnique Localities:")
    for locality in locations['localities']:
        print(f"- {locality}")
