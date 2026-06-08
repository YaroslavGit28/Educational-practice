from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'internet_magazin',
        'version': '0.1.1',
    })
