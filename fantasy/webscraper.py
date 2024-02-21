import requests
from bs4 import BeautifulSoup
from datetime import datetime

current_year = "2024"


def scrape_events_schedule():
    events_url = f"https://www.worldsurfleague.com/events/{current_year}/ct?all=1"
    event_ranking_url = (
        f"https://www.worldsurfleague.com/athletes/tour/mct?year={current_year}"
    )
    response = requests.get(events_url)
    soup = BeautifulSoup(response.text, "html.parser")

    event_schedule_data = extract_events_schedule(soup)

    response = requests.get(event_ranking_url)
    soup = BeautifulSoup(response.text, "html.parser")

    events_ranking_data = extract_events_champion(soup)

    test = []
    for event in event_schedule_data:
        test.append(format_event(event, events_ranking_data))
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


def format_event(event, events_ranking):
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

    if event["status"] == "Completed":
        formatted_event["first_place"] = events_ranking[str(event["number"])][
            "first_place"
        ]
        formatted_event["second_place"] = events_ranking[str(event["number"])][
            "second_place"
        ]

    return formatted_event


def format_date_str_month_day(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")


def extract_events_champion(soup):
    events_champions = {
        "1": {},
        "2": {},
        "3": {},
        "4": {},
        "5": {},
        "6": {},
        "7": {},
        "8": {},
        "9": {},
        "10": {},
    }

    event_table_body = soup.find("tbody")
    event_table_rows = event_table_body.find_all("tr")
    for row in event_table_rows:
        athlete_headshot_url = row.find("a", class_="headshot proxy-img")
        if athlete_headshot_url:
            athlete_headshot_url = athlete_headshot_url["data-img-src"]
        athlete_name = row.find("a", class_="athlete-name")
        if athlete_name:
            athlete_name = athlete_name.text
        athlete_country = row.find("span", class_="athlete-country-name")
        if athlete_country:
            athlete_country = athlete_country.text
        athlete = {
            "name": athlete_name,
            "country": athlete_country,
            "headshot_url": athlete_headshot_url,
        }

        placements = row.find_all("td", class_="athlete-event-place")
        for index, placement in enumerate(placements):
            if placement.text.strip() == "10,000":
                events_champions[str(index + 1)]["first_place"] = athlete
            elif placement.text.strip() == "7,800":
                events_champions[str(index + 1)]["second_place"] = athlete

    return events_champions


def scrape_rankings():
    rankings_url = f"https://www.worldsurfleague.com/athletes/rankings"
    response = requests.get(rankings_url)
    soup = BeautifulSoup(response.text, "html.parser")

    rankings_data = extract_rankings(soup)

    return rankings_data


def extract_rankings(soup):
    rankings = []

    rankings_ul = soup.find("ul", class_="athletes-tour-athletes")
    rankings_li = rankings_ul.find_all("li")
    for row in rankings_li:
        athlete_rank = row.find("span", class_="athlete-rank")
        if athlete_rank:
            athlete_rank = athlete_rank.text.strip()
        athlete_points = row.find("span", class_="athlete-points")
        if athlete_points:
            athlete_points = athlete_points.text.strip()
        athlete_avatar = row.find("span", class_="athlete-avatar")
        athlete_name = None
        athlete_headshot_url = None
        athlete_country = None
        if athlete_avatar:
            athlete_name = athlete_avatar.find("a", class_="athlete-name")
            if athlete_name:
                athlete_name = athlete_name.text.strip()
            athlete_country = athlete_avatar.find("span", class_="athlete-country-name")
            if athlete_country:
                athlete_country = athlete_country.text.strip()
            athlete_headshot_url = athlete_avatar.find("a", class_="headshot proxy-img")
            if athlete_headshot_url:
                athlete_headshot_url = athlete_headshot_url["data-img-src"]

        athlete = {
            "rank": athlete_rank,
            "name": athlete_name,
            "headshot_url": athlete_headshot_url,
            "country": athlete_country,
            "points": athlete_points,
        }
        rankings.append(athlete)
    return rankings


if __name__ == "__main__":
    print(scrape_rankings())
