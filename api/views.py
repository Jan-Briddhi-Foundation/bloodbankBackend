from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import Profile_Serializer, Blood_Request_Serializer, Donation_Criteria_Serializer
from .models import Profile, Blood_Request, Donation_Form
# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def profile(request):
    try:
        profile = Profile.objects.all()
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Profile_Serializer(profile, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def blood_request(request):
    try:
        request_blood = Blood_Request.objects.all()
    except request_blood.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = Blood_Request_Serializer(request_blood, many=True)
    return Response(serializer.data)


@api_view(['GET' , 'POST', 'PUT', 'DELETE'])
def donate(request):
    try:
        donate_blood = Donation_Form.objects.all()
    except donate_blood.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = Donation_Criteria_Serializer(donate_blood, many=True)
    return Response(serializer.data)