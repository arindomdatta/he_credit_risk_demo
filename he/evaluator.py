def encrypted_linear_score(enc_x, weights, bias):

    result = enc_x.dot(weights)

    result += bias

    return result