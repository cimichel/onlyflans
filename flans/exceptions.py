class FlanServiceError(Exception):
    """Base exception for flan service errors"""
    pass


class FlanNotFoundError(FlanServiceError):
    """Raised when a flan is not found"""

    def __init__(self, flan_id: int):
        self.flan_id = flan_id
        super().__init__(f"Flan with ID {flan_id} not found")


class InvalidFlanDataError(FlanServiceError):
    """Raised when flan data validation fails"""

    def __init__(self, errors: list):
        self.errors = errors
        super().__init__(f"Invalid flan data: {', '.join(errors)}")


class EmailServiceError(Exception):
    """Base exception for email service errors"""
    pass


class InvalidEmailTemplateError(EmailServiceError):
    """Raised when email template context is invalid"""

    def __init__(self, missing_keys: list):
        self.missing_keys = missing_keys
        super().__init__(
            f"Email template missing required keys: {missing_keys}")


class SubscriptionError(Exception):
    """Base exception for subscription errors"""
    pass


class DuplicateSubscriberError(SubscriptionError):
    """Raised when trying to create a duplicate subscriber"""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Subscriber with email {email} already exists")


class AnalyticsServiceError(Exception):
    """Base exception for analytics service errors"""
    pass
