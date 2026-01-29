import json
import random
import re

# Load valid values from the JSON file.
with open("data/valid_values.json", "r") as f:
    valid_data = json.load(f)

# Convert valid values to lowercase for case-insensitive matching.
valid_locations = [loc.lower() for loc in valid_data["locations"]]
valid_cuisines = [cuisine.lower() for cuisine in valid_data["cuisines"]]
valid_dates = [date.lower() for date in valid_data["dates"]]
valid_times = [time.lower() for time in valid_data["times"]]

chat_bot_name = "Ola Larsson"

KEYWORDS = {
    "weather": ["weather", "forecast", "temperature"],
    "restaurant": ["restaurant", "food", "eat", "dinner", "lunch", "cuisine"],
    "transit": ["bus", "tram", "transit", "train", "metro"]
}

FRAME_CONFIG = {
    "weather": ("Weather", ["location", "date"]),
    "restaurant": ("Restaurant", ["location", "cuisine"]),
    "transit": ("Transit", ["location", "time"]),
}

SLOT_QUESTIONS = {
    "location": "What location? (e.g., " + ", ".join(random.sample(valid_data["locations"], 2)) + ")",
    "date": "What date? (e.g., " + ", ".join(random.sample(valid_data["dates"], 2)) + ")",
    "time": "What time? (e.g., " + ", ".join(random.sample(valid_data["times"], 2)) + ")",
    "cuisine": "What cuisine? (e.g., " + ", ".join(random.sample(valid_data["cuisines"], 2)) + ")"
}


def validate_location(location):
    return location.lower() in valid_locations

def validate_cuisine(cuisine):
    return cuisine.lower() in valid_cuisines

def validate_date(date):
    return date.lower() in valid_dates

def validate_time(time):
    return time.lower() in valid_times

# Validators dictionary: maps slot names to (validation function, lambda returning random examples).
validators = {
    "location": (validate_location, lambda: ", ".join(random.sample(valid_data["locations"], 2))),
    "cuisine": (validate_cuisine, lambda: ", ".join(random.sample(valid_data["cuisines"], 2))),
    "date": (validate_date, lambda: ", ".join(random.sample(valid_data["dates"], 2))),
    "time": (validate_time, lambda: ", ".join(random.sample(valid_data["times"], 2)))
}


class Frame:
    def __init__(self, name, slots):
        self.name = name
        self.slots = {slot: None for slot in slots}

    def fill_slot(self, slot, value):
        if slot in self.slots and value:
            self.slots[slot] = value.strip().lower()  # store as lowercase

    def is_complete(self):
        return all(value is not None for value in self.slots.values())

    def missing_slots(self):
        return [slot for slot, value in self.slots.items() if value is None]


def create_frame(frame_type):
    config = FRAME_CONFIG[frame_type]
    return Frame(config[0], config[1])


# Determine which frame to use based on keywords.
def select_frame(user_input):
    text = user_input.lower()
    for key, keywords in KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return key
    return None


# Generic function to extract the first valid value for any slot.
def extract_first_valid_value(user_input, slot):
    valid_map = {
        "location": valid_locations,
        "cuisine": valid_cuisines,
        "date": valid_dates,
        "time": valid_times
    }
    user_input_lower = user_input.lower()
    for candidate in valid_map.get(slot, []):
        if re.search(r'\b' + re.escape(candidate) + r'\b', user_input_lower):
            return candidate
    return None


# Update current frame with new info from input using the generic extractor.
def update_frame(user_input, current_frame):
    if current_frame.name == "Weather":
        if current_frame.slots["location"] is None:
            candidate = extract_first_valid_value(user_input, "location")
            if candidate:
                current_frame.fill_slot("location", candidate)
        if current_frame.slots["date"] is None:
            candidate = extract_first_valid_value(user_input, "date")
            if candidate:
                current_frame.fill_slot("date", candidate)
    elif current_frame.name == "Restaurant":
        if current_frame.slots["location"] is None:
            candidate = extract_first_valid_value(user_input, "location")
            if candidate:
                current_frame.fill_slot("location", candidate)
        if current_frame.slots["cuisine"] is None:
            candidate = extract_first_valid_value(user_input, "cuisine")
            if candidate:
                current_frame.fill_slot("cuisine", candidate)
    elif current_frame.name == "Transit":
        if current_frame.slots["location"] is None:
            candidate = extract_first_valid_value(user_input, "location")
            if candidate:
                current_frame.fill_slot("location", candidate)
        if current_frame.slots["time"] is None:
            candidate = extract_first_valid_value(user_input, "time")
            if candidate:
                current_frame.fill_slot("time", candidate)
    return current_frame


# Ask for missing slot information.
def ask_for_missing_info(current_frame):
    missing = current_frame.missing_slots()
    if missing:
        slot = missing[0]
        question = SLOT_QUESTIONS[slot]
        return question, slot
    return None, None


# Generic function to fill missing slots.
def fill_missing_slots(current_frame, valid_data, validators):
    first_time = True
    while not current_frame.is_complete():
        question, slot = ask_for_missing_info(current_frame)
        if question:
            if first_time:
                print(f"{chat_bot_name}: {question}")
            user_response = input("You: ")
            # Use generic extraction on the user's response.
            candidate = extract_first_valid_value(user_response, slot)
            if candidate is None or not validators[slot][0](candidate):
                examples = validators[slot][1]()
                print(f"{chat_bot_name}: I didn't recognize that {slot}. Please provide a valid {slot} (e.g., {examples}).")
                first_time = False
                continue
            # Use the extracted candidate for filling the slot.
            current_frame.fill_slot(slot, candidate)
            current_frame = update_frame(user_response, current_frame)
            first_time = True
    return current_frame


def main():
    first_time = True
    while True:
        if first_time:
            print(f"{chat_bot_name}: Welcome to your digital assistant {chat_bot_name}. How can I help you?")
        else:
            print(f"{chat_bot_name}: How can I help you?")

        frame_key = None
        while frame_key is None:
            initial_input = input("You: ")
            frame_key = select_frame(initial_input)
            if frame_key is None:
                print(f"{chat_bot_name}: I'm sorry, I couldn't determine your request. Please mention weather, restaurant, or transit.")

        current_frame = create_frame(frame_key)
        current_frame = update_frame(initial_input, current_frame)
        current_frame = fill_missing_slots(current_frame, valid_data, validators)

        if current_frame.name == "Weather":
            print(f"{chat_bot_name}: Fetching weather for {current_frame.slots['location']} on {current_frame.slots['date']}.")
        elif current_frame.name == "Restaurant":
            print(f"{chat_bot_name}: Searching for {current_frame.slots['cuisine']} restaurants near {current_frame.slots['location']}.")
        elif current_frame.name == "Transit":
            print(f"{chat_bot_name}: Retrieving transit info for {current_frame.slots['location']} at {current_frame.slots['time']}.")

        print(f"{chat_bot_name}: Is there anything else I can help you with? (yes/no)")
        answer = input("You: ").strip().lower()
        if answer not in ["yes", "y"]:
            print(f"{chat_bot_name}: Goodbye!")
            break

        first_time = False

if __name__ == "__main__":
    main()
