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

# Define the IAM policy for EBS CSI Driver permissions
resource "aws_iam_policy" "ebs_csi_driver_policy" {
  name        = "EBSCSIDriverPolicy"
  description = "IAM policy for EBS CSI Driver to manage EBS volumes"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateVolume",
          "ec2:AttachVolume",
          "ec2:DetachVolume",
          "ec2:DeleteVolume",
          "ec2:DescribeInstances",
          "ec2:DescribeVolumes",
          "ec2:DescribeVolumeAttribute",
          "ec2:DescribeVolumeStatus",
          "ec2:DescribeSnapshots",
          "ec2:CreateTags",
          "ec2:DeleteTags"
        ],
        Resource = "*"
      }
    ]
  })
}

# Fetch the existing IAM role associated with your EKS node group
data "aws_iam_role" "eks_node_role" {
  name = "karpenter-eks-node-group-20240809013028374400000003" # Replace with your actual role name
}

# Attach the policy to the existing IAM role
resource "aws_iam_role_policy_attachment" "attach_ebs_csi_policy" {
  role       = data.aws_iam_role.eks_node_role.name
  policy_arn = aws_iam_policy.ebs_csi_driver_policy.arn
}
