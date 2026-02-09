from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    TrafficViolation, UserProfile, TrafficReport, 
    Fine, Leaderboard, Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badge_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'points', 'violations_count', 'reports_count',
            'badge_level', 'badge_name', 'driver_license', 'phone_number',
            'city', 'avatar', 'is_verified_driver', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'violations_count']
    
    def get_badge_name(self, obj):
        badges = {1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Platinum'}
        return badges.get(obj.badge_level, 'Bronze')


class TrafficViolationSerializer(serializers.ModelSerializer):
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)
    verified_by_username = serializers.CharField(source='verified_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = TrafficViolation
        fields = [
            'id', 'violation_id', 'violator_name', 'vehicle_number',
            'violation_type', 'severity', 'location', 'latitude', 'longitude',
            'description', 'violation_time', 'reported_by', 'reported_by_username',
            'reported_at', 'evidence_image', 'is_verified', 'verified_by',
            'verified_by_username', 'verified_at'
        ]
        read_only_fields = ['id', 'reported_at', 'verified_at']


class TrafficReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)
    violation = TrafficViolationSerializer(read_only=True)
    
    class Meta:
        model = TrafficReport
        fields = [
            'id', 'report_id', 'violation', 'reporter', 'reporter_username',
            'description', 'evidence_urls', 'status', 'submitted_at',
            'reviewed_at', 'reviewed_by', 'reviewed_by_username',
            'review_comments', 'reward_points'
        ]
        read_only_fields = ['id', 'submitted_at', 'reviewed_at', 'reward_points']


class FineSerializer(serializers.ModelSerializer):
    violation = TrafficViolationSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Fine
        fields = [
            'id', 'fine_id', 'violation', 'base_amount', 'severity_multiplier',
            'repeat_offender_multiplier', 'final_amount', 'discount_percentage',
            'amount_after_discount', 'payment_status', 'due_date', 'paid_date',
            'payment_method', 'transaction_id', 'created_at', 'updated_at',
            'notes', 'is_overdue'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_overdue']


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    badge_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user_id', 'username', 'rank', 'points',
            'reports_submitted', 'verified_reports', 'badge_level',
            'badge_name', 'date'
        ]
        read_only_fields = fields
    
    def get_badge_name(self, obj):
        badges = {1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Platinum'}
        return badges.get(obj.badge_level, 'Bronze')


class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_username', 'notification_type', 'title',
            'message', 'related_violation', 'related_fine', 'is_read',
            'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'created_at']


class ViolationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for a single violation including related reports and fine"""
    reported_by = UserSerializer(read_only=True)
    reports = TrafficReportSerializer(many=True, read_only=True)
    fine = FineSerializer(read_only=True)
    
    class Meta:
        model = TrafficViolation
        fields = [
            'id', 'violation_id', 'violator_name', 'vehicle_number',
            'violation_type', 'severity', 'location', 'latitude', 'longitude',
            'description', 'violation_time', 'reported_by', 'reported_at',
            'evidence_image', 'is_verified', 'reports', 'fine'
        ]
        read_only_fields = fields
