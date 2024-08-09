# 🎉 Welcome to Productivity Rate Infra! 🎉

terramate create --all-terraform

git add .
terramate run --changed terraform init
terramate run --changed terraform plan
terramate run --changed terraform apply -auto-approve
terramate run --changed terraform destroy -auto-approve

terramate run terraform destroy -auto-approve  
terramate run terraform apply -auto-approve

terramate --chdir infra/stacks/dev/ecr run -- terraform init
terramate --chdir infra/stacks/dev/ecr run -- terraform apply -auto-approve
terramate --chdir infra/stacks/dev/ecr run -- terraform destroy -auto-approve

aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 014498641718.dkr.ecr.eu-north-1.amazonaws.com
