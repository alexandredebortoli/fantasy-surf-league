import requests
from bs4 import BeautifulSoup
from datetime import datetime

current_year = "2024"


def scrape_events_schedule():
    url = f"https://www.worldsurfleague.com/events/{current_year}/ct?all=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    event_schedule_data = extract_events_schedule(soup)
    test = []
    for event in event_schedule_data:
        test.append(format_event(event))
    return test


def extract_events_schedule(soup):
    events = []

    event_table_rows = soup.find_all("tr")
    for row in event_table_rows:
        cells = row.find_all("td")
        if len(cells) != 4:
            continue
        events.append(
            {
                "date": cells[0].text.strip(),
                "name": cells[1].find("a").text.strip().split("\n")[0],
                "location": cells[1]
                .find("span", class_="event-schedule-details__location")
                .text.strip(),
                "number": len(events) + 1,
                "status": cells[3].text,
            }
        )
    return events


def format_event(event):
    start_date_str, end_date_str = event["date"].split(" - ")

    start_date = datetime.strptime(
        start_date_str + " " + current_year, "%b %d %Y"
    ).strftime("%Y-%m-%d")

    if end_date_str.isdigit():
        end_date = datetime.strptime(
            start_date_str.split(" ")[0] + " " + end_date_str + " " + current_year,
            "%b %d %Y",
        ).strftime("%Y-%m-%d")
    else:
        end_date = datetime.strptime(
            end_date_str + " " + current_year, "%b %d %Y"
        ).strftime("%Y-%m-%d")

    formatted_event = {
        "start_date": format_date_str_month_day(start_date),
        "end_date": format_date_str_month_day(end_date),
        "name": event["name"],
        "location": event["location"],
        "number": event["number"],
        "status": event["status"],
    }

    return formatted_event


def format_date_str_month_day(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")
