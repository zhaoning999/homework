## part1 writeup

### bug 1: XSS

In the LegacySite/views.py, line 70, a variable named director which is part of user request is directly fed into context, so that it will be rendered on the templates/item-single.html and templates/gift.html. Moreover, the place where the director is referenced is marked as safe in templates, so we can acheive a XSS with a simple JavaScript in our GET request: GET /buy.html?director=<script type="text/javascript">alert('XSS'); </script>

To prevent this kind of attack, we should sanitize user input by filtering out special characters in JavaScript like semicolon, and django's renderer makes this as default. So the problem occurs on the safe tag at the director in those two templates. We should remove the safe tag on templates.



### bug 2: unauthorized purchase

In the LegacySite/views.py the gift_card_view function didn't check whether user in the request is identical to the user currently logged in. So the attacker can purchase a gift card in the name of other users without their knowledge. To make this attack happen, modify the request sent by attacker, by modifying the parameter user to another user which exists on the server.

To prevent this, the server should check whether the user in the request received is the same as the one who currently logged in.



### bug 3: SQL injection

The raw SQL query in the LegacySite/views.py line 193-194 is noticed. It performs a query to the card database to check if the signature is valid. However, if we modify the downloaded giftcard file(which turns out to be a json string) with malicious SQLi payload, it will show us the content we want, like content in the password database LegacySite_user.

To prevent this, we should avoid using raw SQL query, and sanitize user input as well. Moreover, the integrity of the file should be provided by signature.



### bug 4: same seed every time

In LegacySite/extras.py, the generate_salt() function initializes random seed every time it is called. However, the seed it uses is one of the configs in GiftcardSite/conf.py, which is expected to be a constant. Therefore, every time the function is called, it will produce the same output, as random() is pseudo-random stream cipher whose output relies on the initial vector.

To prevent this bug, one should only initialize the seed once in the program.



### bug 5:  misuse of system()

Also in LegacySite/extras.py, call of system() is seen. This line of code is dangerous, as it enables user input to have arbitrate command run on server.

We should not rely on external binary to perform any action, as it will use system() function.

 