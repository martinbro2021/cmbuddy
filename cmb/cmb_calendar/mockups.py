import random
from datetime import date, time, timedelta

MENU_ENTRY_MOCKUP = {
    "Calendar":
    {
        "position": 15,
        "name": "Calendar",
        "url": "/calendar",
    }
}

SNIPPET_MOCKUP = {
    "calendar_title": "Calendar",
    "calendar_no_entries": "No calendar entries"
}


LINKS = ("Tickets", "Further information", "Read more")

CITIES = ("Berlin", "Frankfurt", "London", "New York", "Paris", "Lyon", "Prague", "Kopenhagen", "Amsterdam")

LOCATIONS = ("Theatre", "Opera", "Concert Hall", "Guildhall", "Arts Center")


LOREM_IPSUM = """ lorem ipsum dolor sit amet, consetetur sadipscing elitr,
sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""

TIMES = (time(20, 0), time(19, 30), time(19, 0), time(18, 30), time(18, 0), time(17, 30), time(17, 0), time(11))


rnd = random.Random(0)
today = date.today()

CALENDAR_ENTRY_MOCKUP = {
    index: {
        "date": today + timedelta(rnd.randint(-500, 350)),
        "time": rnd.choice(TIMES),
        "html": LOREM_IPSUM
    }
    for index in range(100)
}
