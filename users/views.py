from django.contrib.auth.tokens import default_token_generator

from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users import compat
from users import email

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, ActivationSerializer
from .permissions import CurrentUserOrAdmin


class UserView(viewsets.ModelViewSet):
    permission_classes = [CurrentUserOrAdmin, ]
    serializer_class = UserSerializer
    queryset = User.objects.all().filter(is_active=True)
    lookup_field = User._meta.pk.name
    token_generator = default_token_generator

    def get_permissions(self):
        '''
        It returns a permission classes for a specific action to endpoints
        '''
        if self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'activation':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        '''
        It returns a serializer classes for specific action to endpoints
        '''
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == "me":
            return UserSerializer
        elif self.action == "activation":
            return ActivationSerializer
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        context = {"user": user}
        to = [compat.get_email(user)]
        email.ActivationEmail(self.request, context).send(to)

    @action(['post'], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()
        to = [compat.get_email(user)]
        email.ConfrimationEmail(self.request).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)
