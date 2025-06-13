from users.models import CustomUser
from .models import SendAttempt, MailingList

class UserStatistic:
    @staticmethod
    def get_user_statistic(user):
        try:
            success_sent_attempts = SendAttempt.objects.filter(user=user, status='Успешно').count()
        except:
            success_sent_attempts = 0

        try:
            fail_sent_attempts = SendAttempt.objects.filter(user=user, status='Не успешно').count()
        except:
            fail_sent_attempts = 0
        try:
            sent_messages = SendAttempt.objects.filter(user=user).count()
        except:
            sent_messages = 0
        return [success_sent_attempts, fail_sent_attempts, sent_messages]