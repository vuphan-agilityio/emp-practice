"""Custom authorization functions."""
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class NoAccessAuthorization(Authorization):
    """User object only authorization."""

    def update_list(self, object_list, bundle):
        """Update list users."""
        raise Unauthorized("Sorry, no update by bundle.")

    def update_detail(self, object_list, bundle):
        """Update user details."""
        raise Unauthorized("Sorry, no update by bundle.")

    def delete_detail(self, object_list, bundle):
        """Delete user detail."""
        raise Unauthorized("Sorry, no delete by bundle.")

    def delete_list(self, object_list, bundle):
        """Delete list users."""
        raise Unauthorized("Sorry, no deletes by bundle")

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        raise Unauthorized("Sorry, no get by bundle.")
