# RANGS ROUTES
from .Owners import router as owners_routes
from .Admins import router as admins_routes
from .Moderators import router as moderation_routes

# GOODGUARD ROUTES
from .GoodGuard.GoodGuard import router as good_guard_routes

# USERS ROUTES
from .Users.Users import router as users_routes
from .user.endpoints import router as users_routes_v1

# BUCKET ROUTERS
from .Buckets.Buckets import router as bucket_routes