###########
# PARSERS #
###########

string_to_smplcs = lambda st: [smplx.replace("}", "") for smplx in st.split("}, ")]

smplcs_to_cmplx  = lambda smplcs: [smplx.replace("{", "").replace(" ", "").split(',') for smplx in smplcs]