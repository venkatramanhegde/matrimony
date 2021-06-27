import os

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.backends import django
from django.urls import reverse
from django.views import View
from rest_framework import status
from django.conf import settings
from .authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer, AdminPageSerializer, UserPageSerializer,\
    UpdateUserSerializer, LogedinUserDetailsSerializer, UserDetailSerializer
from .models import User, UserDetails, Token
from datetime import date


class LoginAPIView(APIView):
    """
    This class based api view is for login.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        This method takes 'email' and 'password'
        url: http://localhost:8000/appmanagment/login/

        """

        serializer = LoginSerializer(data=request.data)
        user1 = authenticate(phone_no=request.data.get('phone_no'), password=request.data.get('password'))
        if not user1:
            return Response("invalid credentials", status=401)
        login(request, user1)
        token = Token.objects.create(
            user=user1)  # if authenticated successfully, token is generated for that user.(ex:8953636ea742ba4d8ce22b0f2d6001299dc6b198)
        user_token = token.key
        print(user1)
        if user1.is_admin:
            serializer = LogedinUserDetailsSerializer(UserDetails.objects.filter(user_id=request.user.id), many=True)
            return Response({"data": serializer.data, "user_token":user_token}, status.HTTP_200_OK)

            # return HttpResponseRedirect(reverse('admin_page'))

        else:
            if user1.is_approved:

                serializer = LogedinUserDetailsSerializer(UserDetails.objects.filter(user_id=request.user.id), many=True)
                return Response({"data": serializer.data, "user_token":user_token}, status.HTTP_200_OK)
            else:
                return Response({"data":"Your profile is under review. Please contact 8792737236 in case of any clarification or question"}, status=401)

            # if request.user.is_male:
                # serializer = AdminPageSerializer(UserDetails.objects.filter(Q(is_user=True) & Q(is_female=True)) ,
                #                                                      # & Q(date_of_birth__lte=request.user.date_of_birth)),
                #                                                       many=True)
                # return Response({"data": serializer.data}, status.HTTP_200_OK)
            # if request.user.is_female:
                # serializer = AdminPageSerializer(User.objects.filter(
                #     Q(is_user=True) & Q(is_male=True) & Q(date_of_birth__gte=request.user.date_of_birth)),
                #                                  many=True)
        return Response("User logedin successfull")


class SignUp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    def post(self, request):
        """
                         url:appmanagment/sign_up/
                         This will for sign up to application
                """

        print(request.data)
        myfiles = request.FILES.getlist('photo1')
        folder = 'photos/'  # document uploaded to datastore inside media folder
        data = []
        file_data = {}
        for f in myfiles:
            filename = str(f.name).replace(" ", "")
            extension = filename.split('.')
            fs = FileSystemStorage(location=folder)  # defaults to DATASTORE
            name = fs.save(filename, f)
            mediapath = folder + "{}"
            filepath = os.path.join(mediapath).format(name)
            # file_data = {'photo1': filepath, 'horoscope': horoscope,}
        myfiles = request.FILES.getlist('horoscope')
        folder = 'jataga/'  # document uploaded to datastore inside media folder
        for f in myfiles:
            filename = str(f.name).replace(" ", "")
            extension = filename.split('.')
            fs = FileSystemStorage(location=folder)  # defaults to DATASTORE
            name = fs.save(filename, f)
            mediapath = folder + "{}"

        today = date.today()
        age = today.year - int(request.data["date_of_birth"][:4])
        user_add = self.serializer_class(data=request.data, context={'file_data': data, 'age': age})

        print(age)
        if user_add.is_valid():
            user_add.save()
            return Response({"msg": "user added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": user_add.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdminPage(APIView):
    # permission_classes = [IsInstructor]  # Only Authenticated Instructor  can access this api.
    serializer_class = AdminPageSerializer

    def get(self, request):
        # try:
        print("here", User.objects.filter(id=5))
        u = User.objects.all()
        for i in u:
            print(i.id)
        serializer = AdminPageSerializer(User.objects.all(), many=True)
        print(serializer.data)
        return Response({"data": serializer.data}, status.HTTP_200_OK)
        # except Exception as e:
        #     print(e)
        #     return Response({"msg": "something went wrong"})


class FilterUserPage(APIView):
    # permission_classes = [IsInstructor]  # Only Authenticated Instructor  can access this api.
    permission_classes = (AllowAny,)
    serializer_class = UserPageSerializer
    authentication_classes = [TokenAuthentication,]

    def post(self, request):
        print(request.data)
        try:
            age_from = request.data.get("age_from", None)
            age_to = request.data.get("age_to", None)
            height_from = request.data.get("height_from", None)
            height_to = request.data.get("height_to", None)
            religion = request.data.get("religion", None)
            cast = request.data.get("cast", None)
            occupation = request.data.get("occupation", None)
            print(height_from)
            if "filter" in request.data:
                if request.user.is_admin:
                    query_set = UserDetails.objects.filter(is_user=True)
                    if age_from:
                        query_set = query_set.filter(Q(age__gte=age_from) and Q(age__lte=age_to))
                        print(query_set)

                    if height_from:
                        print("height_from")

                        query_set = query_set.filter(Q(height_from__gte=age_from) and Q(height_to__lte=age_to))
                    if religion:
                        query_set = query_set.filter(community=religion)
                    if cast:
                        query_set = query_set.filter(cast=cast)
                    if occupation:
                        query_set = query_set.filter(occupation=occupation)

                    serializer = UserDetailSerializer(query_set, many=True)
                else:
                    if request.user.is_male:
                        # serializer = AdminPageSerializer(User.objects.filter(Q(is_user=True) & Q(is_female=True) & Q(date_of_birth__lte=request.user.date_of_birth)),
                        #                                  many=True)
                        query_set = UserDetails.objects.filter(is_user=True, is_male=False, is_approved=True)
                        print(query_set)
                        if age_from:
                            print("age_from")

                            query_set = query_set.filter(age__gte=age_from, age__lte=age_to)
                            print(query_set)

                        if height_from:
                            print("height_from")
                            query_set = query_set.filter(height__gte=height_from, height__lte=height_to)
                            print(query_set)
                        if religion:
                            query_set = query_set.filter(community=religion)
                        if cast:
                            query_set = query_set.filter(cast=cast)
                        if occupation:
                            query_set = query_set.filter(occupation=occupation)

                        serializer = UserDetailSerializer(query_set, many=True)
                        return Response({"data": serializer.data}, status.HTTP_200_OK)
                    if request.user.is_female:
                        serializer = UserDetailSerializer(User.objects.filter(
                            Q(is_user=True) & Q(is_male=True) & Q(date_of_birth__gte=request.user.date_of_birth)),
                            many=True)
                        return Response({"data": serializer.data}, status.HTTP_200_OK)
            else:
                if request.user.is_admin:
                    print("asas")
                    serializer = UserDetailSerializer(UserDetails.objects.filter(is_user=True), many=True)
                    return Response({"data": serializer.data}, status.HTTP_200_OK)
                else:
                    if request.user.is_male:
                        serializer = UserDetailSerializer(UserDetails.objects.filter(
                            Q(is_user=True) & Q(is_female=True) & Q(date_of_birth__gte=request.user.date_of_birth) & Q(is_approved=True) ),
                                                         many=True)
                        return Response({"data": serializer.data}, status.HTTP_200_OK)
                    if request.user.is_female:
                        serializer = UserDetailSerializer(UserDetails.objects.filter(
                            Q(is_user=True) & Q(is_male=True) & Q(date_of_birth__lte=request.user.date_of_birth)& Q(is_approved=True) ),
                            many=True)
                        return Response({"data": serializer.data}, status.HTTP_200_OK)
        except Exception:
            print(serializer.errors)
            return Response({"msg": "something went wrong"})


class UpdateUser(APIView):
    # permission_classes = [IsInstructor]  # Only Authenticated Instructor  can access this api.
    serializer_class = UpdateUserSerializer
    def post(self, request):
        try:
            if 'id' in request.data:
                user = UserDetails.objects.filter(user_id=request.data['id']).first()
                if not user:
                    return Response({"msg": user.errors}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    update_tag_serializer = UpdateUserSerializer(user, data=request.data)
                if not update_tag_serializer.is_valid():
                    return Response({"msg": user.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "user updated successfully", "data": update_tag_serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"msg": "something went wrong please try again"})


class UserApproveView(APIView):
    authentication_classes = [TokenAuthentication,]
    def post(self, request):
        id = request.data['user_id']
        user_det_obj = UserDetails.objects.filter(user_id=id).update(is_approved=True, is_rejected=False)
        user_obj = User.objects.filter(id=id).update(is_approved=True, is_rejected=True)
        return Response({"msg": "User approved successfully"})



class LogoutAPIView(APIView):
    """
    This class based api view is for logout.
    """
    authentication_classes = [TokenAuthentication, ]
    def post(self, request, *args, **kwargs):
        """
        This method takes 'token'
        url: api/v1/auth/logout/{{token}}
        :return: success message.
        This api will be called when logout button is clicked.
        """
        token = request.data.get('token') # users token is fetched and deleted. Token is available only for that seesion(Untill user is logged out)
        try:
            Token.objects.get(key=token).delete()
            logout(request)
        except:
            return Response({"message": "logout failed"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class ForgotPassword(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_id = User.objects.get(phone_no=request.data["phone_no"])
        user_id.set_password(request.data["password"])

        return JsonResponse({"message": "Password updated successful"}, status=200)


class RejectUser(APIView):
    authentication_classes = [TokenAuthentication, ]
    def post(self, request):
        id = request.data['user_id']
        user_det_obj = UserDetails.objects.filter(user_id=id).update(is_approved=False, is_rejected=True)
        user_obj = User.objects.filter(id=id).update(is_approved=False, is_rejected=True)
        return Response({"msg": "User rejected successfully"})

