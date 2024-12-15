import os


def get_cwd_filename(filename: str):
    return os.path.join(os.getcwd(), filename)


def get_env_dict(env_filename: str) -> dict:
    """
    Reads .env file with the following format:
    KEY1=value1
    KEY2=value2
    KEY3=value3

    Ignores line that start with '#' symbol

    Returns dictionary with keys as keys and values as values

    duh..
    """

    env_dict = dict()
    full_env_filename = get_cwd_filename(env_filename)

    with open(full_env_filename, 'r') as f:
        for line in f:
            if not line[0].isalpha():
                continue
            key, value = line.strip().split('=', maxsplit=1)
            env_dict[key] = value

    return env_dict
