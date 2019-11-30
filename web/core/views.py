from django.shortcuts import redirect, resolve_url


def home(request):
    return redirect(resolve_url("admin:core_job_changelist"))
