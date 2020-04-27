import re


def labellize(labelText):
    # make text valid for a Google Cloud label
    # label rules here - https://cloud.google.com/compute/docs/labeling-resources
    # in summary - lower case characters, numbers, dash or hyphen. <= 63 characters
    labelText = labelText.lower()
    return re.sub('[^0-9a-z-_]+', '-', labelText)

