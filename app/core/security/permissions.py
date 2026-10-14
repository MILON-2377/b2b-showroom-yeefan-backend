class Permissions:
    ACCOUNT_READ_SELF = "account:read_self"
    ACCOUNT_UPDATE_SELF = "account:update_self"
    ACCOUNT_CHANGE_PASSWORD = "account:change_password"

    SESSION_READ_SELF = "session:read_self"
    SESSION_REVOKE_SELF = "session:revoke_self"
    SESSION_REVOKE_OTHERS = "session:revoke_others"

    USER_READ = "user:read"
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_ACTIVATE = "user:activate"
    USER_DEACTIVATE = "user:deactivate"
    USER_RESET_PASSWORD = "user:reset_password"
    USER_REVOKE_SESSIONS = "user:revoke_sessions"

    BRAND_READ = "brand:read"
    BRAND_MANAGE = "brand:manage"

    COLLECTION_READ = "collection:read"
    COLLECTION_MANAGE = "collection:manage"

    CATEGORY_READ = "category:read"
    CATEGORY_MANAGE = "category:manage"

    PRODUCT_READ = "product:read"
    PRODUCT_MANAGE = "product:manage"

    MEDIA_UPLOAD = "media:upload"

    INQUIRY_READ = "inquiry:read"
    INQUIRY_MANAGE = "inquiry:manage"
