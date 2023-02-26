#!/bin/zsh

# ------------------------------------------------
# Command help information
# ------------------------------------------------
if [ "$1" == "help" ]; then
  cat <<END
A ssh wrapper for connecting quickly to EC2 instances in an Auto Scaling group.

Usage: ec2-asg-ssh {ssh-key-location} {ssh-user}
eg: ec2-asg-ssh foobar ~/app/app.pem root

Note: Make sure to export the AWS profile first, read more:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

END
  exit
fi

# ------------------------------------------------
# Fetch autoscaling groups
# ------------------------------------------------
AUTO_SCALINGS=$(aws autoscaling describe-auto-scaling-groups --output text)
# Auto scaling names
AUTO_SCALING_IDS=$(awk '{print $3}' <<<"$AUTO_SCALINGS")
FILTERED_AUTO_SCALING_IDS=$(awk 'BEGIN{RS=ORS=" "}!a[$0]++' <<<$AUTO_SCALING_IDS)
# Apply filter
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/True/}")
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/False/}")
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/Healthy/}")
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/Unhealthy/}")
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/UnHealthy/}")
FILTERED_AUTO_SCALING_IDS=("${FILTERED_AUTO_SCALING_IDS[@]/True/}")

PS3='Select auto scaling group: '
select AUTO_SCALING_ID in $FILTERED_AUTO_SCALING_IDS 'Quit'; do
  if [ "$AUTO_SCALING_ID" = "Quit" ]; then
    exit
  else
    echo "Selected: $AUTO_SCALING_ID"
    break
  fi
done

# ------------------------------------------------
# Fetch running instances within autoscaling group
# ------------------------------------------------
INSTANCES=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names $AUTO_SCALING_ID --query 'AutoScalingGroups[0].Instances[]' --output text)
# Collect instance ids
INSTANCE_IDS=$(awk '{print $3}' <<<"$INSTANCES")

PS3='Select instance: '
select INSTANCE_ID in $INSTANCE_IDS 'Quit'; do
  if [ "$INSTANCE_ID" = "Quit" ]; then
    exit
  else
    echo "Selected: $INSTANCE_ID"
    break
  fi
done

# ------------------------------------------------
# Setup SSH user
# ------------------------------------------------
SSH_USER='ec2-user'
if [ -n "$3" ]; then
  SSH_USER=$3
fi

# ------------------------------------------------
# Get instance IP and SSH into instance
# ------------------------------------------------
# Fetch instance ip
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[0].Instances[0].PublicIpAddress" --output text)
PRIVATE_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[0].Instances[0].PrivateIpAddress" --output text)

if [ "$PUBLIC_IP" != "None" ]; then
  echo "SSHing into public instance: $PUBLIC_IP with user $SSH_USER"
  ssh -i $2 $SSH_USER@$PUBLIC_IP
  break
else
  echo "SSHing into private instance: $PRIVATE_IP with user $SSH_USER"
  ssh -i $2 $SSH_USER@$PRIVATE_IP
  break
fi
