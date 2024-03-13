from apps.stt.models.team import Team
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Updates teams with automatiq_credentials_website_id from a JSON file"

    def handle(self, *args, **kwargs):
        with open("seatscouts.json", "r") as file:
            data = json.load(file)
            for item in data:
                try:
                    team = Team.objects.get(
                        league=item["league"], name=item["description"]
                    )
                    team.automatiq_credentials_website_id = item["id"]
                    team.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully updated {team.name}")
                    )
                except Team.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Team not found for {item["league"]}, {item["description"]}'
                        )
                    )
                except Team.MultipleObjectsReturned:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Multiple teams found for {item["league"]}, {item["description"]} - manual review needed'
                        )
                    )
