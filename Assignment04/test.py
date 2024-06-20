""" P(R|c, -s, w) """
# P(r|c, -s, w) = alpha * P(r, c, -s, w) = alpha * P(r|c)P(c)P(-s|c)P(w|-s, r)
P_r_given_c_nots_w = bn.P['R'][True, True] * bn.P['C'][True] * bn.P['S'][True, False] * bn.P['W'][False, True, True]
# P(-r|c, -s, w) = alpha * P(-r, c, -s, w) = alpha * P(-r|c)P(c)P(-s|c)P(w|-s, -r)
P_notr_given_c_nots_w = bn.P['R'][True, False] * bn.P['C'][True] * bn.P['S'][True, False] * bn.P['W'][False, False, True]
# Calculate alpha: P(r|c, -s, w) * alpha + P(-r|c, -s, w) * alpha = 1
alpha = 1 / (P_r_given_c_nots_w + P_notr_given_c_nots_w)