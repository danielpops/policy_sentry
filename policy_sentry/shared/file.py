import yaml
import os.path
import json
from os import listdir
from os.path import isfile, join


def read_this_file(filename):
    lines = []

    with open(filename, 'r') as fileobj:
        for row in fileobj:
            # FIXME check for bad or unknown characters, we know this should be in a standard format,
            lines.append(row.rstrip('\n'))
            # we should enforce it
    return lines


# FIXME as with the json files we should have a generic validation function, maybe it can read the file extension
# and then figure out what to do with it. I like what is going on here but where do you check to see if the file
# exists or validate the path?
def read_yaml_file(filename):
    """
    Description: Reads a YAML file, safe loads, and returns the dictionary
    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return cfg


def check_valid_file_path(file):
    """
    Checks if the file path is valid.
    :param file: The file to check.
    :return: True if it exists, False if it does not
    """

    if os.path.exists(file):
        # print("Evaluating: " + file)
        return True
    else:
        print("File does not exist or is formatted incorrectly: " + file + "\nPlease provide a valid path.")
        return False


def write_json_file(filename, json_contents):
    """
    Description: Writes a YAML file
    :param json_contents: a dictionary used to build the JSON. This is the IAM Policy built by write_policy functions.
    :param filename: name of the yaml file, which should include the path
    """
    with open(filename, 'w') as file:
        # try:
        json.dump(json_contents, file, indent=4)
        # except yaml.YAMLError as exc:
        #     print(exc)
    # return filename


def get_actions_from_json_policy_file(json_file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    with open(json_file) as json_file:
        # validation function/parser as there is a lot of json floating around in this tool. [MJ]
        data = json.load(json_file)
        actions_list = []
        # Multiple statements are in the 'Statement' list
        for i in range(len(data['Statement'])):
            try:
                if isinstance(data['Statement'], dict):
                    try:

                        if isinstance(data['Statement']['Action'], str):
                            actions_list.append(data['Statement']['Action'])
                        elif isinstance(data['Statement']['Action'], list):
                            actions_list.extend(data['Statement']['Action'])
                        else:
                            print("Unknown error: The 'Action' is neither a list nor a string")
                            continue
                    except KeyError as e:
                        print(e)
                        exit()
                elif isinstance(data['Statement'], list):
                    try:
                        if isinstance(data['Statement'][i]['Action'], str):
                            actions_list.append(data['Statement'][i]['Action'])
                        elif isinstance(data['Statement'][i]['Action'], list):
                            actions_list.extend(data['Statement'][i]['Action'])
                        else:
                            print("Unknown error: The 'Action' is neither a list nor a string")
                            exit()
                    except KeyError as e:
                        print(e)
                        exit()
                else:
                    print("Unknown error: The 'Action' is neither a list nor a string")
                    exit()
            except TypeError as e:
                print(e)
                exit()
    try:
        actions_list = [x.lower() for x in actions_list]
    except AttributeError:
        print(actions_list)
        print("AttributeError: 'list' object has no attribute 'lower'")
    actions_list.sort()
    return actions_list


def list_files_in_directory(directory):
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return only_files


def create_directory_if_it_doesnt_exist(directory):
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)
