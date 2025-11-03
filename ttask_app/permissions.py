def check_permission(user, item_name, action):
    if not user or not user.role:
        return False, {'error': "Unauthorized"}, 401
    try:
        perm = user.role.permission_set.get(item__name = item_name)
        if action == 'view' and perm.can_view:
            return True, None, 200
    except:
        pass
    return False, {'error': 'Forbidden'}, 403

def require_admin(user):
    if user and user.role and user.role.name =='admin':
        return True, None, 200
    return False, {'error': 'Admin only'}, 403