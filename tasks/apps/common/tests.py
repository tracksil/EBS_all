from unittest.mock import Mock

from django.contrib.auth.models import User
from django.test import TestCase

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.views import APIView

from apps.common.exceptions import custom_exception_handler

from apps.common.permissions import ReadOnly
from apps.common.validators import CustomNumericValidator


class TestCommon(TestCase):
    fixtures = ["database"]

    def setUp(self) -> None:
        self.client = APIClient()
        # check data in fixture json file
        self.test_user1 = User.objects.get(email="testuser@gmail.com")

    def test_health_view(self):
        response = self.client.get(reverse("health_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['live'], True)

    def test_protected_view(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(reverse("protected_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['live'], True)


factory = APIRequestFactory()


class TestExceptions(TestCase):

    def test_custom_exception_handler_authentication_failed(self):
        exc = AuthenticationFailed('Authentication failed')

        context = Mock()

        response = custom_exception_handler(exc, context)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(str(response.data['detail']), 'Authentication failed')


class TestPermissions(TestCase):
    def test_readonly_permission(self):

        permission = ReadOnly()

        request = factory.get('/test')

        self.assertTrue(permission.has_permission(request, None))

        request = factory.post('/test')

        self.assertFalse(permission.has_permission(request, None))

        class TestView(APIView):
            permission_classes = [IsAuthenticated]

            def get(self, request):
                return Response({'message': 'success'})

        user = User.objects.create_user(username='testuser', password='testpass')

        request = factory.get('/test')
        request.user = user

        view = TestView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = factory.get('/test')

        view = TestView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCustomNumericValidator(TestCase):
    def test_valid_numeric_input(self):
        validator = CustomNumericValidator()
        result = validator('123456')
        self.assertEqual(result, '123456')

    def test_invalid_non_numeric_input(self):
        validator = CustomNumericValidator()
        with self.assertRaises(ValidationError) as context:
            validator('1234a56')

        expected_error = _("This field must contains only numbers!")
        self.assertEqual(str(context.exception.detail[0]), expected_error)
