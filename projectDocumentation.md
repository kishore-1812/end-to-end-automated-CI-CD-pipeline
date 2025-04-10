									<u>PROJECT DOCUMENTATION</u>





To start with the project, we should setup a cloud infrastructure (network) using AWS so that we will have all the resources like SIEM, backend services and also, public facing resources like the frontend server, API gateways, load balancer. Before we setup these resources inside our network, we create a VPC network, so that we will have two subnets, one for public facing resources and the other for the private resources; which we don't want the outside people to have direct access because main security measures are implemented here, so we protect this.

Steps to follow to create a VPC:

1. We should create a **VPC** with **CIDR : 10.0.0.0/16** from the AWS CLI using the following command

   ```
   aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=SecurityVPC}]'
   ```

   Note: 

2. We then go on to create two subnets (**Public Subnet & Private Subnet**) and before to that, we get the **ID** of the VPC instance that we created already

   ```
   # Get the VPC ID:
   VPC_ID=$(aws ec2 describe-vpcs --filters "Name=cidr-block,Values=10.0.0.0/16" --query "Vpcs[0].VpcId" --output text) 
   
   #Create Public Subnet:
    aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PublicSubnet}]' 
   
   #Create Private Subnet: 
   aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PrivateSubnet}]'
   ```

3. The next step will be setting up an Internet Gateway for the public subnet to be able to communicate with the internet and vice versa by the public internet users

   ```
   # Create Internet Gateway: 
   IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text) 
   
   #Attach it to the VPC:
    aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID 
   ```

4. We need to be able to define the routing information (create routing table and configure route) for both the subnets and we do that using the following command

​	

```
# Create Route Table for Public Subnet: 
1. PUB_RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text) 

2. aws ec2 associate-route-table --route-table-id $PUB_RT_ID --subnet-id $(aws ec2 describe-subnets --filters "Name=tag:Name,Values=PublicSubnet" --query "Subnets[0].SubnetId" --output text) 

#Create a Route to Allow Internet Access in Public Subnet: 
aws ec2 create-route --route-table-id $PUB_RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID

# Create Route Table for Private Subnet:
1. PRIV_RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)

2. aws ec2 associate-route-table --route-table-id $PRIV_RT_ID --subnet-id $(aws ec2 describe-subnets --filters "Name=tag:Name,Values=PrivateSubnet" --query "Subnets[0].SubnetId" --output text)
```

​	Note: We are creating route table so that we can make the internet connection possible with the subnets and we make sure that we only create a route for the public subnet to the internet gateway and not for the private subnet since it has to stay secured and not be accessed by anybody.

5. We then implement security groups to define which resources has been granted access to what entity using the following command

   ```
   # Create Security Group for Public Subnet: 
   
   PUB_SG_ID=$(aws ec2 create-security-group --group-name PublicSG --description "Public Security Group" --vpc-id $VPC_ID --query 'GroupId' --output text) 
   
   #Allow HTTP/HTTPS traffic to Public Subnet (Frontend/API): 
   
   1. aws ec2 authorize-security-group-ingress --group-id $PUB_SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0 
   
   2. aws ec2 authorize-security-group-ingress --group-id $PUB_SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0 
   
   3. aws ec2 authorize-security-group-ingress --group-id $PUB_SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 # SSH for maintenance
   
   # Create Security Group for Private Subnet
   PRIV_SG_ID=$(aws ec2 create-security-group --group-name PrivateSG --description "Private Security Group" --vpc-id $VPC_ID --query 'GroupId' --output text)
   
   # Allow only traffic from Public Security Group:
   aws ec2 authorize-security-group-ingress --group-id $PRIV_SG_ID --protocol tcp --port 9200 --source-group $PUB_SG_ID 
   
   # Allow ELK/SIEM from Public:
    aws ec2 authorize-security-group-ingress --group-id $PRIV_SG_ID --protocol tcp --port 22 --source-group $PUB_SG_ID # Allow SSH only from Public Subnet
   ```

   6. Finally, we deploy the EC2 instances inside VPC 

      ```
      # Launch SIEM Server in Private Subnet:
      aws ec2 run-instances --image-id ami-0abcdef1234567890 --count 1 --instance-type t2.medium --key-name MyKeyPair --security-group-ids $PRIV_SG_ID --subnet-id $(aws ec2 describe-subnets --filters "Name=tag:Name,Values=PrivateSubnet" --query "Subnets[0].SubnetId" --output text) --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=SIEM-Server}]' 
      
      # Launch Web Application in Public Subnet:
      aws ec2 run-instances --image-id ami-0abcdef1234567890 --count 1 --instance-type t2.medium --key-name MyKeyPair --security-group-ids $PUB_SG_ID --subnet-id $(aws ec2 describe-subnets --filters "Name=tag:Name,Values=PublicSubnet" --query "Subnets[0].SubnetId" --output text) --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebApp}]'
      
      
      ```








SIEM choices:

![image-20250213120554806](/home/kishore/.config/Typora/typora-user-images/image-20250213120554806.png)