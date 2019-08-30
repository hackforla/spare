import rules


@rules.predicate
def is_related_org_user(user, obj):
    if obj:
        return obj.get_related_org() == user.org

    return user.is_org_user
