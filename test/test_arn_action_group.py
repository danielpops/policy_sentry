import unittest
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.policy import ArnActionGroup

home = str(Path.home())
config_directory = '/.policy_sentry/'
database_file_name = 'aws.sqlite3'
database_path = home + config_directory + database_file_name
db_session = connect_db(database_path)

# To get the print statements in output, run this:
# nosetests -v tests/test_arn_action_group.py --nocapture


class ArnActionGroupTestCase(unittest.TestCase):
    def test_add_s3_permissions_management_arn(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = [
            {
                'arn': 'arn:aws:s3:::example-org-s3-access-logs',
                'service': 's3',
                'access_level': 'Permissions management',
                'arn_format': 'arn:aws:s3:::${BucketName}',
                'actions': []
            }
        ]
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        print(arn_action_group.get_arns())
        self.assertEqual(arn_action_group.get_arns(), desired_output)

    def test_update_actions_for_raw_arn_format(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = [
            {
                'arn': 'arn:aws:s3:::example-org-s3-access-logs',
                'service': 's3',
                'access_level': 'Permissions management',
                'arn_format': 'arn:aws:s3:::${BucketName}',
                'actions': [
                    "s3:deletebucketpolicy",
                    "s3:putbucketacl",
                    "s3:putbucketpolicy",
                    "s3:putbucketpublicaccessblock"
                ]
            }
        ]
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        arn_action_group.update_actions_for_raw_arn_format(db_session)
        print(arn_action_group.get_arns())
        self.assertEqual(arn_action_group.get_arns(), desired_output)


    def test_get_policy_elements(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = {
            'S3PermissionsmanagementBucket':
                {
                    'name': 'S3PermissionsmanagementBucket',
                    'actions': [
                        's3:deletebucketpolicy',
                        's3:putbucketacl',
                        's3:putbucketpolicy',
                        's3:putbucketpublicaccessblock'
                    ],
                    'arns': [
                        'arn:aws:s3:::example-org-s3-access-logs'
                    ]
                }
        }
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        arn_action_group.update_actions_for_raw_arn_format(db_session)
        arn_dict = arn_action_group.get_policy_elements(db_session)
        print(arn_dict)
        self.assertEqual(arn_dict, desired_output)
