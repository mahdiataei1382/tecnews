from django.core.management.base import BaseCommand
from tecnews.scraper import main_scraper

class Command(BaseCommand):
    help = 'Scrape news from the website and save to the database'

    def handle(self, *args, **kwargs):
        main_scraper()
