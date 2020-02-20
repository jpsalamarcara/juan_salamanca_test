

def check_overlap(vector_a: tuple, vector_b: tuple) -> bool:
    assert len(vector_a) == len(vector_b), 'vectors must have the same rank'
    assert len(vector_a) == 2, 'only 2 rank vectors are allowed'
    return not (max(vector_a) < min(vector_b) or max(vector_b) < min(vector_a))
