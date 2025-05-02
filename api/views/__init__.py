# Import all views from their respective modules
from .basic_views import HealthCheckView
from .user_views import UserView, UsersView, FollowingNetworkView, UserProfileView, UserFollowingView
from .auth_views import AuthView, AuthTestView, SpotifyAuthView
from .albums_views import AlbumView, AlbumsRatingView, AlbumRatingsView, AlbumUserRatingView
from .ratings_views import RatingsView
from .feed_views import FeedView
from .user_complete_profile_view import UserCompleteProfileView

# Export all view classes
__all__ = [
    'HealthCheckView',
    'UserView',
    'UsersView',
    'AuthView',
    'AuthTestView',
    'SpotifyAuthView',
    'FollowingNetworkView',
    'UserProfileView',
    'UserFollowingView',
    'AlbumView',
    'AlbumsRatingView',
    'AlbumRatingsView',
    'AlbumUserRatingView',
    'RatingsView',
    'FeedView',
    'UserCompleteProfileView'
]