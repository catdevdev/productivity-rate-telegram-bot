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

# IAM Policy for EBS CSI Driver
resource "aws_iam_policy" "ebs_csi_policy" {
  name        = "AmazonEKS_EBS_CSI_Driver_Policy"
  description = "Policy for EBS CSI Driver to access EBS resources"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateVolume",
          "ec2:AttachVolume",
          "ec2:DetachVolume",
          "ec2:DeleteVolume",
          "ec2:CreateSnapshot",
          "ec2:DeleteSnapshot",
          "ec2:DescribeVolumes",
          "ec2:DescribeSnapshots",
          "ec2:DescribeInstances",
          "ec2:DescribeAvailabilityZones",
          "ec2:DescribeVolumeStatus",
          "ec2:DescribeVolumeAttribute",
          "ec2:DescribeSnapshotAttribute",
          "ec2:DescribeInstanceAttribute",
          "ec2:DescribeInstanceCreditSpecifications",
          "ec2:DescribeVolumeTypes",
          "ec2:DescribeVpcAttribute",
          "ec2:DescribeVpcEndpoints",
          "ec2:DescribeVpcs",
          "ec2:ModifyVolume",
          "ec2:ModifyVolumeAttribute",
          "ec2:ModifyInstanceAttribute",
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach Policy to EKS Node Role
resource "aws_iam_role_policy_attachment" "eks_node_role_attachment" {
  policy_arn = aws_iam_policy.ebs_csi_policy.arn
  role       = "<EKS_NODE_ROLE_NAME>" # Replace with your EKS node role name
}