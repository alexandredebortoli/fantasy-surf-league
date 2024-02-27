from datetime import date
from fantasy.models import Event
from fantasy.task import scrape_and_update_data


class ScrapeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        events_ended = (
            Event.objects.exclude(status="Completed")
            .filter(end_date__lt=date.today())
            .order_by("number")
        )

        events_started = (
            Event.objects.exclude(status__in=["Completed", "Live"])
            .filter(start_date__lt=date.today())
            .order_by("number")
        )

        empty_events = not Event.objects.exists()

        if empty_events or events_ended.exists() or events_started.exists():
            print("Scraping data...")
            scrape_and_update_data()
            print("Data scraped!")

        response = self.get_response(request)

        return response
