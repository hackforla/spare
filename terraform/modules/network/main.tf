module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "1.60.0"

  name = "${var.name}"

  cidr = "${var.cidr}"

  azs             = "${var.azs}"
  private_subnets = "${var.private_subnets}"
  public_subnets  = "${var.public_subnets}"

  enable_nat_gateway = true
  enable_vpn_gateway = true
}
