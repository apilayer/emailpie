# A simple email validation API.

Give us an email and we make sure its legit. If not, you'll find out why.


### Features

* Normal regex based check.
* Ensures DNS records exist for the mail exchange.
* TODO: Simple telnet check for IMAP or SMTP (http://www.webdigi.co.uk/blog/2009/how-to-check-if-an-email-address-exists-without-sending-an-email/)
* TODO: Suggest fixes to common misspellings. lulz@gnail.com -> did you mean lulz@**gmail**.com.
* TODO: Throttle requests by IP (redis based).


### Install/Usage

1. `git clone git@github.com:bryanhelmig/emailpie.git`
2. `cd emailpie`
3. `mkvirtualenv emailpie`
4. `pip install -r requirements`
5. `python rundev.py`
6. Visit http://localhost:5000/v1/check?email=test@gmail.com
