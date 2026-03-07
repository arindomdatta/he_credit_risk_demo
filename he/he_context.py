import tenseal as ts
import config

def create_context():

    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=config.POLY_MODULUS_DEGREE,
        coeff_mod_bit_sizes=config.COEFF_MOD_BIT_SIZES
    )

    context.generate_galois_keys()
    context.generate_relin_keys()

    context.global_scale = config.SCALE

    return context