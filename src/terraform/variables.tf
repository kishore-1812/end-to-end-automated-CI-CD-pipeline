variable "aws_region" {
  description = "AWS region for deployment"
  default     = "eu-north-1"
}
variable "vpc_cidr" {
  default     = "10.0.0.0/16"
  description = "CIDR block for VPC"
}
variable "public_subnet_cidr" {
  default     = "10.0.1.0/24"
  description = "Public subnet for FastAPI"
}
variable "private_subnet_cidr" {
  default     = "10.0.2.0/24"
  description = "Private subnet for Wazuh"
}
variable "instance_type" {
  default     = "t3.micro"
  description = "Instance type for EC2"
}
variable "ssh_key_name" {
  description = "Name of AWS EC2 Key Pair"
}

variable "admin_ip" {
  default = "109.134.247.65/32"
  description = "Admin IP"
}