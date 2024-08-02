resource "aws_organizations_organization" "org" {
  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com",
  ]

  feature_set = "ALL"
}

resource "aws_organizations_organizational_unit" "ou_dev" {
  name      = "Development"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_organizational_unit" "ou_prod" {
  name      = "Production"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_account" "dev_account" {
  name      = "DevAccount"
  email     = "ooliinykvladislav+productivity-rate-dev@gmail.com"
  role_name = "OrganizationAccountAccessRole"
  parent_id = aws_organizations_organizational_unit.ou_dev.id
  lifecycle {
    ignore_changes = [role_name]
  }
  depends_on = [aws_organizations_organization.org]
}

resource "aws_organizations_account" "prod_account" {
  name      = "ProdAccount"
  email     = "ooliinykvladislav+productivity-rate-prod@gmail.com"
  role_name = "OrganizationAccountAccessRole"
  parent_id = aws_organizations_organizational_unit.ou_prod.id
  lifecycle {
    ignore_changes = [role_name]
  }
  depends_on = [aws_organizations_organization.org]
}
