from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

from .models import (
    TrafficViolation, UserProfile, TrafficReport,
    Fine, Leaderboard, Notification
)
from .serializers import (
    TrafficViolationSerializer, UserProfileSerializer, TrafficReportSerializer,
    FineSerializer, LeaderboardSerializer, NotificationSerializer,
    ViolationDetailSerializer, UserSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ViolationViewSet(viewsets.ModelViewSet):
    """ViewSet for Traffic Violations"""
    queryset = TrafficViolation.objects.all()
    serializer_class = TrafficViolationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['violation_type', 'severity', 'is_verified']
    search_fields = ['vehicle_number', 'violator_name', 'location']
    ordering_fields = ['reported_at', 'severity']
    ordering = ['-reported_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ViolationDetailSerializer
        return TrafficViolationSerializer
    
    @action(detail=True, methods=['post'])
    def verify_violation(self, request, pk=None):
        """Verify a traffic violation"""
        violation = self.get_object()
        violation.is_verified = True
        violation.verified_by = request.user
        violation.verified_at = timezone.now()
        violation.save()
        return Response({'status': 'violation verified'})
    
    @action(detail=False, methods=['get'])
    def pending_review(self, request):
        """Get violations pending verification"""
        violations = self.queryset.filter(is_verified=False)
        page = self.paginate_queryset(violations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(violations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get violation statistics"""
        total = self.queryset.count()
        verified = self.queryset.filter(is_verified=True).count()
        by_type = self.queryset.values('violation_type').annotate(count=Count('id'))
        by_severity = self.queryset.values('severity').annotate(count=Count('id'))
        return Response({
            'total': total,
            'verified': verified,
            'pending': total - verified,
            'by_type': list(by_type),
            'by_severity': list(by_severity)
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['points', 'badge_level']
    ordering = ['-points']
    
    @action(detail=True, methods=['post'])
    def add_points(self, request, pk=None):
        """Add points to user profile"""
        profile = self.get_object()
        points = request.data.get('points', 0)
        profile.points += points
        profile.calculate_badge_level()
        profile.save()
        return Response({
            'points': profile.points,
            'badge_level': profile.badge_level
        })
    
    @action(detail=False, methods=['get'])
    def top_contributors(self, request):
        """Get top contributors by reports"""
        top = self.queryset.order_by('-reports_count')[:10]
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get overall leaderboard"""
        limit = request.query_params.get('limit', 50)
        top = self.queryset.order_by('-points')[:int(limit)]
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)


class TrafficReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Traffic Reports (P2P Reporting)"""
    serializer_class = TrafficReportSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'violation']
    ordering_fields = ['submitted_at', 'reward_points']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        return TrafficReport.objects.all()
    
    @action(detail=True, methods=['post'])
    def approve_report(self, request, pk=None):
        """Approve a report and award points"""
        report = self.get_object()
        reward = request.data.get('reward', 50)
        
        report.status = 'APPROVED'
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.reward_points = reward
        report.save()
        
        # Add points to reporter
        profile = report.reporter.profile
        profile.points += reward
        profile.reports_count += 1
        profile.calculate_badge_level()
        profile.save()
        
        return Response({'status': 'report approved', 'reward_points': reward})
    
    @action(detail=True, methods=['post'])
    def reject_report(self, request, pk=None):
        """Reject a report"""
        report = self.get_object()
        reason = request.data.get('reason', '')
        
        report.status = 'REJECTED'
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.review_comments = reason
        report.save()
        
        return Response({'status': 'report rejected'})
    
    @action(detail=False, methods=['get'])
    def pending_reviews(self, request):
        """Get pending reports for review"""
        reports = TrafficReport.objects.filter(status='SUBMITTED')
        page = self.paginate_queryset(reports)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)


class FineViewSet(viewsets.ModelViewSet):
    """ViewSet for Fine Management"""
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['payment_status']
    ordering_fields = ['final_amount', 'due_date', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Mark fine as paid"""
        fine = self.get_object()
        fine.payment_status = 'PAID'
        fine.paid_date = timezone.now().date()
        fine.payment_method = request.data.get('payment_method', 'online')
        fine.transaction_id = request.data.get('transaction_id', '')
        fine.save()
        return Response({'status': 'fine marked as paid'})
    
    @action(detail=False, methods=['get'])
    def overdue_fines(self, request):
        """Get overdue fines"""
        overdue = self.queryset.filter(
            payment_status='PENDING',
            due_date__lt=timezone.now().date()
        )
        page = self.paginate_queryset(overdue)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def revenue_report(self, request):
        """Get revenue statistics"""
        total_fines = self.queryset.aggregate(Sum('final_amount'))['final_amount__sum'] or 0
        paid_fines = self.queryset.filter(payment_status='PAID').aggregate(
            Sum('amount_after_discount')
        )['amount_after_discount__sum'] or 0
        pending = self.queryset.filter(payment_status='PENDING').count()
        return Response({
            'total_fine_amount': total_fines,
            'collected_amount': paid_fines,
            'pending_count': pending
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard (Read-only)"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'points']
    ordering = ['rank']
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's leaderboard"""
        today = timezone.now().date()
        leaderboard = self.queryset.filter(date=today).order_by('rank')
        page = self.paginate_queryset(leaderboard)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Notifications"""
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'status': 'all notifications marked as read'})
