from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, resolve_url

from web.core import tasks
from web.core.forms import ScreenNameForm
from web.core.models import Job


def home(request):
    return redirect(resolve_url(settings.ROOT_REDIRECTS_TO))


def screen_name_view(action):
    def view(request):
        if not request.user.is_authenticated:
            login_url = resolve_url("admin:login")
            msg = f"User not authenticated. Please, login at {login_url}"
            return JsonResponse({"error": msg}, status=403)

        if request.method != "POST":
            return HttpResponseNotAllowed(("POST",))

        form = ScreenNameForm(request.POST)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)

        message = action(form.cleaned_data["screen_name"])
        messages.info(request, message)
        return redirect(resolve_url(settings.ROOT_REDIRECTS_TO))

    return view


@screen_name_view
def start(screen_name):
    data = {"screen_name": screen_name}
    job, _ = Job.objects.get_or_create(**data, defaults=data)
    task = tasks.start.delay(job.pk)
    job.save_task(task.id)
    return f"Done! Soon @{screen_name}'s followers will be checked using Botometer."


@screen_name_view
def pause(screen_name):
    try:
        job = Job.objects.get(screen_name=screen_name)
    except Job.DoesNotExist:
        pass
    else:
        tasks.pause.delay(job.pk)
        job.save_task(None)

    return f"Ok, soon Botometer will stop to check @{screen_name}'s followers."
