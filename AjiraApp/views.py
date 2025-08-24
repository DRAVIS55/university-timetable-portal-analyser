from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import ChatMessage
import re
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
import fitz  # PyMuPDF
from collections import defaultdict
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import ChatMessage, PrivateMessage
# views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import PrivateMessage
from .decorators import login_required_custom  # your custom login decorator


from django.db import transaction
from django.db.models import Case, When, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from functools import wraps
from .decorators import login_required_custom, admin_required

from .forms import (
    PDFUploadForm,
    AdvertisementForm,
    NewsForm,
    MemoForm,
    ReelForm,
    HostelForm,
    SignUpForm,
    LoginForm,
)
from .models import (
    TimetableEntry,
    Advertisement,
    News,
    Memo,
    Reel,
    Hostel,
    UserProfile,
)
# ====================== Auth Views ======================
def auth_view(request):
    if request.user.is_authenticated:
        return redirect("portal")

    # Check passwordless session
    user_id = request.session.get("passwordless_user")
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            profile = UserProfile.objects.get(user=user)
            if profile.passwordless:
                login(request, user)
                return redirect("portal")
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            pass

    mode = request.GET.get("mode", "login")
    signup_form = SignUpForm()
    login_form = LoginForm(request)

    if request.method == "POST":
        if request.POST.get("action") == "signup":
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.set_password(signup_form.cleaned_data["password"])
                user.save()
                UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, "✅ Signed up and logged in successfully.")
                return redirect("portal")

        elif request.POST.get("action") == "login":
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)

                if login_form.cleaned_data.get("passwordless"):
                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    profile.passwordless = True
                    profile.save()
                    request.session["passwordless_user"] = user.id

                if not login_form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

                return redirect("portal")

    return render(request, "signUpIn.html", {
        "signup_form": signup_form,
        "login_form": login_form,
        "mode": mode,
    })


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    # Clear any custom session values
    request.session.pop("passwordless_user", None)

    # Django logout (clears session and user auth)
    logout(request)

    # Redirect to login page (make sure name matches in urls.py)
    return redirect("auth")




# ====================== Portal & Timetable ======================
@login_required_custom
def portal(request):
    q_course = (request.GET.get("course") or "COSC").strip().upper()
    q_year = (request.GET.get("year") or "3").strip()
    qs = TimetableEntry.objects.all()

    if q_course:
        qs = qs.filter(course_code__istartswith=q_course.lower())
    if q_year.isdigit():
        qs = qs.filter(year=int(q_year))

    day_order = Case(
        When(day__iexact="Monday", then=1),
        When(day__iexact="Tuesday", then=2),
        When(day__iexact="Wednesday", then=3),
        When(day__iexact="Thursday", then=4),
        When(day__iexact="Friday", then=5),
        default=99,
        output_field=IntegerField(),
    )

    time_order = Case(
        When(time__icontains="7.00", then=1),
        When(time__icontains="10.00", then=2),
        When(time__icontains="1.00", then=3),
        When(time__icontains="4.00", then=4),
        default=99,
        output_field=IntegerField(),
    )

    qs = qs.order_by(day_order, time_order, "room")

    codes = TimetableEntry.objects.values_list("course_code", flat=True).distinct()
    prefixes = sorted({re.sub(r"\d+$", "", (c or "")).upper() for c in codes if c})

    ads = Advertisement.objects.filter(active=True)[:10]
    mid = len(ads) // 2 + len(ads) % 2
    ads_left = ads[:mid]
    ads_right = ads[mid:]

    news_list = News.objects.all().order_by("-created_at")[:5]
    memos = Memo.objects.all().order_by("-created_at")[:5]
    reels = Reel.objects.all().order_by("-created_at")[:5]
    hostels = Hostel.objects.all()[:5]

    slots = [
        "7.00 AM→10.00",
        "10.00 AM→1.00",
        "10.00 AM→1.00 PM",
        "1.00 PM→4.00",
        "4.00 PM→7.00",
        "4.00 PM 4.00 PM→7.00 PM",
        "10.00 AM→1.00PM ",
        "10.00 AM→1.00PM",
    ]

    years = ["1", "2", "3", "4", "5", "6"]

    context = {
        "timetable_entries": qs,
        "courses": prefixes,
        "selected_course": q_course,
        "selected_year": q_year,
        "ads_left": ads_left,
        "ads_right": ads_right,
        "news_list": news_list,
        "memos": memos,
        "reels": reels,
        "hostels": hostels,
        "slots": slots,
        "years": years,
    }

    return render(request, "chukaPortal.html", context)


@login_required_custom
def timetable_view(request):
    return portal(request)


#========MY PDF READER AND ANALYZER (MY AI)==========#
DAY_NAMES = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

#==================- helpers==================-
def _group_words_by_lines(words, y_tol=2.0):
    """Group words by their y coordinate into visual lines."""
    if not words:
        return []
    words = sorted(words, key=lambda w: (round(w[1], 1), w[0]))
    lines, current = [], [words[0]]
    current_y = words[0][1]
    for w in words[1:]:
        if abs(w[1] - current_y) <= y_tol:
            current.append(w)
        else:
            lines.append(sorted(current, key=lambda t: t[0]))
            current = [w]
            current_y = w[1]
    lines.append(sorted(current, key=lambda t: t[0]))
    return lines

def _line_text(line_words):
    return " ".join(w[4] for w in line_words).strip()

def _build_columns_from_header(line_words):
    """Identify ROOM + 4 timeslot columns from header row."""
    ws = sorted(line_words, key=lambda w: w[0])

    # find "ROOM"
    room_x = None
    for w in ws:
        if w[4].upper() == "ROOM":
            room_x = w[0]
            break
    if room_x is None:
        return None, None

    # find timeslot starts
    starts = [w[0] for w in ws if re.fullmatch(r"\d{1,2}\.\d{2}", w[4])]
    if len(starts) < 4:
        return None, None

    col_starts = sorted([room_x] + starts[:4])  # ensure 4 slots only
    col_ranges = []
    for i, x_start in enumerate(col_starts):
        if i < len(col_starts) - 1:
            x_end = (col_starts[i] + col_starts[i + 1]) / 2.0
        else:
            x_end = max(w[2] for w in ws) + 50.0
        col_ranges.append((x_start - 2.0, x_end))

    # capture labels (AM/PM optional)
    time_labels = []
    for c in range(1, 5):
        x0, x1 = col_ranges[c]
        words_in_cell = [w[4] for w in ws if x0 <= w[0] < x1]
        time_labels.append(" ".join(words_in_cell).strip())
    return col_ranges, time_labels

def _cells_from_row(line_words, col_ranges):
    """Split a line into 5 cells (room + 4 slots)."""
    ws = sorted(line_words, key=lambda w: w[0])
    cells = []
    for x0, x1 in col_ranges:
        words_in_cell = [w[4] for w in ws if x0 <= w[0] < x1]
        cells.append(" ".join(words_in_cell).strip())
    return cells

def _normalize_day(text):
    t = text.strip().upper()
    for d in DAY_NAMES:
        if t == d:
            return d.capitalize()
    return None

def _extract_course_info(unit_text: str):
    """Extract (course_code, year) from unit text."""
    if not unit_text:
        return "", None
    first_piece = re.split(r"\s*(?:/|&|,|\band\b)\s*", unit_text, flags=re.IGNORECASE)[0]
    cleaned = re.sub(r"[()\s\.]", "", first_piece)

    m = re.search(r"([A-Za-z]{2,})[-_ ]*(\d{3,})", cleaned)
    if not m:
        m = re.search(r"([A-Za-z]{2,})(\d{3,})", cleaned)
    if not m:
        return "", None

    letters = m.group(1)
    digits_all = m.group(2)
    last3 = digits_all[-3:]
    course_code = (letters + last3).lower()
    year = int(last3[0]) if last3 and last3[0].isdigit() else None
    return course_code, year

#==================- main parse==================-
def parse_timetable(pdf_file):
    """Parse timetable PDF into TimetableEntry objects (unsaved)."""
    try:
        pdf_file.seek(0)
    except Exception:
        pass

    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    entries, current_day, col_ranges, time_labels = [], None, None, None

    for page in doc:
        words = page.get_text("words")
        lines = _group_words_by_lines(words)

        for line_words in lines:
            text = _line_text(line_words)

            # Detect day headers
            nd = _normalize_day(text)
            if nd:
                current_day, col_ranges, time_labels = nd, None, None
                continue

            # Detect table headers (more flexible now)
            if "ROOM" in text.upper():
                cr, tl = _build_columns_from_header(line_words)
                if cr and tl and len(cr) == 5 and len(tl) >= 4:
                    col_ranges, time_labels = cr, tl[:4]
                else:
                    col_ranges, time_labels = None, None
                continue

            if not current_day or not col_ranges:
                continue

            # Split into cells
            room, s1, s2, s3, s4 = _cells_from_row(line_words, col_ranges)
            if not room or len(room) < 2:
                continue

            for i, cell in enumerate([s1, s2, s3, s4]):
                cell = cell.strip()
                if not cell:
                    continue
                course_code, year = _extract_course_info(cell)
                if not course_code:
                    continue
                entries.append(
                    TimetableEntry(
                        course_code=course_code,
                        unit_code=cell,
                        unit_name="",
                        year=year,
                        day=current_day,
                        time=time_labels[i],
                        room=room,
                    )
                )
    return entries

# ====================== PDF Upload & Parsing ======================
@login_required_custom
# ================ upload view =============
def upload_timetable(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.cleaned_data.get("timetable_pdf")
            if not pdf:
                messages.error(request, "No PDF file was uploaded.")
                return redirect("upload_timetable")

            try:
                entries = parse_timetable(pdf)
            except Exception as e:
                messages.error(request, f"Failed to parse PDF: {e}")
                return redirect("upload_timetable")

            if not entries:
                messages.warning(request, "No valid timetable entries found in the PDF.")
                return redirect("timetable")

            with transaction.atomic():
                TimetableEntry.objects.all().delete()
                TimetableEntry.objects.bulk_create(entries, batch_size=500)

            messages.success(request, f"✅ Uploaded {len(entries)} entries (replaced previous timetable).")
            return redirect("timetable")
        else:
            messages.error(request, "Invalid form. Please upload a valid PDF.")
    else:
        form = PDFUploadForm()
    return render(request, "upload.html", {"form": form})

#===================TIME TABLE VIEW============================
def timetable_view(request):
    entries = TimetableEntry.objects.all()
    course = request.GET.get("course", "").strip()
    year = request.GET.get("year", "").strip()

    if course:
        entries = entries.filter(course_code__icontains=course)  # use icontains
    if year.isdigit():
        entries = entries.filter(year=int(year))

    slots = [
        ("7–10 AM", 7, 10),
        ("10–1 PM", 10, 13),
        ("1–4 PM", 13, 16),
        ("4–7 PM", 16, 19),
    ]

    # Convert QuerySet to list so we can add dynamic attributes
    entries = list(entries)
    for entry in entries:
        entry.slot = None
        # Parse time string like "7.00 AM→10.00"
        time_match = re.match(r"(\d{1,2})\.\d{1,2}\s*(AM|PM)", entry.time)
        if time_match:
            hour = int(time_match.group(1))
            meridian = time_match.group(2)
            if meridian.upper() == "PM" and hour != 12:
                hour += 12
            elif meridian.upper() == "AM" and hour == 12:
                hour = 0
            # Assign slot
            for slot_name, start, end in slots:
                if start <= hour < end:
                    entry.slot = slot_name
                    break

    # Sort entries by day, slot, room
    day_order_dict = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5}
    slot_order_dict = {s[0]: i+1 for i, s in enumerate(slots)}

    entries.sort(key=lambda e: (
        day_order_dict.get(e.day, 99),
        slot_order_dict.get(e.slot, 99),
        e.room
    ))

    context = {
        "timetable_entries": entries,
        "selected_course": course,
        "selected_year": year,
        "slots": [s[0] for s in slots],
        "courses": TimetableEntry.objects.values_list("course_code", flat=True).distinct()
    }

    return render(request, "timetable.html", context)


# ======================= delete view =====================
def delete_timetable(request):
    if request.method == "POST":
        with transaction.atomic():
            TimetableEntry.objects.all().delete()
        messages.success(request, "✅ All timetable entries have been deleted.")
        return redirect("upload_timetable")
    return render(request, "delete_timetable.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import (
    AdminRegistrationForm, ReligionForm, PoliticsForm, MusicForm,
    AdvertisementForm, NewsForm, MemoForm, ReelForm, HostelForm
)
from .models import Religion, Politics, Music, Advertisement, News, Memo, Reel, Hostel

# ================== ADMIN PANEL ==================
def admin_panel(request):
    # Initialize forms
    forms = {
        "admin_form": AdminRegistrationForm(),
        "religion_form": ReligionForm(),
        "politics_form": PoliticsForm(),
        "music_form": MusicForm(),
        "ad_form": AdvertisementForm(),
        "news_form": NewsForm(),
        "memo_form": MemoForm(),
        "reel_form": ReelForm(),
        "hostel_form": HostelForm(),
    }

    # Handle POST (Add/Edit)
    if request.method == "POST":
        action = request.POST.get("action")
        item_id = request.POST.get("item_id")

        action_map = {
            "add_admin": (AdminRegistrationForm, User),
            "edit_admin": (AdminRegistrationForm, User),
            "add_religion": (ReligionForm, Religion),
            "edit_religion": (ReligionForm, Religion),
            "add_politics": (PoliticsForm, Politics),
            "edit_politics": (PoliticsForm, Politics),
            "add_music": (MusicForm, Music),
            "edit_music": (MusicForm, Music),
            "add_ad": (AdvertisementForm, Advertisement),
            "edit_ad": (AdvertisementForm, Advertisement),
            "add_news": (NewsForm, News),
            "edit_news": (NewsForm, News),
            "add_memo": (MemoForm, Memo),
            "edit_memo": (MemoForm, Memo),
            "add_reel": (ReelForm, Reel),
            "edit_reel": (ReelForm, Reel),
            "add_hostel": (HostelForm, Hostel),
            "edit_hostel": (HostelForm, Hostel),
        }

        if action in action_map:
            FormClass, ModelClass = action_map[action]

            instance = None
            if "edit" in action and item_id:
                try:
                    instance = get_object_or_404(ModelClass, id=int(item_id))
                except ValueError:
                    messages.error(request, "Invalid item ID")
                    return redirect("admin_panel")

            # Check if form has file fields
            has_files = any(
                field.widget.__class__.__name__ == "ClearableFileInput"
                for field in FormClass().fields.values()
            )

            form = FormClass(
                request.POST, request.FILES, instance=instance
            ) if has_files else FormClass(request.POST, instance=instance)

            if form.is_valid():
                obj = form.save(commit=False)
                # Handle User password
                if isinstance(obj, User):
                    pw = form.cleaned_data.get("password")
                    if pw:
                        obj.set_password(pw)
                    elif instance:
                        obj.password = instance.password
                obj.save()
                messages.success(request, f"{FormClass.__name__.replace('Form','')} {'updated' if instance else 'added'} successfully!")
                return redirect("admin_panel")
            else:
                print(form.errors)
                messages.error(request, f"Failed to save {FormClass.__name__.replace('Form','')}. Check form for errors.")

    # Collect instances for display
    context = {
        **forms,
        "users": User.objects.filter(is_staff=True),
        "religions": Religion.objects.all(),
        "politics_list": Politics.objects.all(),
        "music_list": Music.objects.all(),
        "ads": Advertisement.objects.all(),
        "news_list": News.objects.all(),
        "memos": Memo.objects.all(),
        "reels": Reel.objects.all(),
        "hostels": Hostel.objects.all(),
        "admins": User.objects.filter(is_staff=True),
    }

    # Handle edit view toggle
    edit_id = request.GET.get("edit_id")
    edit_type = request.GET.get("edit_type")
    if edit_type and edit_id:
        try:
            instance = get_object_or_404(action_map[f"edit_{edit_type}"][1], id=int(edit_id))
            context[f"edit_{edit_type}"] = instance
            context[f"{edit_type}_form"] = action_map[f"edit_{edit_type}"][0](instance=instance)
        except Exception:
            messages.error(request, "Failed to load item for editing.")

    return render(request, "admin_panel.html", context)

# ================== GENERIC DELETE ==================
def delete_instance(request, model_class, item_id):
    item = get_object_or_404(model_class, id=item_id)
    item.delete()
    messages.success(request, f"{model_class.__name__} deleted successfully!")
    return redirect("admin_panel")

# Specific delete views
def delete_admin(request, user_id): return delete_instance(request, User, user_id)
def delete_religion(request, item_id): return delete_instance(request, Religion, item_id)
def delete_politics(request, item_id): return delete_instance(request, Politics, item_id)
def delete_music(request, item_id): return delete_instance(request, Music, item_id)
def delete_ad(request, item_id): return delete_instance(request, Advertisement, item_id)
def delete_news(request, item_id): return delete_instance(request, News, item_id)
def delete_memo(request, item_id): return delete_instance(request, Memo, item_id)
def delete_reel(request, item_id): return delete_instance(request, Reel, item_id)
def delete_hostel(request, item_id): return delete_instance(request, Hostel, item_id)


# ====================== Chat, Confession, Displayer ======================
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConfessionForm
from .models import Confession
from .decorators import login_required_custom

@login_required_custom
def confession(request):
    if request.method == "POST":
        form = ConfessionForm(request.POST)
        if form.is_valid():
            confession = form.save(commit=False)
            confession.user = request.user
            confession.save()
            messages.success(request, "Confession sent successfully!")
            return redirect('confession')
        else:
            messages.error(request, "Failed to send confession. Please check your input.")
    else:
        form = ConfessionForm()

    all_confessions = Confession.objects.all()

    context = {
        'form': form,
        'confessions': all_confessions,
    }
    return render(request, "confession.html", context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import News, Hostel, Reel, Memo, Advertisement
from .models import News, Hostel, Reel, Memo, Religion, Politics, Music

SECTION_MODELS = {
    "news": News,
    "hostels": Hostel,
    "reels": Reel,
    "memos": Memo,
    "religion": Religion,
    "politics": Politics,
    "music": Music,
}

@login_required
def displayer(request, section):
    context = {"section": section}

    if section == "news":
        context["items"] = News.objects.all().order_by("-created_at")
    elif section == "hostels":
        context["items"] = Hostel.objects.all().order_by("-created_at")
    elif section == "reels":
        context["items"] = Reel.objects.all().order_by("-created_at")
    elif section == "memos":
        context["items"] = Memo.objects.all().order_by("-created_at")
    elif section == "ads":
        context["items"] = Advertisement.objects.filter(active=True).order_by("-created_at")
    else:
        context["items"] = []  # fallback

    return render(request, "displayer.html", context)

#====================Chat Board====================

@login_required_custom
def chatBoard(request):
    return render(request, "Chat.html")

# API endpoint to fetch messages
@login_required_custom
def get_messages(request):
    messages = ChatMessage.objects.order_by("-timestamp")[:50]  # last 50
    data = [
        {
            "user": msg.user.username,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime("%H:%M")
        }
        for msg in reversed(messages)  # so oldest first
    ]
    return JsonResponse(data, safe=False)

# API endpoint to send a message
@csrf_exempt
@login_required_custom
def send_message(request):
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        if text:
            ChatMessage.objects.create(user=request.user, message=text, timestamp=now())
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

@admin_required
def edit_admin(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=True)
    form = AdminRegistrationForm(instance=user)
    
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data["password"]:
                user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, f"✅ Admin '{user.username}' updated successfully!")
            return redirect("admin_panel")
    
    return render(request, "edit_admin.html", {"form": form, "admin_user": user})


@admin_required
def delete_admin(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=True)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"❌ Admin '{user.username}' deleted successfully!")
        return redirect("admin_panel")
    return render(request, "delete_admin.html", {"admin_user": user})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import ChatMessage, PrivateMessage
from django.contrib.auth.models import User

# Use your custom login decorator everywhere
from .decorators import login_required_custom


# ------------------ CHAT BOARD ------------------ #
@login_required_custom
def chatBoard(request):
    """Main chat dashboard (global + private + contacts + reports)"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, "Chat.html", {"users": users})


# ------------------ GLOBAL CHAT ------------------ #
@login_required_custom
def global_messages(request):
    msgs = ChatMessage.objects.order_by("timestamp")
    data = [
        {"user": m.user.username, "message": m.message, "timestamp": m.timestamp.strftime("%H:%M:%S")}
        for m in msgs
    ]
    return JsonResponse(data, safe=False)


@login_required_custom
def send_message(request):
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        if text:
            ChatMessage.objects.create(user=request.user, message=text, timestamp=now())
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


# ------------------ PRIVATE CHAT ------------------ #
@login_required_custom
def private_messages(request, username):
    other = get_object_or_404(User, username=username)
    msgs = PrivateMessage.objects.filter(
        sender__in=[request.user, other],
        recipient__in=[request.user, other]
    ).order_by("timestamp")

    data = [
        {"user": m.sender.username, "message": m.message, "timestamp": m.timestamp.strftime("%H:%M:%S")}
        for m in msgs
    ]
    return JsonResponse(data, safe=False)


@login_required_custom
def send_private_message(request, username):
    if request.method == "POST":
        other = get_object_or_404(User, username=username)
        text = request.POST.get("message", "").strip()
        if text:
            PrivateMessage.objects.create(
                sender=request.user,
                recipient=other,
                message=text,
                timestamp=now()
            )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


# ------------------ REPORT ------------------ #
@login_required_custom
def report_message(request):
    if request.method == "POST":
        msg_id = request.POST.get("message_id")
        reason = request.POST.get("reason")
        # Example: Save into a Report model
        # Report.objects.create(user=request.user, message_id=msg_id, reason=reason)
        return JsonResponse({"status": "report received"})
    return JsonResponse({"status": "error"}, status=400)


