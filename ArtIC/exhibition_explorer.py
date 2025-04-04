import requests


def get_search_term() -> str:
    """
    Prompts the user to enter a search term for exhibitions.

    Returns:
        str: The search term entered by the user.
    """
    return input("Enter a search term for exhibitions: ")


def search_exhibitions(search_term: str) -> list:
    """
    Searches the ArtIC API for exhibitions matching the given search term
    and that have artwork titles.

    Args:
        search_term (str): The term to search for in exhibitions.

    Returns:
        list: A list of exhibitions that match the search criteria and have artwork titles.
    """
    # Base URL for the ArtIC API exhibitions search endpoint
    url = "https://api.artic.edu/api/v1/exhibitions/search"

    # Create a query that searches for the term and ensures artwork_titles exists
    query = {
        "bool": {
            "must": [{"match": {"title": search_term}}],
            "filter": [{"exists": {"field": "artwork_titles"}}],
        }
    }

    # Parameters for the API request
    params = {
        "q": search_term,
        "query": query,
        "fields": "id,title,aic_start_at,aic_end_at,artwork_titles",
        "limit": 100,  # Get a good number of results
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Return only exhibitions that have artwork_titles
        exhibitions = [
            exhibition
            for exhibition in data.get("data", [])
            if "artwork_titles" in exhibition and exhibition["artwork_titles"]
        ]
        return exhibitions
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return []


def display_exhibition_count(exhibitions: list) -> None:
    """
    Displays the number of exhibitions found that match the search criteria.

    Args:
        exhibitions (list): The list of exhibitions to display the count for.
    """
    count = len(exhibitions)
    if count == 0:
        print("No exhibitions found matching your search term.")
    elif count == 1:
        print("1 exhibition found matching your search term.")
    else:
        print(f"{count} exhibitions found matching your search term.")


def get_exhibition_count(max_count: int) -> int:
    """
    Prompts the user to enter the number of exhibitions they want to view.

    Args:
        max_count (int): The maximum number of exhibitions available.

    Returns:
        int: The number of exhibitions the user wants to view.
    """
    while True:
        try:
            if max_count == 0:
                return 0

            count = input(
                f"How many exhibitions would you like to view (1-{max_count}, or 0 to go back): "
            )
            count = int(count)

            if 0 <= count <= max_count:
                return count
            else:
                print(f"Please enter a number between 0 and {max_count}.")
        except ValueError:
            print("Please enter a valid number.")


def get_exhibition_artwork(exhibition: dict) -> list:
    """
    Retrieves the artwork titles for a given exhibition.

    Args:
        exhibition (dict): The exhibition to get artwork titles for.

    Returns:
        list: The list of artwork titles for the exhibition.
    """
    # Since we filtered for exhibitions with artwork_titles in our search,
    # we can directly access the artwork_titles field
    return exhibition.get("artwork_titles", [])


def display_exhibition_artwork(exhibition: dict, artwork_titles: list) -> None:
    """
    Displays the title of the exhibition and its artwork titles.

    Args:
        exhibition (dict): The exhibition information.
        artwork_titles (list): The list of artwork titles to display.
    """
    print(f"\nExhibition: {exhibition['title']}")
    print(
        f"Date: {exhibition.get('aic_start_at', 'Unknown')} to {exhibition.get('aic_end_at', 'Unknown')}"
    )
    print("\nArtworks in this exhibition:")

    if not artwork_titles:
        print("No artwork titles available for this exhibition.")
    else:
        for i, title in enumerate(artwork_titles, 1):
            print(f"{i}. {title}")


def continue_program() -> bool:
    """
    Asks the user if they want to continue searching for exhibitions.

    Returns:
        bool: True if the user wants to continue, False otherwise.
    """
    response = input(
        "\nWould you like to search for another exhibition? (y/n): "
    ).lower()
    return response == "y" or response == "yes"


def main():
    """
    Main function that runs the program loop.
    Allows users to search for exhibitions, view artwork titles,
    and repeat the process until they choose to exit.
    """
    print("Welcome to the Art Institute of Chicago Exhibition Search!")

    while True:
        # Get search term from user
        search_term = get_search_term()

        # Search for exhibitions
        print(f"Searching for exhibitions matching '{search_term}'...")
        exhibitions = search_exhibitions(search_term)

        # Display the count of exhibitions found
        display_exhibition_count(exhibitions)

        # If exhibitions were found, let the user choose how many to view
        if exhibitions:
            count = get_exhibition_count(len(exhibitions))

            # Display the artwork for each selected exhibition
            for i in range(count):
                if i < len(exhibitions):
                    exhibition = exhibitions[i]
                    artwork_titles = get_exhibition_artwork(exhibition)
                    display_exhibition_artwork(exhibition, artwork_titles)

        # Ask if the user wants to continue
        if not continue_program():
            print(
                "Thank you for using the Art Institute of Chicago Exhibition Search. Goodbye!"
            )
            break


if __name__ == "__main__":
    main()
