#%%############################################################################
# Returns the generating polynomial of order n as a column vector of coefficients.
###############################################################################
# Maximum length feedback polynomial coefficients obtained from
# https://en.wikipedia.org/wiki/Linear-feedback_shift_register

def generating_polynomial(n):
    if n == 2:
        gp = [1, 1]
    elif n == 3:
        gp = [0, 1, 1]
    elif n == 4:
        gp = [0, 0, 1, 1]
    elif n == 5:
        gp = [0, 0, 1, 0, 1]
    elif n == 6:
        gp = [0, 0, 0, 0, 1, 1]
    elif n == 7:
        gp = [0, 0, 0, 0, 0, 1, 1]
    elif n == 8:
        gp = [0, 0, 0, 1, 1, 1, 0, 1]
    elif n == 9:
        gp = [0, 0, 0, 0, 1, 0, 0, 0, 1]
    elif n == 10:
        gp = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    elif n == 11:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    elif n == 12:
        gp = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
    elif n == 13:
        gp = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1]
    elif n == 14:
        gp = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
    elif n == 15:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    elif n == 16:
        gp = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1]
    elif n == 17:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    elif n == 18:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
    elif n == 19:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1]
    elif n == 20:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
    elif n == 21:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    elif n == 22:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    elif n == 23:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    elif n == 24:
        gp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
    else:
        # TODO: Handle this case better.
        msg = 'The requested generating polynomial order is out the range of this function.'
        raise ValueError(msg)
        return -1
    return gp

#%%############################################################################
# This function implements a linear feedback shift register (LFSR) to 
# generate one complete period of a binary pseudorandom sequence given by 
# the input generating polynomial (gp) and initial state (initial_state).
#
# The generating polynomial is specified by a row vector of zeros or ones
# corresponding to the coefficients of the polynomial with x^0 = 1 assumed.
# E.g. [1 0 1 0 1] is the polynomial  1 + x^1 + x^3 + x^5.
#
# The initial_state must also be a row vector of zeros and ones. It must
# have the same length as generating_polynomial and not consist entirely of
# zeros.
###############################################################################
def LFSR(gp, initial_state):
    # Number of bits in the register.
    m = len(gp)
    # Ensure the initial state length is equal to the degree of the generating
    # polynomial.
    if m != len(initial_state):
        # TODO: Handle this error better.
        msg = 'generating_polynomial and intitial_state must be the same length.'
        raise ValueError(msg)
    
    # Ensure the generating_polynomial and initial_state are only ones and zeros and not all zeros.
    if not any(i != 1.0 or i != 0.0 for i in gp) or all(i == 0.0 for i in gp):
        msg = 'Invalid generating_polnomial.'
        raise ValueError(msg)
    
    if (not all(i == 1 or i == 0 for i in gp)) or all(i == 0 for i in initial_state):
        msg = 'Invalid initial_state.'
        raise ValueError(msg)
    
    # Length of the PN sequence before it will repeat.
    L = 2**m - 1
    
    # Initialize shift register and PN sequence.
    # This makes shift_register a reference to initial_state
    shift_register = initial_state
    PN_seq = [0 for i in range(L)]
    
    for p in range(L):
        e = shift_register[-1]
        PN_seq[p] = e
        e = sum([gp[i]*shift_register[i] for i in range(len(gp))])%2        
        shift_register.insert(0, e)
        shift_register.pop()

    return PN_seq
    

#%%############################################################################
# Test the above functions.
###############################################################################
#nBits = 6
#gp = generating_polynomial(nBits)
#initial_state = [1 for i in range(nBits)]
#
#PN_seq = LFSR(gp, initial_state)
#
#print '\nPN_seq = '
#print PN_seq
#print 'len(PN_seq) = ' + str(len(PN_seq))





















