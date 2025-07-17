import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def fetch_events():
    url = "https://www.hbs.edu/recruiting/hire-talent/policies-and-dates/Pages/recruiting-calendars.aspx?view=calendar"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    for li in soup.find_all("li"):
        text = li.get_text(separator=" ", strip=True)
        match = re.search(r"([A-Za-z]+\s\d{1,2},\s\d{4})", text)
        if match:
            try:
                date = datetime.strptime(match.group(1), "%B %d, %Y").strftime("%Y%m%d")
                title = text.replace(match.group(1), "").strip(" –:-")
                events.append((title, date))
            except:
                pass
    return events

def build_ics(events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "PRODID:-//HBS Recruiting Calendar//EN"
    ]
    for title, date in events:
        lines += [
            "BEGIN:VEVENT",
            f"SUMMARY:{title}",
            f"DTSTART;VALUE=DATE:{date}",
            f"DTEND;VALUE=DATE:{date}",
            "END:VEVENT"
        ]
    lines.append("END:VCALENDAR")
    with open("hbs_recruiting.ics", "w") as f:
        f.write("\n".join(lines))
    print("✅ 生成成功：hbs_recruiting.ics")

events = fetch_events()
build_ics(events)
