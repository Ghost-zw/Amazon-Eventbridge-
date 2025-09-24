# EC2 State Change Notifications
EC2 State Change Notification with Eventbridge
This guide is going to show you how to create an Amazon EC2 State Change Notification, using Amazon EC2 instances, Amazon Eventbridge, Amazon Lambda and Amazon SNS


# Architecture
<img width="3504" height="1305" alt="EC2StateChange (1)" src="https://github.com/user-attachments/assets/f7d5d3e1-02d0-4afe-a51c-cdc5baaaa0d0" />

This diagram shows the key components of our setup, including:

EC2 instance for producing events
Eventbridge for creating rules
SNS for sending notifications

As we progress through this guide, we'll set up each of these components step by step.

## Table of Contents
1. [Overview of EC2 State Change Notification](#overview)
2. [Why we need EC2 State Change Notification Architecture](#EC2StateChange)
  - Phase 1 : [Create SNS](#CreateSNSTopic)
  - Phase 2 : [Launch EC2 Instance](#LaunchEC2Instance )
  - Phase 3 : [Create Lambda Function](#Lambda)
  - Phase 4 : [Deploy Application Logic](#DeployAppLogic)
  - Phase 5 : [Setting Up the Rules with Eventbridge](#Eventbridge-Setup)
  - Phase 6 : [Test the the whole solution and checking notifications](#Testing)
3. [Conclusion](#Conclusion)

# Overview of an EC2 State Change Notification Architecture <a name="overview"></a>

An EC2 state change notification architecture consists of several key AWS components that work together to monitor and respond to changes in the state of EC2 instances. Amazon EC2 hosts the virtual servers, while Amazon EventBridge continuously monitors these instances for state changes, such as starting, stopping, or terminating. When a state change is detected, EventBridge generates an event and sends it to Amazon SNS (Simple Notification Service). SNS dispatches notifications to subscribers, such as emails or SMS, while EventBridge can also route events to various targets, including AWS Lambda for executing custom logic. This architecture enables real-time monitoring, scalable notifications, and the flexibility to trigger specific actions based on instance states, all within a cost-effective pay-per-use model.

**Why we need EC2 State Change Notification  ?** <a name="EC2StateChange"></a>

EC2 state change notifications are essential for several reasons:

<p><b>Real-Time Awareness:</b> They provide immediate alerts about changes in the state of EC2 instances, ensuring that administrators are informed of critical events like starting, stopping, or terminating instances.</p>
<p></p><b>Cost Management:</b> By monitoring the state of instances, organizations can avoid unnecessary costs associated with running idle instances. Notifications can trigger actions to stop or terminate unused resources.</p>
<p></p><b>Improved Security and Compliance:</b> Monitoring state changes helps ensure that instances are properly managed and compliant with organizational policies. Alerts can be set up for unauthorized state changes, enhancing security.</p>
<p></p><b>Enhanced Troubleshooting:</b> Immediate notifications about state changes can aid in faster diagnosis of issues, allowing teams to respond promptly to potential problems.</p>

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Phase 1: CREATE SNS Topic
<a name="CreateSNS"></a>

In this Phase we are going to create a SNS Topic. This is SNS Topic is responsible for sending to notifications to the Account Admin.

Step-by-Step Process:

**1. Create SNS Topic**
  2.Go to the SNS Console:
  3.Open the AWS Management Console and navigate to the Amazon SNS dashboard.
  4.Create a Topic:
  5.Click on "Topics".
  6.Click "Create topic".
  7.Choose "Standard" and give it a name (e.g., EC2StateChangeNotifications).
  8.Click "Create topic".
  9.Subscribe to the Topic:
  9.After creating the topic, click on it.
  10.Click "Create subscription".
  11.Choose the protocol (e.g., Email) and enter the endpoint (e.g., your email address).
  12.Confirm the subscription via the email link.

<img width="1846" height="770" alt="SNS Topic" src="https://github.com/user-attachments/assets/d1391416-bda5-4f09-a8b2-43c62168999d" />

**2. Click create SNS button:**

<img width="1893" height="793" alt="SNS Creation" src="https://github.com/user-attachments/assets/834b126f-0675-4aed-80f3-07676140a6fc" />

**3. Create SNS Subcription**
Check confirmation link in email, and confirm subcription

<img width="1902" height="800" alt="SNS Subscription" src="https://github.com/user-attachments/assets/9b1d9a49-43c8-4bd1-a31a-762aafdb350f" />

## Phase 2: 
<a name="LaunchEC2Instance"></a>

**1. Launch an EC2 Instance**
  2.Go to the EC2 Dashboard in the AWS Management Console.
  3. Click Launch Instance.
  4. Choose an Amazon Machine Image (AMI):
  5. Select Amazon Linux 2023 (free tier eligible).
  6.Choose an Instance Type:
  7.Select t2.micro (free tier eligible).
  8.Configure the Network Settings:
  9.Select the Default VPC.
  10.Leave other options as default

<img width="1902" height="798" alt="launch ec2 instance" src="https://github.com/user-attachments/assets/c12a24e0-1e06-457f-93f5-6ec99cd0e7fd" />

**2. Attach a security group, either create a new security group or using an existing SG and proceed without key pair.**

<img width="1898" height="797" alt="create sg and key pair" src="https://github.com/user-attachments/assets/bee7d331-8a9b-4c54-a9e8-4f38668b053f" />

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Phase 3: Create Lambda Function
<a name="Lambda"></a>
In this phase l am going to create a lambda function which is responsible for processing the logic of processing events sent from eventbridge, invoking SNS topic to send notifications and error handling for failed events 

**1. Go to the Lambda Console:**
  2.Navigate to the AWS Lambda dashboard.
  3.Create a New Function:
  4.Click "Create function".
  5.Choose "Author from scratch".
  6.Enter a name for your function (e.g., EC2StateChangeNotifier).
  7.Choose Python 3.x (or another language of your choice) for the runtime.
  8.Click "Create function"

<img width="1892" height="793" alt="create lambda function" src="https://github.com/user-attachments/assets/4cd15694-7334-40b0-9b15-38cc06f4523c" />

**2. Create a policy to allow lambda to publish to AWS Lambda.**

<img width="1867" height="785" alt="create policy" src="https://github.com/user-attachments/assets/7f289058-4a2e-4409-b2c1-35a7c9923259" />

**3. Create Execution role for lambda and attach the policy we create above and attach LambdaBasicExecutionRole.**

<img width="1902" height="798" alt="execution policy role" src="https://github.com/user-attachments/assets/db38a73a-bce6-4c8c-a91d-f79290c4e04d" />


<img width="1875" height="785" alt="attach 2 policies" src="https://github.com/user-attachments/assets/00927a07-8546-4d48-824f-f89c22fd75bb" />


**4. Attach Lambda Execution role with a policy that allows lambda to publish to SNS Topic we created and create lambda function.** 

<img width="1892" height="788" alt="execution role" src="https://github.com/user-attachments/assets/0074da60-382d-44aa-ab65-36430985c2d4" />



