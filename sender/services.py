from .models import SendAttempt


class UserStatistic:
    @staticmethod
    def get_user_statistic(user):
        success_sent_attempts = SendAttempt.objects.filter(
            user=user, status="Успешно"
        ).count()

        if not success_sent_attempts:
            success_sent_attempts = 0

        fail_sent_attempts = SendAttempt.objects.filter(
            user=user, status="Не успешно"
        ).count()

        if not fail_sent_attempts:
            fail_sent_attempts = 0
        sent_messages = SendAttempt.objects.filter(user=user).count()

        if not sent_messages:
            sent_messages = 0

        return [success_sent_attempts, fail_sent_attempts, sent_messages]
