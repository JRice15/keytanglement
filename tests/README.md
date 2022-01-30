# Description of Test Cases

###########
# Test  1 #
###########
Scenario: Both Alice's and Bob's lists of qubit-pairs and group codes are identical.

Result: Both Alice and Bob should receive a list of correct measurements indicating that all
        of Bob's reversal circuits and group codes matched Alice's circuits and group codes.
        Both Alice and Bob should receive identical keys corresponding to all of the group codes
        that weren't used in consistency checking.


###########
# Test  2 #
###########
Scenario: Alice's and Bob's lists of qubit-pairs are identical. The first group code in Alice's
          and Bob's group code list is different.

Result: Both Alice and Bob should receive a list of correct measurements indicating that only one
        of Bob's reversal circuits and group codes did not match the corresponding circuit and group code
        in Alice's circuits and group codes. Both Alice and Bob should receive identical keys corresponding 
        to all of the matching group codes that weren't used in consistency checking.


###########
# Test  3 #
###########
Scenario: Alice's and Bob's lists of group codes are identical. The third qubit-pair in Alice's
          and Bob's group code list is different.

Result: Both Alice and Bob should receive a list of correct measurements indicating that only one
        of Bob's reversal circuits and group codes did not match the corresponding circuit and group code
        in Alice's circuits and group codes. Both Alice and Bob should receive identical keys corresponding 
        to all of the matching group codes that weren't used in consistency checking.
