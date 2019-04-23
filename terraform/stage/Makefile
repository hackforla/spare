# By default, setup and plan, but don't make any changes
all: setup plan

.PHONY: init
init:
	terraform init

.PHONY: setup
setup:
	terraform get

.PHONY: plan
plan:
	terraform plan

.PHONY: apply
apply:
	terraform apply

.PHONY: destroy
destroy:
	terraform destroy
