import rules

from organizations.rules import is_related_org_user

model_names = ['location', 'dropofftime', 'donationfulfillment', 'manualdropoffdate', 'donationrequest']

for model_name in model_names:
    rules.add_perm('donations.add_{}'.format(model_name), is_related_org_user)
    rules.add_perm('donations.read_{}'.format(model_name), is_related_org_user)
    rules.add_perm('donations.remove_{}'.format(model_name), is_related_org_user)
    rules.add_perm('donations.change_{}'.format(model_name), is_related_org_user)
