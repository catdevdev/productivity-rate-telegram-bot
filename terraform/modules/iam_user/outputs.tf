# modules/iam_users/outputs.tf
output "terraform_access_key_id" {
  value = aws_iam_access_key.terraform_access_key.id
}

output "terraform_secret_access_key" {
  value     = aws_iam_access_key.terraform_access_key.secret
  sensitive = true
}


output "encrypted_secret_key_admin" {
  value = aws_iam_access_key.admin.encrypted_secret
}

output "access_key_admin" {
  value = aws_iam_access_key.admin.id
}



output "encrypted_secret_key_terraform" {
  value = aws_iam_access_key.terraform.encrypted_secret
}

output "access_key_terraform" {
  value = aws_iam_access_key.terraform.id
}