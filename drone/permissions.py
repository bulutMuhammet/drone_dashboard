from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners (team members) of a part to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Parçanın takımı ile kullanıcının takımı aynı mı?
        return obj.part.team == request.user.staff.team


class IsAssemblyTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff.team.is_assembler

