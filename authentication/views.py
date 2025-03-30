from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from authentication.emails import EmailSender
from authentication.serializers import (
    GetUserSerializer,
    RegisterSerializer,
    CreateUserProfileSerializer,
)
from django.contrib.auth.models import User
from .utils import PermissionHandler
from rest_framework.response import Response
from .models import UserType, UserProfile, VerificationCode
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
import string
from datetime import timedelta
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().get(id=request.user.id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    allowed_methods = ("POST",)

    def mask_email(self, email):
        name, domain = email.split("@")
        name = name[:1] + "***" + name[-1:] if len(name) > 1 else name + "***"
        return f"{name}@{domain}"

    def create(self, request, *args, **kwargs):
        otp = random.randint(100000, 999999)

        user_type, created = UserType.objects.get_or_create(
            name=request.data.get("user_type")
        )

        data = {
            "username": request.data.get("username"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "password": request.data.get("password"),
            "password2": request.data.get("password2"),
            "email": request.data.get("email"),
        }

        user_profile_data = {
            "user": None,
            "phone_number": request.data.get("phone_number"),
            "user_type": user_type.id,
        }
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        user = serializer.save()

        # create profile
        user_profile_data["user"] = user.id
        user_profile = CreateUserProfileSerializer(data=user_profile_data)
        if not user_profile.is_valid():
            user.delete()
            raise serializers.ValidationError(user_profile.errors)

        user_profile.save()

        if user:
            # Create verification code
            vc = VerificationCode.objects.create(
                user=user, code=otp, created_at=timezone.localtime(timezone.now())
            )
            try:

                PermissionHandler.update_permissions(
                    group_name=user_type.name,
                    user=user,
                    request=request,
                    models=[UserProfile],
                )
            except Exception as e:
                user.delete()
                raise serializers.ValidationError(f"Error updating permissions {e}")
            try:
                EmailSender.send_otp_email(user, otp)
            except Exception as e:
                user.delete()
                raise serializers.ValidationError(f"Error sending email {e}")

        masked_email = self.mask_email(request.data.get("email"))
        message = f"User created successfully. A verification code has been sent to your email ({masked_email}). Please verify your account immediately before the session expires in 10 minutes."
        return Response(
            {"message": message, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class ResendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp = random.randint(100000, 999999)
        if not request.data.get("email"):
            raise serializers.ValidationError("Email is required")
        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        try:
            verification_model = VerificationCode.objects.get(user=user)
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Verification code does not exist")

        if user.is_active:
            raise serializers.ValidationError(
                "ACCOUNT ALREADY ACTIVATED, NO NEED TO RESEND OTP"
            )

        time_remaining = (
            verification_model.created_at
            + timedelta(minutes=10)
            - timezone.localtime(timezone.now())
        )
        if time_remaining > timedelta(minutes=0):

            raise serializers.ValidationError(
                f"PLEASE WAIT FOR {time_remaining.seconds // 60} MINUTES AND {time_remaining.seconds % 60} SECONDS BEFORE SENDING ANOTHER OTP"
            )

        verification_model.code = otp
        verification_model.otp_used = False
        verification_model.created_at = timezone.localtime(timezone.now())
        verification_model.save()
        try:
            EmailSender.send_otp_email(user, otp)
        except Exception as e:
            raise serializers.ValidationError(f"Error sending email {e}")
        return Response({"message": "OTP SENT SUCCESSFULLY"}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.data.get("email") or not request.data.get("otp"):
            return Response(
                {"message": "Email and OTP are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        if user.is_active:
            return Response(
                {"message": "ACCOUNT ALREADY ACTIVATED"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = request.data.get("otp", None)
        # user = User.objects.get(email=request.data.get('email'))
        verification_model = VerificationCode.objects.get(user=user)
        if verification_model.code == otp and timezone.localtime(
            timezone.now()
        ) < verification_model.created_at + timedelta(minutes=10):
            user.is_active = True
            verification_model.otp_used = True
            verification_model.save()
            user.save()
            return Response(
                {"message": "ACCOUNT ACTIVATED SUCCESSFULLY"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": " Invalid OTP or OTP expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# class ReactivateAccountView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user_id = request.data.get("user_id")

#         if not user_id:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="User ID (UUID) is required.",
#             )

#         # Retrieve the user by UUID
#         user = User.objects.filter(id=user_id).first()

#         if not user:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="User does not exist.",
#             )

#         if user.is_active:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="Account is already Active.",
#             )

#         # Activate the account
#         user.is_active = True
#         user.save()

#         return api_response(
#             code=ApiCodes.SUCCESS,
#             status=True,
#             data=None,
#             message="Account Re-activated successfully.",
#         )


# class DeactivateAccountView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user_id = request.data.get("user_id")

#         if not user_id:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="User ID (UUID) is required.",
#             )

#         # Retrieve the user by UUID
#         user = User.objects.filter(id=user_id).first()

#         if not user:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="User does not exist.",
#             )

#         if user.is_active == False:
#             return api_response(
#                 code=ApiCodes.BAD_REQUEST,
#                 status=True,
#                 data=None,
#                 message="Account is already Deactivated.",
#             )

#         # Activate the account
#         user.is_active = False
#         user.save()

#         return api_response(
#             code=ApiCodes.SUCCESS,
#             status=True,
#             data=None,
#             message="Account Deactivated Successfully.",
#         )
