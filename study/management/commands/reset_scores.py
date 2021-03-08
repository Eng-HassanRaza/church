from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from leaderboard.leaderboard import Leaderboard

from study.models import CompleteTheVerse, NameTheBook
from study.views import leaderboard_key_for

User = settings.AUTH_USER_MODEL

supported = ['ctv','ntb']
game_model_map = {
    'ctv': CompleteTheVerse,
    'ntb': NameTheBook
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('code')

    def handle(self, *args, **options):
        global supported
        code = options['code']
        if code == '-1':
            to_do = supported
        else:
            if code not in supported:
                raise Exception("Unrecognized code:%s" % code)
            to_do = [code]

        for game in to_do:
            print("\nDeleting all scores for game %s"  % game_model_map[game].__name__)
            model = game_model_map[game]
            model.objects.all().delete()
            lb_score = Leaderboard('%s_sc' % (game,), host=settings.LEADERBOARD_REDIS_HOST)
            lb_time = Leaderboard('%s_tm' % (game,), host=settings.LEADERBOARD_REDIS_HOST)
            lb_score.delete_leaderboard()
            lb_time.delete_leaderboard() 
