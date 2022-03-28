from django.shortcuts import render, redirect


def handle_bad_request(request, *args, **kwargs):  # 400
    return render(request, 'error/400.html')


def handle_forbidden(request, *args, **kwargs):  # 403
    return render(request, 'error/403.html')


def handle_page_not_found(request, *args, **kwargs):  # 404
    return render(request, 'error/404.html')


def handle_server_error(request, *args, **kwargs):  # 500
    return render(request, 'error/500.html')
