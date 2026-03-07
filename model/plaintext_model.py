def compute_plain(x, weights, bias):

    return sum(w * xi for w, xi in zip(weights, x)) + bias