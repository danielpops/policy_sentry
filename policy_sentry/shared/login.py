import os
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def login_sts_test(sts_session):
    try:
        sts_session.get_caller_identity()
    except ClientError as e:
        if "InvalidClientTokenId" in str(e):
            print(
                "ERROR: sts.get_caller_identity failed with InvalidClientTokenId. Likely cause is no AWS credentials are set.",
                flush=True,
            )
            exit(-1)
        else:
            print(
                "ERROR: Unknown exception when trying to call sts.get_caller_identity: {}".format(
                    e
                ),
                flush=True,
            )
            exit(-1)

def login_iam_test(iam_session):
    try:
        iam_session.get_user(UserName="test")
    except ClientError as e:
        if "InvalidClientTokenId" in str(e):
            print(
                "ERROR: AWS doesn't allow you to make IAM calls from a session without MFA, and the collect command gathers IAM data.  Please use MFA or don't use a session. With aws-vault, specify `--no-session` on your `exec`.",
                flush=True,
            )
            exit(-1)
        if "NoSuchEntity" in str(e):
            # Ignore, we're just testing that our creds work
            pass
        else:
            print("ERROR: Ensure your creds are valid.", flush=True)
            print(e, flush=True)
            exit(-1)
    except NoCredentialsError:
        print("ERROR: No AWS credentials configured.", flush=True)
        exit(-1)


def login(profile_name, service='iam'):
    default_region = os.environ.get("AWS_REGION", "us-east-1")
    session_data = {"region_name": default_region}
    if profile_name:
        session_data["profile_name"] = profile_name

    session = boto3.Session(**session_data)

    sts_session = session.client("sts")
    login_sts_test(sts_session)

    # Ensure we can make iam calls
    iam_session = session.client("iam")
    login_iam_test(iam_session)

    # Return the service requested by the function - either sts or iam
    if service:
        this_session = session.client(service)
    # By default return IAM
    else:
        this_session = session.client("iam")
    return this_session
    # return session
# client = boto3.client("sts", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
# account_id = client.get_caller_identity()["Account"]
