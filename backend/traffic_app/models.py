from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.utils import timezone

class TrafficViolation(models.Model):
    """
    Model to store traffic violations reported by citizens or detected by cameras
    """
    VIOLATION_TYPES = [
        ('SPEEDING', 'Speeding'),
        ('SIGNAL_JUMP', 'Traffic Signal Jump'),
        ('PARKING', 'Invalid Parking'),
        ('LANE_CHANGE', 'Unsafe Lane Change'),
        ('NO_HELMET', 'No Helmet'),
        ('RASH_DRIVING', 'Rash Driving'),
        ('OTHER', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    violation_id = models.CharField(max_length=50, unique=True, db_index=True)
    violator_name = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=20, db_index=True)
    violation_type = models.CharField(max_length=20, choices=VIOLATION_TYPES)
    severity = models.IntegerField(choices=SEVERITY_LEVELS, default=1)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField()
    violation_time = models.DateTimeField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations_reported')
    reported_at = models.DateTimeField(auto_now_add=True)
    evidence_image = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='violations_verified')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['vehicle_number', '-reported_at']),
            models.Index(fields=['violation_type', '-reported_at']),
        ]
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.violation_type}"


class UserProfile(models.Model):
    """
    Extended user profile with gamification features
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    violations_count = models.IntegerField(default=0)
    reports_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    badge_level = models.IntegerField(default=1)  # Bronze=1, Silver=2, Gold=3, Platinum=4
    driver_license = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.URLField(null=True, blank=True)
    is_verified_driver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-points']
        indexes = [
            models.Index(fields=['-points']),
            models.Index(fields=['badge_level']),
        ]
    
    def __str__(self):
        return f"{self.user.username} (Points: {self.points})"
    
    def calculate_badge_level(self):
        """Calculate badge level based on points"""
        if self.points >= 5000:
            self.badge_level = 4  # Platinum
        elif self.points >= 3000:
            self.badge_level = 3  # Gold
        elif self.points >= 1000:
            self.badge_level = 2  # Silver
        else:
            self.badge_level = 1  # Bronze
        return self.badge_level


class TrafficReport(models.Model):
    """
    User reports of traffic violations (Peer-to-Peer reporting)
    """
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    report_id = models.CharField(max_length=50, unique=True, db_index=True)
    violation = models.ForeignKey(TrafficViolation, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='traffic_reports')
    description = models.TextField()
    evidence_urls = models.JSONField(default=list)  # Store multiple image URLs
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')
    review_comments = models.TextField(blank=True)
    reward_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
        ]
    
    def __str__(self):
        return f"Report {self.report_id} - {self.status}"


class Fine(models.Model):
    """
    Fine calculation model with intelligent adjustment algorithm
    """
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('WAIVED', 'Waived'),
    ]
    
    fine_id = models.CharField(max_length=50, unique=True, db_index=True)
    violation = models.OneToOneField(TrafficViolation, on_delete=models.CASCADE, related_name='fine')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    severity_multiplier = models.FloatField(default=1.0, validators=[MinValueValidator(0.5), MaxValueValidator(4.0)])
    repeat_offender_multiplier = models.FloatField(default=1.0, validators=[MinValueValidator(1.0), MaxValueValidator(3.0)])
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount_after_discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_status', 'due_date']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Fine {self.fine_id} - {self.final_amount}"
    
    def calculate_fine(self, vehicle_number):
        """
        Intelligent fine calculation algorithm
        Considers: severity, repeat offenses, and other factors
        """
        # Count repeat offenses in last 6 months
        six_months_ago = timezone.now() - timedelta(days=180)
        repeat_violations = TrafficViolation.objects.filter(
            vehicle_number=vehicle_number,
            violation_time__gte=six_months_ago
        ).count()
        
        # Calculate multipliers
        self.severity_multiplier = 1.0 + (self.violation.severity * 0.5)
        self.repeat_offender_multiplier = max(1.0, 1.0 + (repeat_violations * 0.2))
        
        # Calculate final amount
        self.final_amount = self.base_amount * self.severity_multiplier * self.repeat_offender_multiplier
        
        # Apply discount if repeat violations are high (rehabilitation chance)
        if repeat_violations >= 5:
            self.discount_percentage = 10
            self.amount_after_discount = self.final_amount * (1 - self.discount_percentage / 100)
        else:
            self.discount_percentage = 0
            self.amount_after_discount = self.final_amount
        
        return self.amount_after_discount
    
    @property
    def is_overdue(self):
        """Check if fine is overdue"""
        return self.payment_status == 'PENDING' and self.due_date < timezone.now().date()


class Leaderboard(models.Model):
    """
    Leaderboard for gamification - refreshed daily
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    rank = models.IntegerField()
    points = models.IntegerField()
    reports_submitted = models.IntegerField()
    verified_reports = models.IntegerField()
    badge_level = models.IntegerField()
    date = models.DateField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['rank']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['date', 'rank']),
        ]
    
    def __str__(self):
        return f"Rank {self.rank} - {self.user.username}"


class Notification(models.Model):
    """
    Notifications for users about their violations, fines, and achievements
    """
    NOTIFICATION_TYPES = [
        ('VIOLATION', 'Violation Reported'),
        ('FINE', 'Fine Generated'),
        ('PAYMENT', 'Payment Reminder'),
        ('ACHIEVEMENT', 'Achievement Unlocked'),
        ('ALERT', 'System Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_violation = models.ForeignKey(TrafficViolation, on_delete=models.SET_NULL, null=True, blank=True)
    related_fine = models.ForeignKey(Fine, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
