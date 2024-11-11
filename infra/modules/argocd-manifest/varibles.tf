variable "cluster_ca_certificate" {
  description = "The cluster CA certificate"
  type        = string
}

variable "cluster_name" {
  description = "The name of the Kubernetes cluster"
  type        = string
}

variable "cluster_endpoint" {
  description = "The endpoint of the Kubernetes cluster"
  type        = string
}
