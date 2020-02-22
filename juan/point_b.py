import re

version_pattern = r'^[0-9]+(\.[0-9]+)*[ab]?$'
alpha_beta_subversion_pattern = r'^[0-9]+[ab]{1}$'
assertion_message = '{} must have a pattern like: {}'
literal_decoder = {'a': -0.2, 'b': -0.1}


def decode_value(code: str) -> float:
    if re.match(alpha_beta_subversion_pattern, code):
        value = float(code[:-1])
        value = value + literal_decoder[code[-1]]
        return value
    else:
        return float(code)


def check_residual(version1: list, version2: list) -> tuple:
    total_diff = sum(list(map(lambda x: decode_value(x), version1[len(version2):])))
    if total_diff == 0:
        return tuple((0, 0))
    elif total_diff > 0:
        return tuple((1, -1))
    elif total_diff <= 0:
        return tuple((-1, 1))


def check_version(version1: str, version2: str) -> tuple:
    # returns an integer tuple: (0, 0) if versions are equal
    #                          (1, -1) if version1 is greater than version2
    #                          (-1, 1) if version2 is greater than version1
    #
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
    # After check every matched version number pair, it checks if there is a residual version code greater than zero
    if len(version1) > len(version2):
        return check_residual(version1, version2)
    elif len(version2) > len(version1):
        output = check_residual(version2, version1)
        return tuple((output[1], output[0]))
    return tuple((0, 0))
