from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request,'Reconciliation_app/index.html')


@csrf_protect
@api_view(['POST'])
def reconciliation(request):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    print(startDate,endDate)
    return HttpResponse(f'{startDate},{endDate}')
