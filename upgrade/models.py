from django.db import models
from django.contrib.auth.models import User  
from django.db.models.signals import post_save
from django.dispatch import receiver
 

# ---------------- Vehicle Model ----------------
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # e.g. car, bike
    base_hp = models.IntegerField(default=100)
    base_torque = models.IntegerField(default=150)

    def __str__(self):
        return f"{self.name} ({self.type})"


# ---------------- Upgrade Model ----------------
class Upgrade(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    part = models.CharField(max_length=100)   # e.g. turbo, exhaust
    hp_gain = models.IntegerField()
    torque_gain = models.IntegerField()

    def __str__(self):
        return f"{self.part} (+{self.hp_gain}hp, +{self.torque_gain}Nm)"

# ---------------- SimulationResult Model ----------------
class SimulationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE, null=True, blank=True)  # Made optional
    new_horsepower = models.IntegerField()
    new_torque = models.IntegerField()
    new_efficiency = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)

# ---------------- Profile Model ----------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# ---------------- Signals ----------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
    





