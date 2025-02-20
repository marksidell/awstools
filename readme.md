- In the AWS Elastic Container Registry create a repository in the (e.g. "www")

- In the AWS Elastic Container Service, create a Task definition.

  - Family: e.g. "www"
  - Launch type: Fargate
  - Task role: If the container software needs to call the AWS API, first create
      an IAM role with the necessary permissions and enter the role ARN here.
      To allow debugging include "AmazonSSMManagedEC2InstanceDefaultPolicy"
  - Task execution role: Create new role
  - Container: The one you created previously.

- Create an ECS Cluster (e.g. "www"). If the create fails, delete the CloudFormation
  stack for the failed cluster and try again.

  