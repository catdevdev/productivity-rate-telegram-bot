# 🎉 Welcome to Productivity Rate Infra! 🎉

git add .
terramate run --changed terraform init
terramate run --changed terraform plan
terramate run --changed terraform apply -auto-approve
terramate run --changed terraform destroy -auto-approve

terramate run terraform destroy -auto-approve  
terramate run terraform apply -auto-approve
