from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileUpdateForm
from .models import Profile


# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(
                request,
                username=username,
                password=password,
            )
            login(request, user)

            messages.success(request, "Registration successful.")
            return redirect("edit_profile")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# -----------------------------
# EDIT PROFILE PAGE
# -----------------------------
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES["profile_photo"]

        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "accounts/edit_profile.html", {"profile": profile})


# -----------------------------
# PROFILE PAGE
# -----------------------------
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {"profile": profile, "form": form},
    )


# -----------------------------
# LOGIN
# -----------------------------
def login_user(request):
    if "next" in request.GET:
        messages.warning(request, "You must login first.")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Make sure profile exists even for old accounts
            Profile.objects.get_or_create(user=user)

            messages.success(request, "Login successful.")
            return redirect(request.GET.get("next", "products"))

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -----------------------------
# LOGOUT
# -----------------------------
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("products")
