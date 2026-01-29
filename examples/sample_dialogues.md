# Sample Dialogues

This file contains example conversations demonstrating the dialogue system's capabilities.

## Example 1: Weather Query

```
Ola Larsson: Welcome to your digital assistant Ola Larsson. How can I help you?
You: What's the weather like in Stockholm tomorrow?
Ola Larsson: Fetching weather for stockholm on tomorrow.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: no
Ola Larsson: Goodbye!
```

## Example 2: Restaurant Search with Booking

```
Ola Larsson: Welcome to your digital assistant Ola Larsson. How can I help you?
You: I want to find a restaurant
Ola Larsson: What location? (e.g., Paris, Tokyo)
You: Gothenburg
Ola Larsson: What cuisine? (e.g., italian, japanese)
You: Italian
Ola Larsson: Searching for italian restaurants near gothenburg.
Ola Larsson: Would you like to make a booking? (yes/no)
You: yes
Ola Larsson: What time would you like the booking?
You: 7 pm
Ola Larsson: Under what name should I make the booking?
You: Harry
Ola Larsson: Booking a table under the name Harry at 7 pm at a italian restaurant near gothenburg.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: no
Ola Larsson: Goodbye!
```

## Example 3: Transit Information

```
Ola Larsson: Welcome to your digital assistant Ola Larsson. How can I help you?
You: When is the next bus in Oslo?
Ola Larsson: What time? (e.g., morning, 3 pm)
You: evening
Ola Larsson: Retrieving transit info for oslo at evening.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: no
Ola Larsson: Goodbye!
```

## Example 4: Multi-Turn Conversation

```
Ola Larsson: Welcome to your digital assistant Ola Larsson. How can I help you?
You: Weather forecast please
Ola Larsson: What location? (e.g., London, Berlin)
You: Copenhagen
Ola Larsson: What date? (e.g., today, friday)
You: today
Ola Larsson: Fetching weather for copenhagen on today.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: yes
Ola Larsson: How can I help you?
You: Find Chinese food near Stockholm
Ola Larsson: Searching for chinese restaurants near stockholm.
Ola Larsson: Would you like to make a booking? (yes/no)
You: no
Ola Larsson: Okay, no booking will be made.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: no
Ola Larsson: Goodbye!
```

## Example 5: Complete Information in First Query

```
Ola Larsson: Welcome to your digital assistant Ola Larsson. How can I help you?
You: What's the weather in Paris tomorrow?
Ola Larsson: Fetching weather for paris on tomorrow.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: Find me Mexican restaurants near Tokyo
Ola Larsson: Searching for mexican restaurants near tokyo.
Ola Larsson: Would you like to make a booking? (yes/no)
You: no
Ola Larsson: Okay, no booking will be made.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: Transit info for Berlin at 6 pm
Ola Larsson: Retrieving transit info for berlin at 6 pm.

Ola Larsson: Is there anything else I can help you with? (yes/no)
You: no
Ola Larsson: Goodbye!
```

## Features Demonstrated

### Demon-Based Extraction
The system automatically extracts slot values from natural language:
- "weather in **Stockholm** **tomorrow**" ’ location=stockholm, date=tomorrow
- "**Chinese** food near **Tokyo**" ’ cuisine=chinese, location=tokyo

### Clarification Questions
When information is missing, targeted questions are asked:
- Missing location: "What location? (e.g., Paris, Tokyo)"
- Missing cuisine: "What cuisine? (e.g., italian, japanese)"

### Multi-Turn Dialogue
The system maintains context across multiple turns and supports continuous conversations.

### Validation with Examples
Invalid inputs trigger helpful error messages with examples from the validation database.
