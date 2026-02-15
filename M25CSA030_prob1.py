import re
from datetime import date

# this function calculate age from given birth date
# it checks if birthday already came or not in current year
def calculate_age(year, month, day):
    today = date.today()
    age = today.year - year

    # if birthday is not yet occured this year then minus 1
    if (today.month, today.day) < (month, day):
        age -= 1

    return age


# this function try to understand birthday in different formats
# like dd-mm-yyyy, mm-dd-yy, dd month yyyy etc
def parse_birthday(text):
    text = text.strip().lower()

    # format like mm-dd-yy or mm/dd/yyyy
    m = re.match(r'(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})', text)
    if m:
        month, day, year = map(int, m.groups())

        # if year is given in 2 digit then assume 2000+
        if year < 100:
            year += 2000

        return year, month, day

    # format like dd mm yyyy or dd-mm-yyyy
    m = re.match(r'(\d{1,2})[ -](\d{1,2})[ -](\d{4})', text)
    if m:
        day, month, year = map(int, m.groups())
        return year, month, day

    # format like 12 august 2002 or 12 aug 2002
    m = re.match(r'(\d{1,2})\s*([a-zA-Z]+)\s*(\d{4})', text)
    if m:
        day = int(m.group(1))
        month_str = m.group(2)
        year = int(m.group(3))

        # mapping month name to number
        months = {
            "jan":1,"january":1,"feb":2,"february":2,"mar":3,"march":3,
            "apr":4,"april":4,"may":5,"jun":6,"june":6,"jul":7,"july":7,
            "aug":8,"august":8,"sep":9,"september":9,"oct":10,"october":10,
            "nov":11,"november":11,"dec":12,"december":12
        }

        # taking first 3 letters of month
        month = months.get(month_str[:3])
        if month:
            return year, month, day

    # if nothing matched then return none
    return None


# this function detect mood from user input using regex
# it also handle some small spelling mistakes
def respond_to_mood(text):
    text = text.lower()

    # happy mood
    if re.search(r'hap+y|good|great|awesom|excite', text):
        return "That'Good Be Happy!"

    # sad mood
    if re.search(r'sad+|down|low|depress', text):
        return "I'm sorry to hear that."

    # angry mood
    if re.search(r'ang+ry|mad|annoy', text):
        return "Take a deep breath. Things will be soften."

    # normal mood
    if re.search(r'ok+|fine|normal', text):
        return "Got it! "

    # if mood not matched
    return "Hmm, I couldn't clearly understand your mood."


# this function detect surname from full name
# it simply take last word as surname
def detect_surname(name):
    parts = re.split(r'\s+', name.strip())
    if len(parts) >= 2:
        return parts[-1]
    return None


# main chatbot function
def run_chatbot():

    print("Chatbot: Hello! What's your full name?")
    name = input("You: ")

    # detect surname from name
    surname = detect_surname(name)

    if surname:
        print(f"Chatbot: Nice to meet you, Mr/Ms {surname}.")
    else:
        print("Chatbot: Nice to meet you!")

    # asking birthday
    print("Chatbot: When is your birthday?")
    bday_input = input("You: ")

    parsed = parse_birthday(bday_input)

    # if birthday is correctly parsed then calculate age
    if parsed:
        year, month, day = parsed
        age = calculate_age(year, month, day)
        print(f"Chatbot: You are {age} years old.")
    else:
        print("Chatbot: Sorry, I couldn't understand your birthday format.")

    # asking mood
    print("Chatbot: How are you feeling today?")
    mood = input("You: ")

    # responding according to mood
    print("Chatbot:", respond_to_mood(mood))


# program start from here
if __name__ == "__main__":
    run_chatbot()
