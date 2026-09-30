# 1. Get the text
# 2. Define a-z
# 3. Create dictionary with every letter starting at 0
# 4. Loop through the text and update counts
# 5. Loop through dictionary and print results

import string

counter = {letter: 0 for letter in string.ascii_lowercase}

string = "In this lab, we will introduce some simple Python commands. For more resources about Python in general, readers may want to consult the tutorial at docs.python.org/3/tutorial/"
alphabet = string.ascii_lowercase

for i in alphabet:
    if i in string.lower:
        counter[i] += 1

print(counter)