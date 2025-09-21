from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    help = "Комманды для взаимодействия S3 хранилищем"

    def handle(self, *args: Any, **options: Any) -> str | None:
        pass
