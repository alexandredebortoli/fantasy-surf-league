from fantasy.models import *
from fantasy.webscraper import (
    scrape_events_schedule,
    scrape_rankings,
    scrape_surfers,
)


def scrape_and_update_data():
    surfers = scrape_surfers()
    for surfer in surfers:
        existing_surfer = Surfer.objects.filter(name=surfer["name"])
        if not existing_surfer:
            new_surfer = Surfer(
                name=surfer["name"],
                headshot_url=surfer["headshot_url"],
                country=surfer["country"],
            )
            new_surfer.save()

    events = scrape_events_schedule()

    for event in events:
        try:
            existing_event = Event.objects.get(name=event["name"])
        except Event.DoesNotExist:
            existing_event = None
        try:
            first_place = Surfer.objects.get(name=event["first_place"])
        except Surfer.DoesNotExist:
            first_place = None
        try:
            second_place = Surfer.objects.get(name=event["second_place"])
        except Surfer.DoesNotExist:
            second_place = None
        if not existing_event:
            new_event = Event(
                name=event["name"],
                location=event["location"],
                start_date=event["start_date"],
                end_date=event["end_date"],
                number=event["number"],
                status=event["status"],
                first_place=first_place,
                second_place=second_place,
            )
            new_event.save()
        elif event["status"] != existing_event.status:
            existing_event.status = event["status"]
            existing_event.first_place = first_place
            existing_event.second_place = second_place
            existing_event.save()

    rankings = scrape_rankings()
    old_rankings = Ranking.objects.all()
    old_rankings.delete()
    for rank in rankings:
        try:
            surfer = Surfer.objects.get(name=rank["name"])
        except:
            surfer = None
        new_rank = Ranking(
            surfer=surfer,
            rank=rank["rank"],
            points=rank["points"],
        )
        new_rank.save()
