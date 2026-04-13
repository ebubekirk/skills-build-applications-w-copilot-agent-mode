from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models


from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        User = get_user_model()
        # Kullanıcıları sil
        User.objects.all().delete()

        # Dinamik modeller
        Team = self.get_or_create_model('teams', ['name'])
        Activity = self.get_or_create_model('activities', ['user', 'activity_type', 'duration'])
        Leaderboard = self.get_or_create_model('leaderboard', ['user', 'score'])
        Workout = self.get_or_create_model('workouts', ['name', 'difficulty'])

        # Koleksiyonları temizle
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Kullanıcılar
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': 'marvel'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'dc'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
        ]
        for u in users:
            User.objects.create_user(username=u['username'], email=u['email'], password='test1234')

        # Takımlar
        marvel = Team.objects.create(name='marvel')
        dc = Team.objects.create(name='dc')

        # Aktiviteler
        Activity.objects.create(user='ironman', activity_type='run', duration='30')
        Activity.objects.create(user='superman', activity_type='swim', duration='45')

        # Liderlik tablosu
        Leaderboard.objects.create(user='ironman', score='100')
        Leaderboard.objects.create(user='superman', score='120')

        # Antrenmanlar
        Workout.objects.create(name='Pushups', difficulty='easy')
        Workout.objects.create(name='Pullups', difficulty='medium')

        self.stdout.write(self.style.SUCCESS('octofit_db test verileri başarıyla yüklendi.'))

    def get_or_create_model(self, name, fields):
        class Meta:
            app_label = 'octofit_tracker'
            managed = False
            db_table = name
        attrs = {'__module__': 'octofit_tracker.models', 'Meta': Meta}
        for f in fields:
            attrs[f] = models.CharField(max_length=255)
        return type(name.capitalize(), (models.Model,), attrs)
