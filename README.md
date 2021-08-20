# random_id_generator
Short Script that grabs an image from thispersondoesnotexist.com, analyses it regarding approximate age and gender and saves the output.\n
You can for example use this to create anonymous identities for websites that require a full name.

# Usage
`python generator.py`\n
Use `-f`/`-m` for female/male identites only.\n
Use `-i` to store additional information like the website.\n
example: `python generator.py -f -i google.com` would create a female identity to use on google.com.

# Requirements
-opencv
