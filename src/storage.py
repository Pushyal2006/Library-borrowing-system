
import json
import os


DATA_FILE = os.path.join("data", "library_data.json")


def empty_data():
    return {
        "members": [],
        "resources": [],
        "loans": []
    }


def load_data():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        data = empty_data()
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid data format.")

        for key in ("members", "resources", "loans"):
            if key not in data or not isinstance(data[key], list):
                raise ValueError(f"Missing or invalid '{key}' data.")

        return data

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error loading data: {error}")
        return empty_data()


def save_data(data):
    os.makedirs("data", exist_ok=True)

    temp_file = DATA_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_file, DATA_FILE)

    except OSError as error:
        print(f"Error saving data: {error}")

        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
