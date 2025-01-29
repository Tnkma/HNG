""" This file is used to create views for the MyInfo app. """
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import pytz

class MyInfo(APIView):
    """ Hardedcoded information about me."""
    def get(self, request):
        """ Returns information about me."""
        data = {
            "email": "onwusilikenonso@gmail.com",
            "current_datetime": datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "github_url": "https://github.com/Tnkma/HNG/tree/main/HNGIntern/stage0/BasicInfo"
        }
        return Response(data)
