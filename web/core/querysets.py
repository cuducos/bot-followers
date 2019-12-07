from django.db.models import Count, QuerySet


class JobQuerySet(QuerySet):
    def analyzed_followers(self):
        return self.filter(followers__botometer__isnull=False)

    def report(self):
        kwargs = {"analyzed_followers_count": Count("followers")}
        qs = self.analyzed_followers().annotate(**kwargs)
        return qs.filter(total_followers__gt=0, analyzed_followers_count__gt=0)


class AccountQuerySet(QuerySet):
    def analyzed(self):
        return self.filter(botometer__isnull=False)
