from app.core.security.permissions import Permissions
from app.modules.auth.models.user import UserRole

ROLE_PERMISSIONS: dict[UserRole, frozenset[str]] = {
    UserRole.ADMIN: frozenset(
        {
            # Account
            Permissions.ACCOUNT_READ_SELF,
            Permissions.ACCOUNT_UPDATE_SELF,
            Permissions.ACCOUNT_CHANGE_PASSWORD,
            # Sessions
            Permissions.SESSION_READ_SELF,
            Permissions.SESSION_REVOKE_SELF,
            # Showroom: brands, collections, categories, products
            Permissions.BRAND_READ,
            Permissions.BRAND_MANAGE,
            Permissions.COLLECTION_READ,
            Permissions.COLLECTION_MANAGE,
            Permissions.CATEGORY_READ,
            Permissions.CATEGORY_MANAGE,
            Permissions.PRODUCT_READ,
            Permissions.PRODUCT_MANAGE,
            # Media
            Permissions.MEDIA_UPLOAD,
            # Inquiries
            Permissions.INQUIRY_READ,
            Permissions.INQUIRY_MANAGE,
            # Reviews
            Permissions.REVIEW_READ,
            Permissions.REVIEW_MANAGE,
            # Dashboard
            Permissions.DASHBOARD_READ,
            # Company knowledge
            Permissions.COMPANY_KNOWLEDGE_READ,
            Permissions.COMPANY_KNOWLEDGE_MANAGE,
            # Catalogs
            Permissions.CATALOG_READ,
            Permissions.CATALOG_MANAGE,
            # About videos
            Permissions.ABOUT_VIDEO_READ,
            Permissions.ABOUT_VIDEO_MANAGE,
        }
    ),
    UserRole.SUPER_ADMIN: frozenset(
        {
            # Account
            Permissions.ACCOUNT_READ_SELF,
            Permissions.ACCOUNT_UPDATE_SELF,
            Permissions.ACCOUNT_CHANGE_PASSWORD,
            # Sessions
            Permissions.SESSION_READ_SELF,
            Permissions.SESSION_REVOKE_SELF,
            Permissions.SESSION_REVOKE_OTHERS,
            # User management
            Permissions.USER_READ,
            Permissions.USER_CREATE,
            Permissions.USER_UPDATE,
            Permissions.USER_ACTIVATE,
            Permissions.USER_DEACTIVATE,
            Permissions.USER_RESET_PASSWORD,
            Permissions.USER_REVOKE_SESSIONS,
            # Showroom
            Permissions.BRAND_READ,
            Permissions.BRAND_MANAGE,
            Permissions.COLLECTION_READ,
            Permissions.COLLECTION_MANAGE,
            Permissions.CATEGORY_READ,
            Permissions.CATEGORY_MANAGE,
            Permissions.PRODUCT_READ,
            Permissions.PRODUCT_MANAGE,
            # Media
            Permissions.MEDIA_UPLOAD,
            # Inquiries
            Permissions.INQUIRY_READ,
            Permissions.INQUIRY_MANAGE,
            # Reviews
            Permissions.REVIEW_READ,
            Permissions.REVIEW_MANAGE,
            # Dashboard
            Permissions.DASHBOARD_READ,
            # Company knowledge
            Permissions.COMPANY_KNOWLEDGE_READ,
            Permissions.COMPANY_KNOWLEDGE_MANAGE,
            # Catalogs
            Permissions.CATALOG_READ,
            Permissions.CATALOG_MANAGE,
            # About videos
            Permissions.ABOUT_VIDEO_READ,
            Permissions.ABOUT_VIDEO_MANAGE,
        }
    ),
}
