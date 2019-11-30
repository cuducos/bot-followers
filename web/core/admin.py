from django.contrib import admin
from django.utils.safestring import mark_safe

from bot_followers import humanized_percent
from web.core.models import Job


def cell(data, detail):
    return mark_safe(f"{data}<br><small>{detail}</small>")


class JobModelAdmin(admin.ModelAdmin):

    list_display = (
        "formatted_screen_name",
        "analyzed",
        "over50",
        "over75",
        "over80",
        "over90",
        "over95",
    )

    def formatted_screen_name(self, job):
        user = f'<a href="https://twitter.com/{job.screen_name}">@{job.screen_name}</a>'
        followers = f"{job.total_followers:,} followers"
        return cell(user, followers)

    formatted_screen_name.short_description = "Twitter account"

    def analyzed(self, job):
        count = job.total()
        percent = humanized_percent(job.total() / job.total_followers)
        return cell(count, percent)

    analyzed.short_description = "Followes analyzed"

    def _over(self, job, threshold):
        percent, error = (humanized_percent(n) for n in job.percent_over(threshold))
        return cell(percent, f"±{error}")

    def over50(self, job):
        return self._over(job, 0.5)

    over50.short_description = "+50% Botometer"

    def over75(self, job):
        return self._over(job, 0.75)

    over75.short_description = "+75% Botometer"

    def over80(self, job):
        return self._over(job, 0.8)

    over80.short_description = "+80% Botometer"

    def over90(self, job):
        return self._over(job, 0.9)

    over90.short_description = "+90% Botometer"

    def over95(self, job):
        return self._over(job, 0.95)

    over95.short_description = "+95% Botometer"


admin.site.register(Job, JobModelAdmin)
admin.site.site_header = "Bot Follower"
admin.site.site_title = "Bot Follower dashboard"
admin.site.index_title = "Welcome to Bot Follower dashboard"
