output "fastapi_public_ip" {
    value = aws_instance.fastapi.public_ip
    description = "Public IP for FastAPI"
}
output "wazuh_private_ip" {
    value = aws_instance.wazuh.private_ip
    description = "Private IP for Wazuh"
}
output "vpc_id" {
    value = aws_vpc.main.id
}