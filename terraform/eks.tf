# Grab the default AWS network (VPC) so we don't have to build one from scratch
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ==========================================
# 1. IAM Role for the EKS Cluster (The Brain)
# ==========================================
resource "aws_iam_role" "eks_cluster_role" {
  name = "uptime-monitor-eks-cluster-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

# ==========================================
# 2. The EKS Cluster itself
# ==========================================
resource "aws_eks_cluster" "uptime_cluster" {
  name     = "uptime-monitor-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = data.aws_subnets.default.ids
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]
}

# ==========================================
# 3. IAM Role for the Worker Nodes (The Muscle)
# ==========================================
resource "aws_iam_role" "eks_node_role" {
  name = "uptime-monitor-eks-node-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# Give the nodes permission to talk to the cluster, network, and ECR vault
resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}
resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}
resource "aws_iam_role_policy_attachment" "ecr_read_only" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

# ==========================================
# 4. The Worker Nodes (EC2 machines managed by EKS)
# ==========================================
resource "aws_eks_node_group" "uptime_nodes" {
  cluster_name    = aws_eks_cluster.uptime_cluster.name
  node_group_name = "uptime-monitor-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = data.aws_subnets.default.ids

  instance_types = ["t3.micro"] # Smallest recommended size for EKS

  scaling_config {
    desired_size = 2 # We want 2 machines running for High Availability!
    max_size     = 2
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ecr_read_only,
  ]
}

# Output the cluster name so we can configure our laptop to talk to it later
output "eks_cluster_name" {
  value = aws_eks_cluster.uptime_cluster.name
}