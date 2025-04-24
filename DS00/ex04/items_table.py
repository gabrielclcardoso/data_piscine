import csv
from sys import stderr


def main():

    try:
        f = open("subject/item/item.csv")
    except Exception as e:
        print(f"{type(e).__name__}: {e}", file=stderr)
        exit(1)

    with f:
        try:
            enums = get_sets(f)
            print(enums)
        except Exception as e:
            print("Error: make sure the csv file is correctly formatted",
                  file=stderr)
            print(f"{type(e).__name__}: {e}", file=stderr)
            exit(1)


def get_sets(file):
    """Reads the items.csv file and returns a dictonary with 2 sets, one
    representing the options for category code and one representing the options
    for brand
    """

    table = csv.DictReader(file)
    sets = {'category_code': set(), 'brand': set()}

    for row in table:
        sets['category_code'].add(row['category_code'])
        sets['brand'].add(row['brand'])

    return sets


if __name__ == "__main__":
    main()
