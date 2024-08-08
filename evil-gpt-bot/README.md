# 🎉 Welcome to Productivity Rate Bot! 🎉

source venv/bin/activate

aws ecr get-login-password --region eu-north-1 --profile dev | docker login --username AWS --password-stdin 014498641718.dkr.ecr.eu-north-1.amazonaws.com
docker build -t bot-repo .
docker tag bot-repo:latest 014498641718.dkr.ecr.eu-north-1.amazonaws.com/bot-repo:latest
docker push 014498641718.dkr.ecr.eu-north-1.amazonaws.com/bot-repo:latest
