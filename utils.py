payment_type_rep_to_code = {}
for rep in ["credit", "crd", "cre","1"]:
    payment_type_rep_to_code[rep] = 1
for rep in ["cash", "cas", "csh","2"]:
    payment_type_rep_to_code[rep] = 2
for rep in ["no charge", "noc", "no","3"]:
    payment_type_rep_to_code[rep] = 3
for rep in ["dispute", "dis","4"]:
    payment_type_rep_to_code[rep] = 4
for rep in ["unk","5"]:
    payment_type_rep_to_code[rep] = 5
payment_type_rep_to_code["6"] = 6