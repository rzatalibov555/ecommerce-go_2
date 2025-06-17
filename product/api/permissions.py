from rest_framework.permissions import BasePermission
from product.models import Author  # uyğun modelini import et

class IsAuthorAuthenticated(BasePermission):
    """
    Custom permission to allow access only if the user is authenticated via Author model and session.
    """

    def has_permission(self, request, view):
        author_id = request.session.get("author_id")
        if not author_id:
            return False
        try:
            Author.objects.get(id=author_id)
            return True
        except Author.DoesNotExist:
            return False