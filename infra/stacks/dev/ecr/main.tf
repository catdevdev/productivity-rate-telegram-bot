terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.37"
    }
  }
}

provider "aws" {
  region  = "eu-north-1"
  profile = "dev"
}

# Create ECR Repository
resource "aws_ecr_repository" "my_repository" {
  name = "bot-repo"
}

# Create ECR Lifecycle Policy
resource "aws_ecr_lifecycle_policy" "my_repository_policy" {
  repository = aws_ecr_repository.my_repository.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Limit to 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}


resource "aws_ecr_repository" "expenses-repository" {
  name = "expenses-repo"
}

# Create ECR Lifecycle Policy
resource "aws_ecr_lifecycle_policy" "expenses-repository_policy" {
  repository = aws_ecr_repository.expenses-repository.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Limit to 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
