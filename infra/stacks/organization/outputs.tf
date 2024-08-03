output "admin_user_name" {
  description = "The admin user's name"
  value       = module.admin_user.iam_user_name
}

output "admin_user_login_profile_password" {
  description = "The admin user's password"
  value       = module.admin_user.iam_user_login_profile_password
  sensitive   = true
}

//

output "terraform_user_name" {
  description = "The terraform user's name"
  value       = module.terraform_user.iam_user_name
}

output "terraform_user_login_profile_password" {
  description = "The terraform user's password"
  value       = module.terraform_user.iam_user_login_profile_password
  sensitive   = true
}

output "terraform_user_login_iam_access_key_id" {
  description = "The terraform user's password"
  value       = module.terraform_user.iam_access_key_id
}

output "terraform_user_login_iam_access_key_secret" {
  description = "The terraform user's password"
  value       = module.terraform_user.iam_access_key_secret
  sensitive   = true
}
