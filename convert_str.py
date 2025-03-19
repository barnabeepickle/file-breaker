"""A mini-lib that converts an entry (usally from a list) into a valid string.
Returns:
    str: The output valid string.
"""
# mini-lib
# version 1.0
def convert_str(item): # intended to be used internally though I might make it a mini-lib
    """Converts an entry (usally from a list) into a valid string.
    Args:
        item (list, str): The input variable to convert to a valid string.
    Returns:
        str: The output valid string.
    """
    item=str(item)
    item=item.strip(',[]') # strip normal stuff
    item=item.strip('"') # strip double quotes
    item=item.strip("'") # strip single quotes
    return item