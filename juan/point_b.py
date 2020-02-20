import re

version_pattern = r'^[0-9]+(\.[0-9]+)*[ab]?$'
alpha_beta_subversion_pattern = r'^[0-9]+[ab]{1}$'
assertion_message = '{} must have a pattern like: {}'


def decode_value(code):
    if re.match(alpha_beta_subversion_pattern, code):
        value = int(code[:-1])
        value = value - 0.2 if code[-1] == 'a' else value - 0.1
        return value
    else:
        return int(code)


def check_residual(version1: list, version2: list) -> tuple:
    total_diff = sum(list(map(lambda x: decode_value(x), version1[len(version2):])))
    if total_diff == 0:
        return tuple((0, 0))
    elif total_diff > 0:
        return tuple((1, -1))
    elif total_diff <= 0:
        return tuple((-1, 1))


def check_version(version1: str, version2: str) -> tuple:
    assert re.match(version_pattern, version1), assertion_message.format('version1', version_pattern)
    assert re.match(version_pattern, version2), assertion_message.format('version2', version_pattern)
    version1 = version1.split('.')
    version2 = version2.split('.')
    for (v1, v2) in zip(version1, version2):
        value1 = decode_value(v1)
        value2 = decode_value(v2)
        if value1 > value2:
            return tuple((1, -1))
        elif value2 > value1:
            return tuple((-1, 1))
    if len(version1) > len(version2):
        return check_residual(version1, version2)
    elif len(version2) > len(version1):
        output = check_residual(version2, version1)
        return tuple((output[1], output[0]))
    return tuple((0, 0))
