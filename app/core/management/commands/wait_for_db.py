"""
Django command for DB to be available
"""
import time

from psycopg2 import OperationalError as psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for DB connection"""

    def handle(self, *args, **options):
        self.stdout.write("Waitig for DB....")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2Error, OperationalError):
                self.stdout.write('DB is unavailable...!')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('DB is UP'))
