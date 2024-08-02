resource "aws_iam_user" "admin" {
  name = "admin"
}

resource "aws_iam_user_login_profile" "admin_login_profile" {
  user                     = aws_iam_user.admin.name
  password_reset_required  = true
}

resource "aws_iam_policy_attachment" "admin_policy_attachment" {
  name       = "admin_policy_attachment"
  users      = [aws_iam_user.admin.name]
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# ////////////

resource "aws_iam_user" "terraform_user" {
  name = "terraform_user"
}

resource "aws_iam_user_login_profile" "admin_login_profile" {
  user                     = aws_iam_user.terraform_user.name
  password_reset_required  = true
}

resource "aws_iam_policy_attachment" "admin_policy_attachment" {
  name       = "admin_policy_attachment"
  users      = [aws_iam_user.admin.name]
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

