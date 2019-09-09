import rules

from organizations.rules import is_org_user, is_related_org_user

model_names = ['user']

rules.add_perm('core', is_org_user)

for model_name in model_names:
    rules.add_perm('core.add_{}'.format(model_name), is_related_org_user)
    rules.add_perm('core.read_{}'.format(model_name), is_related_org_user)
    rules.add_perm('core.remove_{}'.format(model_name), is_related_org_user)
    rules.add_perm('core.change_{}'.format(model_name), is_related_org_user)
