from datetime import datetime,timedelta
from django.http import JsonResponse
from django.utils import timezone
from .models import Users, SportList, favSports, brodacastMessages
from .serializers import UsersSerializer, SportListSerializer, favSportsSerializer, BrodcastMessagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from hashlib import md5
import jwt 

class createUserAPIView(APIView):
    def get(self,request):
        user = Users.objects.all()
        serializer = UsersSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def post(self,request,*args, **kwargs):
        serialized = UsersSerializer(data=request.data)
        serialized.is_valid()
        if(serialized.is_valid()):
            password = serialized.validated_data['password']
            hashpass = md5(password.encode('utf8')).hexdigest()
            serialized.validated_data['password'] = hashpass
            serialized.save()
            response_data = {
                "message": "User Created. Please Log in!",
                "results": {
                },
                "success": True
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": serialized.errors,
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
      

class AuthenticateUserAPIView(APIView):
    def post(self,request,*args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            hashpass = md5(password.encode('utf8')).hexdigest()
            password = hashpass
            if '@' in username:
                try:
                    user = Users.objects.get(email = username, password = password)
                    user.last_login = datetime.now(tz=timezone.utc)
                    user.save()
                    if user:
                        userDetails = {
                            "username":user.username,
                            "name":user.name,
                            "email":user.email,
                            "exp":datetime.now(tz=timezone.utc)+timedelta(days=2)
                        }
                        encoded_jwt = jwt.encode(userDetails, "secret", algorithm="HS256")      
                        response_data = {
                            "message": "User logged In Successfully",
                            "results": {
                                "access_token":encoded_jwt
                            },
                            "success": True
                        }
                        return Response(response_data,status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    response_data = {
                        "message": "User not Found, Please Try Again",
                        "results": {},
                        "success": False
                    }
                    return Response(response_data,status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    user = Users.objects.get(username = username, password = password)
                    user.last_login = datetime.now(tz=timezone.utc)
                    user.save()
                    if user:
                        userDetails = {
                            "username":user.username,
                            "name":user.name,
                            "email":user.email,
                            "exp":datetime.now(tz=timezone.utc)+timedelta(days=2)
                        }
                        encoded_jwt = jwt.encode(userDetails, "secret", algorithm="HS256")                
                        response_data = {
                            "message": "User logged In Successfully",
                            "results": {
                                "access_token":encoded_jwt
                            },
                            "success": True
                        }
                        return Response(response_data,status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    response_data = {
                        "message": "User not Found, Please Try Again",
                        "results": {},
                        "success": False
                    }
                    return Response(response_data,status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            response_data = {
                "message": "Please Provide a username and Password",
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)


class sportsItemsAPIView(APIView):
    def get(self,request):
        name = request.GET.get('name')
        if(name):
            user = SportList.objects.filter(name = name)
        else:
            user = SportList.objects.all()
        serializer = SportListSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serialized = SportListSerializer(data=request.data)
        serialized.is_valid()
        if(serialized.is_valid()):
            serialized.save()
            response_data = {
                "message": "Item Added",
                "results": {
                },
                "success": True
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": serialized.errors,
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
      
        
class favSportsAPIView(APIView):
    def get(self,request):
        name = request.GET.get('name')
        if(name):
            user = favSports.objects.filter(name=name)
        else:    
            user = favSports.objects.all()
        serializer = favSportsSerializer(user, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serialized = favSportsSerializer(data=request.data)
        serialized.is_valid()
        if(serialized.is_valid()):
            serialized.save()
            user = favSports.objects.all()
            serializer = favSportsSerializer(user, many=True)
            response_data = {
                "message": "Fav Sports Added",
                "results": {
                    "users":serializer.data
                },
                "success": True
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": serialized.errors,
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,*args, **kwargs):
        payload = request.data
        try:
            user = favSports.objects.get(name=payload['name'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user:
            serializer = favSportsSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Updated Fav Sports"},status=status.HTTP_200_OK)
            else:
                response_data = {
                "message": serializer.errors,
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":""},status=status.HTTP_400_BAD_REQUEST)
        

class getUserList(APIView):
    def get(self,request):
        sports = request.GET.get('sport')
        user = favSports.objects.filter(sport__contains = [sports])
        serializer = favSportsSerializer(user, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class brodcastMessagesAPIView(APIView):
    def get(self,request):
        category = request.GET.get('category')
        user = brodacastMessages.objects.filter(category = category)
        serializer = BrodcastMessagesSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serialized = BrodcastMessagesSerializer(data=request.data)
        serialized.is_valid()
        if(serialized.is_valid()):
            serialized.save()
            response_data = {
                "message": "Message brodcasted",
                "results": {
                },
                "success": True
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": serialized.errors,
                "results": {},
                "success": False
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        

    def put(self,request,*args, **kwargs):
        payload = request.data
        try: 
            user = brodacastMessages.objects.get(id=payload['id'])
                
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
                
        if user:
            if user.status == 0:
                try:
                    length = len(user.accepted_by)
                except:
                    length = 0
                if length <= (user.players - 1):
                    if length == (user.players - 1):
                        request.data['status'] = 1
                        print("User status changed to 1:", user.status,user)
                    serialized = BrodcastMessagesSerializer(user,data=request.data)
                    if serialized.is_valid():
                        serialized.save()
                        response_data = {
                            "message": "Accepted",
                            "results": {
                            },
                            "success": True
                        }
                        return Response(response_data,status=status.HTTP_201_CREATED)
                    else:
                        response_data = {
                            "message": serialized.errors,
                            "results": {},
                            "success": False
                        }
                        return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
                else:
                    response_data = {
                        "message": "Maxmimum Members Joined",
                        "results": {},
                        "success": False
                    }
                    return Response(response_data,status=status.HTTP_204_NO_CONTENT)
            else:
                response_data = {
                        "message": "Maxmimum Members Already Joined",
                        "results": {},
                        "success": False
                    }
                return Response(response_data,status=status.HTTP_208_ALREADY_REPORTED)

        else:
            return Response({"message":""},status=status.HTTP_400_BAD_REQUEST)