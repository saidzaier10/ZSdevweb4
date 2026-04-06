"""
Commande Django pour attendre que la base de données soit prête.
Utilisée dans les scripts Docker entrypoint.
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Attend que la base de données soit disponible'

    def handle(self, *args, **options):
        self.stdout.write('⏳ Attente de la base de données...')
        db_conn = None
        retries = 0
        max_retries = 30

        while db_conn is None and retries < max_retries:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('✅ Base de données disponible !'))
            except OperationalError:
                retries += 1
                self.stdout.write(f'  → Tentative {retries}/{max_retries}... retry in 2s')
                time.sleep(2)

        if retries >= max_retries:
            self.stderr.write(self.style.ERROR('❌ Impossible de se connecter à la base de données'))
            raise SystemExit(1)
