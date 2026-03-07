import tenseal as ts

def encrypt_vector(context, vector):

    return ts.ckks_vector(context, vector)