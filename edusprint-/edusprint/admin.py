from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

class EduSprintAdminSite(AdminSite):
    site_header = "🎓 EduSprint Administration"
    site_title = "EduSprint Admin Portal"
    index_title = "Welcome to EduSprint Administration"
    
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request)
        
        # Add custom statistics to the admin index
        if request.path == reverse('admin:index'):
            try:
                from users.models import CustomUser
                from portfolio.models import PortfolioItem, Category, Comment
                
                # Get statistics
                total_users = CustomUser.objects.count()
                total_portfolio_items = PortfolioItem.objects.count()
                total_categories = Category.objects.count()
                total_comments = Comment.objects.count()
                
                # Recent activity (last 7 days)
                recent_users = CustomUser.objects.filter(
                    date_joined__gte=timezone.now() - timedelta(days=7)
                ).count()
                recent_portfolio_items = PortfolioItem.objects.filter(
                    created_at__gte=timezone.now() - timedelta(days=7)
                ).count()
                recent_comments = Comment.objects.filter(
                    created_at__gte=timezone.now() - timedelta(days=7)
                ).count()
                
                # Status breakdowns
                pending_items = PortfolioItem.objects.filter(status='pending').count()
                approved_items = PortfolioItem.objects.filter(status='approved').count()
                featured_items = PortfolioItem.objects.filter(is_featured=True).count()
                pending_comments = Comment.objects.filter(is_approved=False).count()
                
                # Add statistics to the first app (users)
                if app_list:
                    app_list[0]['stats'] = {
                        'total_users': total_users,
                        'total_portfolio_items': total_portfolio_items,
                        'total_categories': total_categories,
                        'total_comments': total_comments,
                        'recent_users': recent_users,
                        'recent_portfolio_items': recent_portfolio_items,
                        'recent_comments': recent_comments,
                        'pending_items': pending_items,
                        'approved_items': approved_items,
                        'featured_items': featured_items,
                        'pending_comments': pending_comments,
                    }
            except Exception:
                pass
        
        return app_list

# Create custom admin site instance
admin_site = EduSprintAdminSite(name='edusprint_admin')

# Import and register models
try:
    from users.models import CustomUser
    from users.admin import CustomUserAdmin
    from portfolio.models import PortfolioItem, Category, Comment
    from portfolio.admin import PortfolioItemAdmin, CategoryAdmin, CommentAdmin
    
    admin_site.register(CustomUser, CustomUserAdmin)
    admin_site.register(PortfolioItem, PortfolioItemAdmin)
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(Comment, CommentAdmin)
except ImportError:
    pass 