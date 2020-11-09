import random
import re
import regex
import string
from contextlib import suppress

import yaml
from google.cloud import storage


def random_element(num_chars):
    """
    generates a random string of numbers and lower case letters
    :type num_chars: int
    """
    characters: str = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for i in range(num_chars))


def labellize(labelText):
    # make text valid for a Google Cloud label
    # label rules here - https://cloud.google.com/compute/docs/labeling-resources
    # in summary - lower case characters, numbers, dash or hyphen. <= 63 characters
    labelText = labelText.lower()
    # labelText = re.sub('[^0-9a-z-_]+', '-', labelText)
    labelText = regex.sub('[^\p{Ll}\p{Lo}\p{N}-_]+', '-', labelText)
    if len(labelText) > 63:
        labelText = labelText[0:63]
    return labelText


# This method should 'sanitize' a given name for GCP usage
# Does the following:
# Makes alphabetic characters lower case
# Replaces anything other alphanumeric/hyphen with hyphen
# first and last characters alphabetic
# name < 63 chars
def sanitize(name):
    # make lower case and replace characters other than alphanumeric and hyphen
    valid = False
    while valid == False:
        name = name.lower()
        name = name[0:63]
        name = re.sub('[^0-9a-z-]+', '-', name)
        if not re.search('[a-zA-Z]', name):
            name = 'a{}a'.format(name)
        if name[0].isnumeric() or name[0] == '-':
            name = name[1:]
        if name[-1].isnumeric() or name[-1] == '-':
            name = name[:-1]
        valid = True

    return name


# Ensure folder name is valid
# The name must be between 3 and 30 characters.
# The name may contain letters, digits, spaces, hyphens and underscores.
# The folder's display name must start and end with a letter or digit.
# The name must be between 3 and 30 characters.
# The name must be distinct from all other folders that share its parent.
def folderize(name):
    valid = False
    while valid == False:
        name = name[0:30]
        name = re.sub('[^0-9a-zA-Z-_]+', '-', name)
        if name[0] == '-' or name[0] == '_' or name[0] == ' ':
            name = name[1:]
        if name[-1] == '-' or name[-1] == '_' or name[-1] == ' ':
            name = name[:-1]
        valid = True

    return name


def remove_keys_from_dict(payload, keys_to_remove):
    for key in keys_to_remove:
        with suppress(KeyError):
            del payload[key]

    return payload
