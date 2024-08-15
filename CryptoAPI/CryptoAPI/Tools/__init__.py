from enum import Enum

# ADMINS content
roles = ["Owner", "Manager", "Administrator", "Moderator", "Developer", "User"]


# ENUMS
class Roles(Enum):
    OWNER = 'Owner'
    MANAGER = 'Manager'
    ADMIN = 'Administrator'
    MODERATOR = 'Moderator'
    DEVELOPER = 'Developer'
    USER = 'User'
