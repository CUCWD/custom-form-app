"""Views for custom account field self-service API."""

import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import ExtraInfoForm
from .models import ExtraInfo


CUSTOM_FIELDS = (
    'ethnicity',
    'employment_status',
    'enrolled_in_school',
    'enrolled_in_school_type',
    'local_community_living',
    'zipcode',
)


def _serialize_extra_info(extra_info):
    """Return the custom-field payload using the six supported fields."""
    payload = {}
    for field_name in CUSTOM_FIELDS:
        payload[field_name] = getattr(extra_info, field_name, None)
    return payload


def _get_or_create_extra_info(user):
    """Create the associated ExtraInfo record for the authenticated user."""
    extra_info, _ = ExtraInfo.objects.get_or_create(user=user)
    return extra_info


def _get_patch_data(request):
    """Parse a PATCH request body into the supported custom-field mapping."""
    if not request.body:
        return {}

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (TypeError, ValueError, UnicodeDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    return {
        field_name: payload[field_name]
        for field_name in CUSTOM_FIELDS
        if field_name in payload
    }


def _custom_fields_response(request, user):
    """Return or update the requested user's custom registration fields."""
    is_self = request.user == user
    if not is_self and (request.method == 'PATCH' or not request.user.is_staff):
        return JsonResponse({'detail': 'You do not have permission to access this account.'}, status=403)

    extra_info = _get_or_create_extra_info(user)

    if request.method == 'GET':
        return JsonResponse(_serialize_extra_info(extra_info))

    patch_data = _get_patch_data(request)
    if patch_data is None:
        return JsonResponse({'detail': 'JSON body must be an object.'}, status=400)

    if not patch_data:
        return JsonResponse(_serialize_extra_info(extra_info))

    form = ExtraInfoForm(instance=extra_info, data=patch_data)
    if not form.is_valid():
        return JsonResponse(form.errors, safe=False, status=400)

    instance = form.save(commit=False)
    instance.user = user
    instance.save()
    return JsonResponse(_serialize_extra_info(instance))


@require_http_methods(['GET', 'PATCH'])
def me(request):
    """Return or update the authenticated user's custom registration fields."""
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

    return _custom_fields_response(request, request.user)


@require_http_methods(['GET', 'PATCH'])
def account(request, username):
    """Return or update custom fields for a username with access controls."""
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

    user = get_user_model().objects.filter(username=username).first()
    if user is None:
        return JsonResponse({'detail': 'Account not found.'}, status=404)

    return _custom_fields_response(request, user)
