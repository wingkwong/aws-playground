# HA Implementation

## Goals

- Create an image of an existing Amazon EC2 instance and use it to launch new instances.
- Expand an Amazon VPC to additional Availability Zones.
- Create VPC Subnets and Route Tables.
- Create an AWS NAT Gateway.
- Create a Load Balancer.
- Create an Auto Scaling group.

![image](https://user-images.githubusercontent.com/35857179/88475455-839bec80-cf62-11ea-9dfb-98bbf0846414.png)

## Prerequisites

- An Amazon VPC
- A public subnet and a private subnet in one Availability Zone
- An Internet Gateway associated with the public subnet
- A NAT Gateway in the public subnet
- An Amazon EC2 instance in the public subnet

## Download, Install, and Launch Your Web Server's PHP Application

In this task, you will be performing typical System Administrator activities to install and configure the web application. In a following task, you will create an image of this machine to automatically deploy the application on more instances to make it Highly Available.

The commands in this task will download, install, and launch your PHP web application. The instructions will step you through each command one at a time so you can understand exactly what you are doing to accomplish this task.

To update the base software installed your instance, execute the following command:

```
sudo yum -y update
```

This will discover what updates are available for your Amazon Linux instance, download the updates, and install them.

Tip for PuTTy users: Simply right-click to Paste.

To install a package that creates a web server, execute the following command:

```
sudo yum -y install httpd php
```

This command installs an Apache web server (httpd) and the PHP language interpreter.

Execute the following command:

```
sudo chkconfig httpd on
```

This configures the Apache web server to automatically start when the instance starts.

Execute the following command:

```
wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-200-ACACAD/studentdownload/phpapp.zip
```

This downloads a zip file containing the PHP web application.

Execute the following command:

```
sudo unzip phpapp.zip -d /var/www/html/
```

This unzips the PHP application into the default Apache web server directory.

Execute the following command:

```
sudo service httpd start
```

This starts the Apache web server.

 You can ignore any warnings about "Could not reliably determine...".

Your web application is now configured! You can now access application to confirm that it is working.

Open a new web browser tab, paste the Public IP address for your instance in the address bar and hit Enter. (That is the same IP address you copied into a Text Editor and used with ssh/PuTTy.)

The web application should appear and will display information about your location (actually, the location of your Amazon EC2 instance). This information is obtained from freegeoip.app.

If the application does not appear, ask your instructor for assistance in diagnosing the configuration.

Close the web application browser tab that you opened in the previous step.

Return to your SSH session, execute the following command:

```
exit
```

This ends your SSH session.

## Create a second Public Subnet 

On the Services menu, click VPC.

In the left navigation pane, click Subnets.

In the row for Public Subnet 1, take note of the value for Availability Zone. (You might need to scroll sideways to see it.)

Note: The name of an Availability Zone consists of the Region name (eg us-west-2) plus a zone identifier (eg a). Together, this Availability Zone has a name of us-west-2a.

Click Create Subnet.

In the Create Subnet dialog box, configure the following:

Name tag: Public Subnet 2

VPC: Lab VPC

Availability Zone: Choose a different Availability Zone from the existing Subnet (for example, if it was a, then choose b).

IPv4 CIDR block: 10.200.1.0/24

This will create a second Subnet in a different Availability Zone, but still within Lab VPC. It will have an IP range between 10.200.1.0 and 10.200.1.255.

Click Create.

Copy the Subnet ID to a text editor for later use, then click Close.

It should look similar to: subnet-abcd1234

With Public Subnet 2 selected, click the Route Table tab in the lower half of the window. (Do not click the Route Tables link in the left navigation pane.)

Here you can see that your new Subnet has been provided with a default Route Table, but this Route Table does not have a connection to your Internet gateway. You will change it to use the Public Route Table.

Click Edit route table association.

Try each Route Table ID in the list, selecting the one that shows a Target containing igw.

Click Save then click Close.

Public Subnet 2 is now a Public Subnet that can communicate directly with the Internet.

## Create a Second Private Subnet

Your application will be deployed in private subnets for improved security. This prevents direct access from the Internet to the instances. To configure high availability, you will need a second private Subnet.

Click Create subnet.

In the Create Subnet dialog box, configure the following:

Name tag: Private Subnet 2
VPC: Lab VPC
Availability Zone: Choose the same Availability Zone you just selected for Public Subnet 2.
IPv4 CIDR block: 10.200.4.0/23
Click Create and then click Close.

The Subnet will have an IP range between 10.200.4.0 and 10.200.5.255.

## Create a Second NAT Gateway

A NAT Gateway (Network Address Translation) is provisioned into a public Subnet and provides outbound Internet connectivity for resources in a private Subnet. Your web application requires connectivity to the Internet to retrieve geographic information, so you will need to route Internet-bound traffic through a NAT Gateway.

To remain Highly Available, your web application must be configured such that any problems in the first Availability Zone should not impact resources in the second Availability Zone, and vice versa. Therefore, you will create a second NAT Gateway in the second Availability Zone.

In the left navigation pane, click NAT Gateways.

Click Create NAT Gateway.

For Subnet, enter the Subnet ID for Public Subnet 2 that you copied to a text editor earlier in the lab.

Click Allocate Elastic IP address.

An Elastic IP Address (EIP) is a static IP address that will be associated with this NAT Gateway. The Elastic IP address will remain unchanged over the life of the NAT Gateway.

Click Create a NAT Gateway, then click Close.

You will now see two NAT Gateways.

Tip: If you only see one, click the refresh icon in the top-right until the second one appears.

The NAT Gateway that you just created will initially have a status of pending. Once it becomes available, you will see that it will have a private IP Address starting with 10.200.1.

Copy the NAT Gateway ID show in the first column, starting with nat-. Paste it into a text document for use in the next task.

You must now configure your network to use the second NAT Gateway.

## Create a Second Private Route Table

A Route Table defines how traffic flows into and out of a Subnet. You will now create a Route Table for Private Subnet 2 that sends Internet-bound traffic through the NAT Gateway that you just created.

In the navigation pane, click Route Tables.

Click Create route table.

In the Create route table dialog box, configure the following:

Name tag: Private Route Table 2

VPC: Lab VPC

Click Create, then click Close.

Highlight the Private Route Table 2 that you just created, and click the Routes tab in the lower half of the window.

The Route Table currently only sends traffic within the VPC, as shown in the route table entry with the Target of local. You will now configure the Route Table to send Internet-bound traffic (identified with the wildcard 0.0.0.0/0) through the second NAT Gateway.

Click Edit routes.

Click Add route.

For Destination, type: 0.0.0.0/0

Click in the Target drop down list, and choose the NAT Gateway with the ID you copied earlier. (Check your text editor for the nat- ID you saved earlier.)

Click Save routes, then click Close.

You can now associate this Route Table (Private Route Table 2) with the second Private Subnet 2 that you created earlier.

With Private Route Table 2 still selected, click the Subnet Associations tab at the bottom of the screen.

Click Edit subnet associations.

Select (tick) the checkbox beside Private Subnet 2.

Click Save.

Private Subnet 2 will now route Internet-bound traffic through the second NAT Gateway.

## Create an Application Load Balancer

In this task, you will create an Application Load Balancer that distributes requests across multiple Amazon EC2 instances. This is a critical component of a Highly Available architecture because the Load Balancer performs health checks on instances and only sends requests to healthy instances.

![image](https://user-images.githubusercontent.com/35857179/88475506-0e7ce700-cf63-11ea-8e74-33bb67290e2a.png)

You do not have any instances yet -- they will be created by the Auto Scaling group in the next task.

Load Balancer    
On the Services menu, click EC2.

In the left navigation pane, click Load Balancers (you might need to scroll down to find it).

Click Create Load Balancer.

Several types of Load Balancers are displayed. Read the descriptions of each type to understand their capabilities.

Under Application Load Balancer, click Create.

For Name, type: LB1

Scroll down to the Availability Zones section.

For VPC, select Lab VPC.

You will now specify which subnets the Load Balancer should use. It will be an Internet-facing load balancer, so you will select both Public Subnets.

Click the first displayed Availability Zone, then click the Public Subnet displayed in the associated drop-down list.

Click the second displayed Availability Zone, then click the Public Subnet displayed in the associated drop-down list.

You should now have two subnets selected: Public Subnet 1 and Public Subnet 2. (If not, go back and try the configuration again.)

Click Next: Configure Security Settings.

A warning is displayed, which recommends using HTTPS for improved security. This is good advice, but is not necessary for this lab.

Click Next: Configure Security Groups.

Select the Security Group with a Description of Security group for the web servers (and deselect any other security group).

Note: This Security Group permits only HTTP incoming traffic, so it can be used on both the Load Balancer and the web servers.

Click Next: Configure Routing.

Target Groups define where to send traffic that comes into the Load Balancer. The Application Load Balancer can send traffic to multiple Target Groups based upon the URL of the incoming request. Your web application will use only one Target Group.

For Name, type: Group1

Click Advanced health check settings to expand it.

The Application Load Balancer automatically performs Health Checks on all instances to ensure that they are healthy and are responding to requests. The default settings are recommended, but you will make them slightly faster for use in this lab.

For Healthy threshold, type: 2

For Interval, type: 10

This means that the Health Check will be performed every 10 seconds and if the instance responds correctly twice in a row, it will be considered healthy.

Click Next: Register Targets.

Targets are instances that will respond to requests from the Load Balancer. You do not have any web application instances yet, so you can skip this step.

Click Next: Review.

Review the settings and click Create.

Click Close.

You can now create an Auto Scaling group to launch your Amazon EC2 instances.

## Create an Auto Scaling Group

Auto Scaling is a service designed to launch or terminate Amazon EC2 instances automatically based on user-defined policies, schedules, and health checks. It also automatically distributes instances across multiple Availability Zones to make applications Highly Available.

![image](https://user-images.githubusercontent.com/35857179/88475510-19d01280-cf63-11ea-89e8-a963fa7d877b.png)

In this task, you will create an Auto Scaling group that deploys Amazon EC2 instances across your Private Subnets. This is best practice security for deploying applications because instances in a private subnet cannot be accessed from the Internet. Instead, users will send requests to the Load Balancer, which will forward the requests to Amazon EC2 instances in the private subnets.

Auto Scaling
In the left navigation pane, click Auto Scaling Groups (you might need to scroll down to find it).

Click Create Auto Scaling group.

Click Get started.

A Launch Configuration defines what type of instances should be launched by Auto Scaling. The interface looks similar to launching an Amazon EC2 instance, but rather than launching an instance it stores the configuration for later use.

You will configure the Launch Configuration to use the AMI that you created earlier. It contains a copy of the software that you installed on the Configuration Server.

In the left navigation pane, click My AMIs.

In the row for Web application, click Select.

Accept the default (t2.micro) instance type and click Next: Configure details .

For Name, type: Web-Configuration

Click Next: Add Storage.

You do not require additional storage on this instance, so keep the default settings.

Click Next: Configure Security Group.

Click Select an existing security group.

Select the Security Group with a Description of Security group for the web servers.

Click Review.

 You may receive a warning that you will not be able to connect to the instance via SSH. This is acceptable because the server configuration is already defined on the AMI and there is no need to login to the instance.

Click Continue to dismiss the warning.

Review the settings, then click Create launch configuration.

When prompted, accept the vockey keypair, select the acknowledgement check box, then click Create launch configuration.

You will now be prompted to create the Auto Scaling group. This includes defining the number of instances and where they should be launched.

In the Create Auto Scaling Group page, configure the following settings:
Group Name: Web application

Group Size: Start with 2 instances

Network: Lab VPC

Subnet: Click in the box and select both Private Subnet 1 and Private Subnet 2

Auto Scaling will automatically distribute the instances amongst the selected Subnets, with each Subnet in a different Availability Zone. This is excellent for maintaining High Availability because the application will survive the failure of an Availability Zone.

Click the Advanced Details heading to expand it.

Select (tick) the Load Balancing checkbox.

Click in Target Groups, then select Group1.

Click Next: Configure scaling policies.

Ensure Keep this group at its initial size is selected.

This configuration tells Auto Scaling to always maintain two instances in the Auto Scaling group. This is ideal for a Highly Available application because the application will continue to operate even if one instance fails. In such an event, Auto Scaling will automatically launch a replacement instance.

Click Next: Configure Notifications.
You will not be configuring any notifications.

Click Next: Configure Tags.
Tags placed on the Auto Scaling group can also automatically propagate to the instances launched by Auto Scaling.

For Key, type: Name

For Value, type: Web application

Click Review.

Review the settings, then click Create Auto Scaling group.

Click Close.

Your Auto Scaling group will initially show zero instances. This should soon update to two instances. (Click the refresh icon in the top-right to update the display.)

Your application will soon be running across two Availability Zones and Auto Scaling will maintain that configuration even if an instance or Availability Zone fails.

## Test the Application

In this task, you will confirm that your web application is running and you will test that it is highly available.

![image](https://user-images.githubusercontent.com/35857179/88475516-25bbd480-cf63-11ea-9d75-9d05d2739fe6.png)

In the left navigation pane, select Target Groups.

Choose Group1 and click on the Targets tab in the lower half of the window.

You should see two Registered instances. The Status column shows the results of the Load Balancer Health Check that is performed against the instances.

Occasionally click the refresh icon in the top-right until the Status for both instances appears as healthy.
 If the status does not eventually change to healthy, ask your instructor for assistance in diagnosing the configuration. Hovering over the  icon in the Status column will provide more information about the status.

You will be testing the application by connecting to the Load Balancer, which will then send your request to one of the Amazon EC2 instances. You will need to retrieve the DNS Name of the Load Balancer.

In the left navigation pane, click Load Balancers.

In the Description tab in the lower half of the window, copy the DNS Name to your clipboard, but do not copy "(A Record)". It should be similar to: LB1-xxxx.elb.amazonaws.com

Open a new web browser tab, paste the DNS Name from your clipboard and hit Enter.

The Load Balancer forwarded your request to one of the Amazon EC2 instances. The Instance ID and Availability Zone are shown at the bottom of the web application.

Reload the page in your web browser. You should notice that the Instance ID and Availability Zone sometimes changes between the two instances.

You sent the request to the Load Balancer, which resides in the public subnets that are connected to the Internet.

The Load Balancer chose one of the Amazon EC2 instances that reside in the private subnets and forwarded the request to it.

The Amazon EC2 instance requested geographic information from freegeoip.app. This request went out to the Internet through the NAT Gateway in the same Availability Zone as the instance.

The Amazon EC2 instance then returned the web page to the Load Balancer, which returned it to your web browser.

## Test High Availability

Your application has been configured to be Highly Available. This can be proven by stopping one of the Amazon EC2 instances.

Return to the EC2 Management Console tab in your web browser (but do not close the web application tab - you will return to it soon).

In the left navigation pane, click Instances.

First, you do not require the Configuration Server any longer, so it can be terminated.

Select the Configuration Server.

Click Actions > Instance State > Terminate, then click Yes, Terminate.

Next, stop one of the Web application instances to simulate a failure.

Select one of the instances named Web application (it does not matter which one you select).

Click Actions > Instance State > Stop, then click Yes, Stop.

In a short time, the Load Balancer will notice that the instance is not responding and will automatically route all requests to the remaining instance.

Return to the Web application tab in your web browser and reload the page several times.
You should notice that the Availability Zone shown at the bottom of the page stays the same. Even though an instance has failed, your application remains available.

After a few minutes, Auto Scaling will also notice the instance failure. It has been configured to keep two instances running, so Auto Scaling will automatically launch a replacement instance.

Return to the EC2 Management Console tab in your web browser. Click the refresh icon in the top-right occasionally until a new Amazon EC2 instance appears.
After a few minutes, the Health Check for the new instance should become healthy and the Load Balancer will continue sending traffic between two Availability Zones. You can reload your Web application tab to see this happening.