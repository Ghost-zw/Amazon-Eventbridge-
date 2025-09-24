import json
import boto3
import logging

# Initialize SNS client
sns = boto3.client('sns')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Extract details from the event
    instance_id = event['detail']['instance-id']
    state = event['detail']['state']
    
    try:
        # Handle different states
        if state == "running":
            # Logic to handle running state if needed
            message = f"EC2 Instance {instance_id} has started."
        elif state == "stopped":
            # Logic to handle stopped state if needed
            message = f"EC2 Instance {instance_id} has stopped."
        elif state == "terminated":
            # Logic to handle terminated state if needed
            message = f"EC2 Instance {instance_id} has been terminated."
        else:
            raise ValueError(f"Unexpected state: {state}")

        # Publish successful state change notification
        subject = f"EC2 Instance State Change Notification"
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:800762100325:EC2_Notification',
            Message=message,
            Subject=subject
        )
        
        logger.info(f"Notification sent for instance {instance_id} with state {state}.")

    except Exception as e:
        # Log the error
        logger.error(f"Error processing instance {instance_id}: {str(e)}")
        
        # Create an error message
        error_message = f"Failed to process EC2 Instance {instance_id}. Error: {str(e)}"
        
        # Publish error notification to SNS
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:800762100325:EC2_NotificationError',
            Message=error_message,
            Subject='EC2 Instance State Change Error'
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Process completed.')
    }
