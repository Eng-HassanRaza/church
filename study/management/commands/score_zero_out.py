from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from leaderboard.leaderboard import Leaderboard

from main.models import User
from study.models import CompleteTheVerse, NameTheBook
from study.views import leaderboard_key_for

supported = ['ctv','ntb']
game_model_map = {
    'ctv': CompleteTheVerse,
    'ntb': NameTheBook
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('code')
        parser.add_argument('field')
        parser.add_argument('user_pk')

    def handle(self, *args, **options):
        global supported
        code = options['code']
        field = options['field']
        user_pk = options['user_pk']
        user = User.objects.get(pk=user_pk)
        lb_key = leaderboard_key_for(user)

        print("\nZeroing scores for game %s for field %s for user %s"  % (game_model_map[code].__name__, field, user_pk))
        model = game_model_map[code]
        if field == 'sc':
            lb_score = Leaderboard('%s_sc' % (code,), host=settings.LEADERBOARD_REDIS_HOST)
            model.objects.filter(user=user).update(stat_score=0)
            lb_score.rank_member(lb_key, 0)
        elif field == 'tm':
            lb_time = Leaderboard('%s_tm' % (code,), host=settings.LEADERBOARD_REDIS_HOST)
            model.objects.filter(user=user).update(stat_time_secs=0)
            lb_time.rank_member(lb_key, 0)
