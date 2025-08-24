# AjiraApp/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from .models import UserProfile
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
User = get_user_model()

# ================== Custom Login (with passwordless support) ==================
def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # Check passwordless session
        user_id = request.session.get("passwordless_user")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                profile = UserProfile.objects.get(user=user)
                if profile.passwordless:
                    login(request, user)
                    return view_func(request, *args, **kwargs)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                pass

        login_url = getattr(settings, "LOGIN_URL", "/auth/")
        return redirect(f"{login_url}?next={request.path}")
    return _wrapped_view


# ================== Admin-only access ==================


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "⚠️ Please log in first.")
            return redirect("auth")
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, "🚫 You do not have permission to access the admin panel.")
            return redirect("portal")
        return view_func(request, *args, **kwargs)
    return wrapper



