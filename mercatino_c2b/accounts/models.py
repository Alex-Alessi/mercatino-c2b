from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20)

    @property
    def completed_sales(self):
        from proposals.models import ItemProposal
        
        return self.user.proposals.filter(
            status=ItemProposal.Status.COMPLETED
        ).count()
    
    @property
    def seller_badge(self):
        sales = self.completed_sales

        if sales >= 30:
            return "Top Venditore"
        elif sales >= 20:
            return "Venditore Oro"
        elif sales >= 10:
            return "Venditore Argento"
        elif sales >= 5:
            return "Venditore Bronzo"      
        return "Nuovo Venditore"
    
    @property
    def next_badge_progress(self):
        sales = self.completed_sales

        if sales < 5:
            return {
                "remaining": 5 - sales,
                "next_badge": "Venditore Bronzo",
            }
        elif sales < 10:
            return {
                "remaining": 10 - sales,
                "next_badge": "Venditore Argento",
            }
        elif sales < 20:
            return {
                "remaining": 20 - sales,
                "next_badge": "Venditore Oro",
            }
        elif sales < 30:
            return {
                "remaining": 30 - sales,
                "next_badge": "Top Venditore",
            }

        return None

    def __str__(self):
        return f"Profilo di {self.user.username}"