import json
import boto3


"""
To be set up as a separate lambda function (outside of 'rdk' cli), and triggered by a CloudWatch event.
"""
def lambda_handler(event, context):
    if event["detail"]["newEvaluationResult"]["complianceType"] == "NON_COMPLIANT":
        user_id = event["detail"]["resourceId"]

        #Get username from user ID
        iam = boto3.client("iam")
        users_result = iam.list_users()
        user_name = ""
        for user in users_result["Users"]:
            if user["UserId"] == user_id:
                user_name = user["UserName"]
                break

        print("Adding user {} to quarantine.".format(user_name))
        iam.add_user_to_group(GroupName="QuarantinedUsers", UserName=user_name)