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

.PHONY: import
import:
	terraform import -backup=- aws_dynamodb_table.default spare-terraform
	terraform import -backup=- aws_s3_bucket.default spare-terraform
