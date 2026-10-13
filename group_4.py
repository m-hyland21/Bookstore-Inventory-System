"""
COM155 Coursework 2 - Book Store Inventory System (BIS)
Group: 4
Members:
    Johnathan Kelly  - Features 1, 2, 3
    Matthew Hyland   - Features 4, 5 + load_books() utility
    Jack Madill      - Features 6, 7, 8

This module implements the Book Store Inventory System with 9 menu options:
    1. Display all book titles and details      [Johnathan Kelly]
    2. Summary report                           [Johnathan Kelly]
    3. Genre report                             [Johnathan Kelly]
    4. Add a new book                           [Matthew Hyland]
    5. Query and update stock                   [Matthew Hyland]
    6. Sort books alphabetically by author      [Jack Madill]
    7. Plot bar chart of books per genre        [Jack Madill]
    8. Low-stock alert report                   [Jack Madill]
    9. Quit
"""

import csv

FILENAME = "Books_data.csv"


def load_books():
    """
    Load all books from the CSV file into a list of dictionaries.

    Each book is represented as a dict with keys matching the CSV
    columns: Author, Title, Format, Publisher, Cost, Stock, Genre.
    Cost is converted to float and Stock to int.

    Returns:
        list[dict]: list of book dictionaries, or empty list on failure.

    Implements: Shared utility (CSV loader) — Matthew Hyland.
    """
    books = []
    try:
        with open(FILENAME, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row["Cost"] = float(row["Cost"])
                    row["Stock"] = int(float(row["Stock"]))
                except ValueError:
                    continue

                if not row.get("Genre", "").strip():
                    row["Genre"] = "unknown"

                books.append(row)
    except FileNotFoundError:
        print(f"Error: '{FILENAME}' not found. Please check the file is in the same folder.")
        return books
    except Exception as error:
        print(f"Error reading the file: {error}")
        return books

    print(f"Loaded {len(books)} books from {FILENAME}.")
    return books


def display_menu():
    """
    Display the main menu of options to the user.
    """
    print("\n===== Book Store Inventory System =====")
    print("1. Display all book titles and details")
    print("2. Summary report")
    print("3. Genre report")
    print("4. Add a new book")
    print("5. Query and update stock")
    print("6. Sort books alphabetically by author")
    print("7. Plot bar chart of books per genre")
    print("8. Low-stock alert report")
    print("9. Quit")


def list_books(books):
    """
    Display all books in the inventory with full details.

    Shows Title, Author, Cost, Stock, and Genre for every book
    currently in the in-memory inventory.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 1 — Johnathan Kelly.
    """
    if not books:
        print("No books in inventory.")
        return books

    print("\n--- All Books in Inventory ---")
    for book in books:
        print(f"Title: {book['Title']}")
        print(f"  Author: {book['Author']}")
        print(f"  Cost: £{book['Cost']:.2f}")
        print(f"  Stock: {book['Stock']}")
        print(f"  Genre: {book['Genre']}")
        print()
    print(f"Total books in inventory: {len(books)}")
    return books


def summary_report(books):
    """
    Display a summary report of the inventory.

    Shows total number of titles, total stock value
    (sum of Cost * Stock for every book), and the
    average book price.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 2 — Johnathan Kelly.
    """
    if not books:
        print("No books available for summary.")
        return books

    total_titles = len(books)
    total_stock_value = 0
    total_price = 0

    for book in books:
        total_stock_value += book["Cost"] * book["Stock"]
        total_price += book["Cost"]

    average_price = total_price / total_titles

    print("\n--- Summary Report ---")
    print(f"Total number of titles: {total_titles}")
    print(f"Total stock value: £{total_stock_value:.2f}")
    print(f"Average book price: £{average_price:.2f}")

    return books


def genre_report(books):
    """
    Display a count of books grouped by genre.

    Iterates through the inventory and produces a
    report showing how many books exist in each
    unique genre, sorted alphabetically.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 3 — Johnathan Kelly.
    """
    if not books:
        print("No books available for genre report.")
        return books

    genre_counts = {}
    for book in books:
        genre = book["Genre"]
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    print("\n--- Genre Report ---")
    for genre in sorted(genre_counts):
        print(f"{genre}: {genre_counts[genre]} book(s)")
    print(f"\nTotal genres: {len(genre_counts)}")

    return books


def add_new_book(books):
    """
    Add a new book to the inventory.

    Prompts the user for Title, Author, Cost, Stock and Genre.
    If the title already exists, the stock count of that book is
    increased. If not, a new book record is appended to the list.
    Finally, displays the new total number of titles.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the updated inventory.

    Implements: Feature 4 (advanced) — Matthew Hyland.
    """
    print("\n--- Add a New Book ---")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    cost_input = input("Cost (e.g. 9.99): ").strip()
    stock_input = input("Initial stock count: ").strip()
    genre = input("Genre: ").strip().lower()

    try:
        cost = float(cost_input)
        stock = int(float(stock_input))
        if cost < 0 or stock < 0:
            print("Cost and Stock cannot be negative. Book not added.")
            return books
    except ValueError:
        print("Invalid number format for Cost or Stock. Book not added.")
        return books

    found = False
    for book in books:
        if book["Title"].lower() == title.lower():
            book["Stock"] += stock
            found = True
            print(f"'{title}' already exists. Stock increased by {stock}.")
            break

    if not found:
        new_book = {
            "Author": author,
            "Title": title,
            "Format": "",
            "Publisher": "",
            "Cost": cost,
            "Stock": stock,
            "Genre": genre if genre else "unknown",
        }
        books.append(new_book)
        print(f"'{title}' added to inventory.")

    print(f"Total number of titles in inventory: {len(books)}")
    return books


def query_and_update_stock(books):
    """
    Query whether a book title exists in the inventory and update its stock.

    Prompts the user for a title. If the book is found, displays the current
    stock and asks whether to increase (I) or decrease (D) the stock level.
    The decrease branch handles two edge cases:
        - decrease amount greater than current stock (rejected),
        - stock reaching zero (flagged as out of stock).
    If the book is not found, an informative message is shown.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the updated inventory.

    Implements: Feature 5 (advanced) — Matthew Hyland.
    """
    print("\n--- Query and Update Stock ---")
    query_title = input("Enter the title to query: ").strip()

    found_book = None
    for book in books:
        if book["Title"].lower() == query_title.lower():
            found_book = book
            break

    if found_book is None:
        print(f"'{query_title}' not found in inventory.")
        return books

    print(f"\nFound: '{found_book['Title']}' by {found_book['Author']}")
    print(f"Current stock: {found_book['Stock']}")

    choice = input("Increase (I) or Decrease (D) stock? ").strip().lower()

    if choice not in ("i", "d"):
        print("Invalid choice. Please enter 'I' or 'D'. No changes made.")
        return books

    if choice == "i":
        try:
            amount = int(input("How many copies to add? ").strip())
            if amount <= 0:
                print("Amount must be positive. No changes made.")
                return books
        except ValueError:
            print("Invalid number. No changes made.")
            return books

        found_book["Stock"] += amount
        print(f"Stock for '{found_book['Title']}' increased by {amount}. New stock: {found_book['Stock']}")
        return books

    if choice == "d":
        try:
            amount = int(input("How many copies sold? ").strip())
            if amount <= 0:
                print("Amount must be positive. No changes made.")
                return books
        except ValueError:
            print("Invalid number. No changes made.")
            return books

        if amount > found_book["Stock"]:
            print(f"Cannot decrease by {amount}. Only {found_book['Stock']} in stock. No changes made.")
            return books

        found_book["Stock"] -= amount

        if found_book["Stock"] == 0:
            print(f"'{found_book['Title']}' is now OUT OF STOCK.")
        else:
            print(f"Stock for '{found_book['Title']}' decreased by {amount}. New stock: {found_book['Stock']}")

    return books


def sort_books_by_author(books):
    """
    Display all books sorted alphabetically by author name.

    Sorting is case-insensitive so "Adams" and "adams" are
    treated equally. The original inventory order is preserved
    (a sorted copy is built rather than mutating the list).

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 6 — Jack Madill.
    """
    if not books:
        print("No books in inventory.")
        return books

    sorted_books = sorted(books, key=lambda book: book["Author"].lower())

    print("\n--- Books Sorted by Author ---")
    for i, book in enumerate(sorted_books, start=1):
        author = book["Author"]
        title = book["Title"]
        format_type = book.get("Format", "")
        if format_type:
            print(f"{i}. {author} - {title} ({format_type})")
        else:
            print(f"{i}. {author} - {title}")

    print(f"\nTotal books: {len(sorted_books)}")
    return books


def display_genre_chart(books):
    """
    Display a bar chart of book counts per genre.

    Counts how many books exist in each genre, then plots them
    as a labelled bar chart using matplotlib. The chart opens
    in a separate window; close it to return to the menu.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 7 — Jack Madill.
    """
    if not books:
        print("No books available for chart.")
        return books

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed. Run: pip install matplotlib")
        return books

    genre_counts = {}
    for book in books:
        genre = book["Genre"]
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    labels = list(genre_counts.keys())
    values = list(genre_counts.values())

    plt.figure()
    plt.bar(labels, values)
    plt.title("Number of Books per Genre")
    plt.xlabel("Genre")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=45)
    plt.tight_layout()
    print("\nDisplaying genre bar chart. Close the chart window to return to the menu.")
    plt.show()

    return books


def low_stock_alert(books):
    """
    Display a low-stock alert listing books with low inventory.

    Threshold is 2 — any book with stock of 2 or fewer is flagged
    so the bookstore knows to reorder. This is the group's
    team-defined extra feature, beyond the brief's specified
    eight features, designed to support inventory management.

    Args:
        books (list[dict]): the current book inventory.

    Returns:
        list[dict]: the inventory unchanged.

    Implements: Feature 8 (team-defined extra) — Jack Madill.
    """
    if not books:
        print("No books in inventory.")
        return books

    threshold = 2

    low_stock_books = [book for book in books if book["Stock"] <= threshold]

    print(f"\n--- Low Stock Alert (stock <= {threshold}) ---")

    if not low_stock_books:
        print("No books are below the low-stock threshold.")
        return books

    low_stock_books.sort(key=lambda book: book["Stock"])

    for book in low_stock_books:
        title = book["Title"]
        author = book["Author"]
        stock = book["Stock"]
        if stock == 0:
            print(f"  [OUT OF STOCK] {title} by {author}")
        else:
            print(f"  [LOW: {stock}] {title} by {author}")

    print(f"\nTotal books needing attention: {len(low_stock_books)}")
    return books


if __name__ == "__main__":
    books = load_books()

    while True:
        display_menu()
        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            books = list_books(books)
        elif choice == "2":
            books = summary_report(books)
        elif choice == "3":
            books = genre_report(books)
        elif choice == "4":
            books = add_new_book(books)
        elif choice == "5":
            books = query_and_update_stock(books)
        elif choice == "6":
            books = sort_books_by_author(books)
        elif choice == "7":
            books = display_genre_chart(books)
        elif choice == "8":
            books = low_stock_alert(books)
        elif choice == "9":
            print("Exiting Book Store Inventory System. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 9.")