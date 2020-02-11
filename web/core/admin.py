from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from web.core.models import Job


def cell(data, detail):
    return mark_safe(f"{data}<br><small>{detail}</small>")


def humanized_percent(number, decimals=2):
    if number is None:
        return ""

    result = round(number * 100, decimals) if decimals else round(number * 100)
    return f"{result}%"


def report(percent, error):
    humanized_error = "" if error is None else f"±{humanized_percent(error)}"
    return cell(humanized_percent(percent), humanized_error)


class JobModelAdmin(admin.ModelAdmin):

    list_display = (
        "formatted_screen_name",
        "analyzed",
        "over50",
        "over75",
        "over80",
        "over90",
        "over95",
        "status",
    )

    def formatted_screen_name(self, job):
        user = f'<a href="https://twitter.com/{job.screen_name}">@{job.screen_name}</a>'
        followers = f"{job.total_followers:,} followers" if job.total_followers else ""
        return cell(user, followers)

    formatted_screen_name.short_description = "Twitter account"

    def analyzed(self, job):
        count, percent = job.followers.analyzed().count(), humanized_percent(0)
        if job.total_followers:
            percent = humanized_percent(count / job.total_followers)
        return cell(count, percent)

    analyzed.short_description = "Followers analyzed"

    def over50(self, job):
        return job.percent_over(0.5, over_or_equal=False, wrapper=report)

    over50.short_description = "+50% Botometer"

    def over75(self, job):
        return job.percent_over(0.75, wrapper=report)

    over75.short_description = "+75% Botometer"

    def over80(self, job):
        return job.percent_over(0.8, wrapper=report)

    over80.short_description = "+80% Botometer"

    def over90(self, job):
        return job.percent_over(0.9, wrapper=report)

    over90.short_description = "+90% Botometer"

    def over95(self, job):
        return job.percent_over(0.9, wrapper=report)

    over95.short_description = "+95% Botometer"

    def status(self, job):
        return render_to_string("core/job_action_form.html", {"job": job})

    status.short_description = "Actions"


admin.site.register(Job, JobModelAdmin)
admin.site.site_header = "Bot Follower"
admin.site.site_title = "Bot Follower dashboard"
admin.site.index_title = "Welcome to Bot Follower dashboard"
