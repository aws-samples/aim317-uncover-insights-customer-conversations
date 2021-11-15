# AIM317 re:Invent 2021 Workshop
## Uncover insights from customer conversations — no ML expertise required

### Abstract 
Understanding what your customers are saying is critical to your business. But navigating the technology needed to make sense of these conversations can be daunting. In this hands-on workshop, you will discover how to uncover valuable insights from your data using custom models that are tailored to your business needs—no ML expertise required. With a set of customer calls, learn how to boost transcription accuracy with Amazon Transcribe custom language models, extract insights with Amazon Comprehend custom entities, localize content with Amazon Translate active custom translation, and create powerful visualizations with Amazon QuickSight.

This code sample is part of the re:Invent 2021 workshop and is designed to guide AWS re:Invent attendees through setting up a complete end-to-end solution for analyzing voice recordings of customer and support representative interactions  These analyses can be used to detect sentiment, keywords, transcriptions, or translations. The following are the high-level steps to deploy this solution:

## Phase 1 - Build using SageMaker Jupyter notebooks

We will first deep dive into the solution to understand what the building blocks are and how you can tie these together. The various notebooks you will run are as shown in the following image.

[SageMaker notebook architecture](https://github.com/aws-samples/aim317-uncover-insights-customer-conversations/blob/main/static/aim317-sm-arch-full.jpg)

For a full list of instructions to running these notebooks, please refer to the [AIM317 Workshop Instructions](https://catalog.us-east-1.prod.workshops.aws/v2/workshops/1e224d5a-4273-444a-acec-28d44a5bfb28/en-US)


## Phase 2 - Full Deployment - Operationalized Solution

The solution that will be deployed is shown in the following image.

[Solution Architecture](https://github.com/aws-samples/aim317-uncover-insights-customer-conversations/blob/main/static/AIM317%20Diagram%20-%20A1.png)

Use the following AWS CloudFormation template to launch the operational version of the solution.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateUrl=https://ai-ml-services-lab.s3.amazonaws.com/public/labs/aim317/cloudformation/aim317Template.yml&param_SubnetID=subnet-00001)

Follow are the list of the parameters. 

| Parameters         | Description                                    |
| ------------------ | ---------------------------------------------- |
| SubnetID           | Subnet where the Lambdas will be deployed      |

You can copy the the required `SubnetID` from your default VPC in the VPC service in the console.

![Subnets](static/subnets.png)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
