import sys

def hmm_filtering(params, evidences):
    """ P(x_t | X_t-1)
        X_t-1   P(x_t)
          T       b
          F       c
    """
    """ P(e_t | X_t)
          X_t   P(e_t)
           T      d
           F      f
    """
    a, b, c, d, f = params

    # Base case: P(X0) = <a, 1 - a>
    # Filtering: P(X_t | e_1:t) = <P(x_t | e_1:t), P(-x_t | e_1:t)>
    prev_prob = [a, 1 - a]
    
    for e in evidences:
        # Sensor: P(e_t+1 | X_t+1)
        if e == 't': # <P(e_t+1 | x_t+1), P(e_t+1 | -x_t+1)>
            sensor_prob = [d, f]
        else: # (e == 'f'): <P(-e_t+1 | x_t+1), P(-e_t+1 | -x_t+1)>
            sensor_prob = [1 - d, 1 - f]

        # Sigma: E_xt~[P(X_t+1 | x_t) * P(x_t | e_1:t)]
        #     =  <P(x_t+1 | x_t) * P(x_t | e_1:t) + P(x_t+1 | -x_t) * P(-x_t | e_1:t),
        #         P(-x_t+1 | x_t) * P(x_t | e_1:t) + P(-x_t+1 | -x_t) * P(-x_t | e_1:t)>
        sigma_prob = [b * prev_prob[0] + c * prev_prob[1], (1 - b) * prev_prob[0] + (1 - c) * prev_prob[1]]

        # alpha * <P(e_t+1 | x_t+1), P(e_t+1 | -x_t+1)> * E_xt~[P(X_t+1 | x_t) * P(x_t | e_1:t)]
        prob = [sensor_prob[0] * sigma_prob[0], sensor_prob[1] * sigma_prob[1]]

        # Calculate alpha: alpha * prob[0] + alpha * prob[1] = 1
        alpha = 1 / (prob[0] + prob[1])

        # Update filtering probability: P(X_t | e_1:t) = <P(x_t | e_1:t), P(-x_t | e_1:t)>
        prev_prob = [prob[0] * alpha, prob[1] * alpha]

    return prev_prob

if __name__ == "__main__":

    # Check input status
    if (len(sys.argv) != 2):
        print("Usage: python hmm.py <file_name>")
        sys.exit(1)
    
    # Read input file
    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            variables = line.split(',')
            params = list(map(float, variables[:5]))
            evidences = variables[5:]
            probabilities = hmm_filtering(params, evidences)
            print(f'{line}--><{"{:.4f}".format(probabilities[0])},{"{:.4f}".format(probabilities[1])}>')
            
