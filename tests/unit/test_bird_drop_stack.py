import aws_cdk as core
import aws_cdk.assertions as assertions

from bird_drop.bird_drop_stack import BirdDropStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bird_drop/bird_drop_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BirdDropStack(app, "bird-drop")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
