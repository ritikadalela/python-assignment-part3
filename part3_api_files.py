# Assignment - Part 3: File I/O, APIs & Exception Handling
# Theme: Product Explorer & Error-Resilient Logger

from datetime import datetime
import requests


BASE_URL = "https://dummyjson.com/products"


def log_error(function_name, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n"
    with open("error_log.txt", "a", encoding="utf-8") as file:
        file.write(log_line)


# ----------------------------
# Task 1 - File Read & Write Basics
# ----------------------------

def task_1():
    print("\nTASK 1 - FILE READ & WRITE BASICS")
    print("-" * 60)

    notes = [
        "Topic 1: Variables store data. Python is dynamically typed.\n",
        "Topic 2: Lists are ordered and mutable.\n",
        "Topic 3: Dictionaries store key-value pairs.\n",
        "Topic 4: Loops automate repetitive tasks.\n",
        "Topic 5: Exception handling prevents crashes.\n",
    ]

    with open("python_notes.txt", "w", encoding="utf-8") as file:
        file.writelines(notes)
    print("File written successfully.")

    extra_lines = [
        "Topic 6: Functions help reuse code and improve readability.\n",
        "Topic 7: APIs allow programs to communicate over the internet.\n",
    ]

    with open("python_notes.txt", "a", encoding="utf-8") as file:
        file.writelines(extra_lines)
    print("Lines appended.")

    with open("python_notes.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    print("\nContents of python_notes.txt:")
    for index, line in enumerate(lines, start=1):
        print(f"{index}. {line.strip()}")

    print(f"\nTotal number of lines: {len(lines)}")

    keyword = input("\nEnter a keyword to search in the notes: ").strip().lower()

    matches = []
    for line in lines:
        if keyword in line.lower():
            matches.append(line.strip())

    if matches:
        print("\nMatching lines:")
        for match in matches:
            print(match)
    else:
        print("No lines matched that keyword.")


# ----------------------------
# Task 2 - API Integration
# ----------------------------

def safe_get(url, function_name):
    try:
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.ConnectionError as e:
        print("Connection failed. Please check your internet.")
        log_error(function_name, "ConnectionError", str(e))
    except requests.exceptions.Timeout as e:
        print("Request timed out. Try again later.")
        log_error(function_name, "Timeout", str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error(function_name, type(e).__name__, str(e))
    return None


def safe_post(url, payload, function_name):
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response
    except requests.exceptions.ConnectionError as e:
        print("Connection failed. Please check your internet.")
        log_error(function_name, "ConnectionError", str(e))
    except requests.exceptions.Timeout as e:
        print("Request timed out. Try again later.")
        log_error(function_name, "Timeout", str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error(function_name, type(e).__name__, str(e))
    return None


def fetch_products():
    print("\nStep 1 - Fetch and Display Products")
    response = safe_get(f"{BASE_URL}?limit=20", "fetch_products")

    if response is None:
        return []

    if response.status_code != 200:
        print(f"Failed to fetch products. Status code: {response.status_code}")
        log_error("fetch_products", "HTTPError", f"Status code {response.status_code}")
        return []

    data = response.json()
    products = data.get("products", [])

    print(f"\n{'ID':<4}| {'Title':<30}| {'Category':<15}| {'Price':<10}| {'Rating'}")
    print("-" * 78)
    for product in products:
        print(
            f"{product['id']:<4}| "
            f"{product['title'][:29]:<30}| "
            f"{product['category'][:14]:<15}| "
            f"${product['price']:<9}| "
            f"{product['rating']}"
        )

    return products


def filter_and_sort_products(products):
    print("\nStep 2 - Filter and Sort")
    filtered = []

    for product in products:
        if product["rating"] >= 4.5:
            filtered.append(product)

    filtered.sort(key=lambda item: item["price"], reverse=True)

    if not filtered:
        print("No products found with rating >= 4.5")
        return

    print(f"\n{'ID':<4}| {'Title':<30}| {'Price':<10}| {'Rating'}")
    print("-" * 60)
    for product in filtered:
        print(
            f"{product['id']:<4}| "
            f"{product['title'][:29]:<30}| "
            f"${product['price']:<9}| "
            f"{product['rating']}"
        )


def fetch_laptops():
    print("\nStep 3 - Search by Category (laptops)")
    response = safe_get(f"{BASE_URL}/category/laptops", "fetch_laptops")

    if response is None:
        return

    if response.status_code != 200:
        print(f"Failed to fetch laptops. Status code: {response.status_code}")
        log_error("fetch_laptops", "HTTPError", f"Status code {response.status_code}")
        return

    data = response.json()
    products = data.get("products", [])

    if not products:
        print("No laptops found.")
        return

    for product in products:
        print(f"{product['title']} - ${product['price']}")


def create_product():
    print("\nStep 4 - POST Request (Simulated)")
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    response = safe_post(f"{BASE_URL}/add", payload, "create_product")

    if response is None:
        return

    if response.status_code not in (200, 201):
        print(f"POST request failed. Status code: {response.status_code}")
        log_error("create_product", "HTTPError", f"Status code {response.status_code}")
        return

    print("Response from server:")
    print(response.json())


# ----------------------------
# Task 3 - Exception Handling
# ----------------------------

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")


def test_exception_handling():
    print("\nTASK 3 - EXCEPTION HANDLING")
    print("-" * 60)

    print("\nPart A - Guarded Calculator")
    print("safe_divide(10, 2)    =", safe_divide(10, 2))
    print("safe_divide(10, 0)    =", safe_divide(10, 0))
    print("safe_divide('ten', 2) =", safe_divide("ten", 2))

    print("\nPart B - Guarded File Reader")
    print("\nReading python_notes.txt:")
    content_1 = read_file_safe("python_notes.txt")
    if content_1 is not None:
        print(content_1)

    print("Reading ghost_file.txt:")
    content_2 = read_file_safe("ghost_file.txt")
    if content_2 is not None:
        print(content_2)


def product_lookup_loop():
    print("\nPart D - Input Validation Loop")
    while True:
        user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()

        if user_input.lower() == "quit":
            print("Exiting product lookup.")
            break

        if not user_input.isdigit():
            print("Warning: Please enter a valid integer.")
            continue

        product_id = int(user_input)

        if product_id < 1 or product_id > 100:
            print("Warning: Product ID must be between 1 and 100.")
            continue

        response = safe_get(f"{BASE_URL}/{product_id}", "lookup_product")

        if response is None:
            continue

        if response.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        elif response.status_code == 200:
            product = response.json()
            print(f"Title: {product['title']}")
            print(f"Price: ${product['price']}")
        else:
            print(f"Unexpected status code: {response.status_code}")
            log_error("lookup_product", "HTTPError", f"Status code {response.status_code} for product ID {product_id}")


def robust_api_demo():
    print("\nTASK 2 - API INTEGRATION")
    print("-" * 60)

    products = fetch_products()
    filter_and_sort_products(products)
    fetch_laptops()
    create_product()


# ----------------------------
# Task 4 - Logging to File
# ----------------------------

def trigger_log_examples():
    print("\nTASK 4 - LOGGING TO FILE")
    print("-" * 60)

    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except requests.exceptions.ConnectionError as e:
        print("Intentionally triggered ConnectionError for logging.")
        log_error("fetch_products", "ConnectionError", str(e))
    except requests.exceptions.Timeout as e:
        print("Intentionally triggered Timeout for logging.")
        log_error("fetch_products", "Timeout", str(e))
    except Exception as e:
        print(f"Unexpected error during forced logging test: {e}")
        log_error("fetch_products", type(e).__name__, str(e))

    response = safe_get(f"{BASE_URL}/999", "lookup_product")
    if response is not None and response.status_code != 200:
        print("Intentionally triggered HTTP error log for missing product.")
        log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")

    print("\nContents of error_log.txt:")
    try:
        with open("error_log.txt", "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("error_log.txt does not exist yet.")


def main():
    task_1()
    robust_api_demo()
    test_exception_handling()
    product_lookup_loop()
    trigger_log_examples()


if __name__ == "__main__":
    main()
