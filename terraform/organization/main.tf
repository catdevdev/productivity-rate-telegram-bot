terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "eu-north-1"
  profile = "root"
}

# module "org" {
#   source = "./modules/org"
# }

module "admin_user" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-user"

  name          = "admin_user"
  force_destroy = true

  create_iam_user_login_profile = true 

  password_reset_required = true

  policy_arns = [
    "arn:aws:iam::aws:policy/AdministratorAccess",
  ]
}

module "terraform_user" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-user"

  name          = "terraform_user"
  force_destroy = true

  create_iam_user_login_profile = false
  create_iam_access_key         = true

  policy_arns = [
    "arn:aws:iam::aws:policy/AdministratorAccess",
  ]
}

