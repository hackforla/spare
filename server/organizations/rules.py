import rules
from rules.predicates import is_superuser


@rules.predicate
def is_related_org_user(user, obj):
    if obj:
        return obj.get_related_org() == user.org

    return user.is_org_user


@rules.predicate
def has_org_permissions(user, obj):
    if obj:
        return obj == user.org

    if user.is_authenticated():
        return user.is_org_user

    return False


@rules.predicate
def is_org_user(user):
    if user.is_authenticated():
        return user.is_org_user

    return False


rules.add_perm('organizations', is_org_user)

rules.add_perm('organizations.add_org', is_superuser)
rules.add_perm('organizations.read_org', has_org_permissions)
rules.add_perm('organizations.remove_org', is_superuser)
rules.add_perm('organizations.change_org', has_org_permissions)

rules.add_perm('organizations.add_orguserrole', is_related_org_user)
rules.add_perm('organizations.read_orguserrole', is_related_org_user)
rules.add_perm('organizations.remove_orguserrole', is_related_org_user)
rules.add_perm('organizations.change_orguserrole', is_related_org_user)
