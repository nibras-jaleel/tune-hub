from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Vehicle, Upgrade, SimulationResult

# ---------------- Home ----------------
def home(request):
    return render(request, 'home.html')

# ---------------- Signup ----------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long!")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # 🟢 IMPORTANT: Log the user in after signup
        auth_login(request, user)
        
        messages.success(request, "Account created successfully!")
        return redirect("user_dashboard")  # Now they're logged in

    return render(request, "signup.html")

# ---------------- Login ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            next_url = request.GET.get('next') or 'user_dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")
    return render(request, 'login.html')

# ---------------- Logout ----------------
def logout_view(request):
    auth_logout(request)
    return redirect("home")

# ---------------- Vehicles Page ----------------
@login_required
def vehicles(request):
    # 🟢 FIXED: Get only the logged-in user's vehicles
    vehicles_list = Vehicle.objects.filter(user=request.user).order_by('-id')
    return render(request, 'vehicle.html', {"vehicles": vehicles_list})

# ---------------- User Dashboard ----------------
@login_required
def user_dashboard(request):
    # 🟢 Get only this user's data
    vehicles = Vehicle.objects.filter(user=request.user)
    simulation_results = SimulationResult.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Calculate statistics
    total_vehicles = vehicles.count()
    total_simulations = simulation_results.count()
    
    # Get the most powerful vehicle (run a fresh query)
    most_powerful = SimulationResult.objects.filter(user=request.user).order_by('-new_horsepower').first()
    
    context = {
        'vehicles': vehicles,
        'simulation_results': simulation_results,
        'total_vehicles': total_vehicles,
        'total_simulations': total_simulations,
        'most_powerful': most_powerful,
    }
    return render(request, 'dashboard.html', context)


# ---------------- Tuning Simulation ----------------
@login_required
def tune(request):
    # 🟢 Get only this user's vehicles
    vehicles = Vehicle.objects.filter(user=request.user)
    selected_vehicle = None
    result = None

    # Step 1: Select vehicle
    if request.method == "POST" and "select_vehicle" in request.POST:
        vehicle_id = request.POST.get("vehicle")
        if vehicle_id:
            selected_vehicle = Vehicle.objects.get(id=vehicle_id, user=request.user)

    # Step 2: Tune vehicle
    elif request.method == "POST" and "tune_vehicle" in request.POST:
        vehicle_id = request.POST.get("vehicle_id")
        selected_vehicle = Vehicle.objects.get(id=vehicle_id, user=request.user)

        engine = request.POST.get("engine")
        exhaust = request.POST.get("exhaust")
        suspension = request.POST.get("suspension")
        tires = request.POST.get("tires")

        horsepower = selected_vehicle.base_hp
        torque = selected_vehicle.base_torque
        efficiency = 70

        # Tuning logic
        if engine == "stage1":
            horsepower += 50
        elif engine == "stage2":
            horsepower += 100
        elif engine == "v8":
            horsepower += 200

        if exhaust == "performance":
            torque += 20
        elif exhaust == "racing":
            torque += 40

        if suspension == "sport":
            efficiency += 5
        elif suspension == "race":
            efficiency += 10

        if tires == "sport":
            efficiency += 5
        elif tires == "slick":
            efficiency += 10

        # Create simulation result
        result = SimulationResult.objects.create(
            user=request.user,
            vehicle=selected_vehicle,
            new_horsepower=horsepower,
            new_torque=torque,
            new_efficiency=efficiency,
        )

        # Redirect to results page
        return redirect('tune_results', result_id=result.id)

    context = {
        "vehicles": vehicles,
        "selected_vehicle": selected_vehicle,
        "result": result,
    }
    return render(request, "tune.html", context)

# ---------------- Tune Results ----------------
@login_required
def tune_results(request, result_id):
    # 🟢 Get the simulation result for this user only
    result = get_object_or_404(SimulationResult, id=result_id, user=request.user)
    
    context = {
        'result': result,
    }
    return render(request, 'tune_results.html', context)

# ---------------- User Profile ----------------
@login_required
def profile(request):
    if request.method == "POST":
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        
        profile = request.user.profile
        profile.bio = bio
        profile.location = location
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "profile.html", {"profile": request.user.profile})

# ----------------- User Profile View ----------------
@login_required
def profile_view(request):
    return render(request, "profile.html")

# ---------------- Upgrade History ----------------
@login_required 
def history(request):
    # 🟢 Get only this user's history
    history = SimulationResult.objects.filter(user=request.user).order_by("-date")
    return render(request, "history.html", {"history": history})

# ---------------- Vehicle Detail ----------------
@login_required
def vehicle_detail(request, vehicle_id):
    # 🟢 Get vehicle only if it belongs to this user
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, user=request.user)
    upgrades = Upgrade.objects.filter(vehicle=vehicle)
    return render(request, "vehicle_detail.html", {
        "vehicle": vehicle,
        "upgrades": upgrades,
    })

# ---------------- Upgrade Detail ----------------
@login_required
def upgrade_detail(request, upgrade_id):
    upgrade = get_object_or_404(Upgrade, id=upgrade_id)
    return render(request, "upgrade_detail.html", {"upgrade": upgrade})

# ---------------- Add Vehicle View ----------------
@login_required
def add_vehicle_view(request):
    if request.method == "POST":
        brand = request.POST.get("brand")
        name = request.POST.get("name")
        v_type = request.POST.get("type")
        base_hp = request.POST.get("base_hp")
        base_torque = request.POST.get("base_torque")

        if not (brand and name and v_type and base_hp and base_torque):
            messages.error(request, "All fields are required!")
            return redirect("add_vehicle")

        # 🟢 Assign logged-in user here
        Vehicle.objects.create(
            user=request.user,
            name=f"{brand} {name}",  # Combine brand and name
            type=v_type,
            base_hp=base_hp,
            base_torque=base_torque,
        )

        messages.success(request, f"Vehicle {brand} {name} added successfully!")
        return redirect("vehicles")  # Redirect to vehicles page to see the new vehicle

    return render(request, "add_vehicle.html")



