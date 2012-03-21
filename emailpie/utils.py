import re

import gevent

from DNS.Base import ServerError

from emailpie import settings


def mxlookup(domain):
    from DNS import Base

    def dnslookup(name, qtype):
        """convenience routine to return just answer data for any query type"""
        if Base.defaults['server'] == []: Base.DiscoverNameServers()
        result = Base.DnsRequest(name=name, qtype=qtype, timout=5).req()
        if result.header['status'] != 'NOERROR':
            raise ServerError("DNS query status: %s" % result.header['status'],
                result.header['rcode'])
        elif len(result.answers) == 0 and Base.defaults['server_rotate']:
            # check with next DNS server
            result = Base.DnsRequest(name=name, qtype=qtype, timout=5).req()
        if result.header['status'] != 'NOERROR':
            raise ServerError("DNS query status: %s" % result.header['status'],
                result.header['rcode'])
        return [x['data'] for x in result.answers]

    def _mxlookup(name):
        """
        convenience routine for doing an MX lookup of a name. returns a
        sorted list of (preference, mail exchanger) records
        """
        l = dnslookup(name, qtype='mx')
        l.sort()
        return l

    return _mxlookup(domain)


class EmailChecker(object):
    """
    Given an email address, run a variety of checks on that email address.

    A check is any method starting with `check_` that returns a list of errors.
    Errors are dictionaries with a message (str) and severity (int) key.
    """

    def __init__(self, email, _gevent=settings.GEVENT_CHECKS):
        self.email = email
        self.errors = []
        self.mx_records = None

        self._gevent = _gevent

    @property
    def username(self):
        return self.email.split('@')[0]

    @property
    def domain(self):
        try:
            return self.email.split('@')[1]
        except IndexError:
            return None

    def didyoumean(self):
        from emailpie.spelling import correct

        if self.domain:
            items = self.domain.split('.')

            suggestion = '{0}@{1}'.format(
                self.username,
                '.'.join(map(correct, items))
            )

            if suggestion == self.email:
                return None
            return suggestion

        return None

    @property
    def checks(self):
        """
        Collects all functions that start with `check_`.
        """
        out = []
        for name in dir(self):
            if name.startswith('check_'):
                out.append(getattr(self, name))
        return out

    def validate(self):
        """
            1. Run each check, fill up self.jobs.
            2. Join all jobs together.
            3. Each job returns a list of errors.
            4. Condense and return each error.
        """
        if self._gevent:
            results = [gevent.spawn(check) for check in self.checks]
            gevent.joinall(results, timeout=7)

            for result in results:
                if result.value:
                    self.errors += result.value
        else:
            for result in [check() for check in self.checks]:
                self.errors += result

        return self.errors


    ############
    ## CHECKS ##
    ############
    
    def check_valid_email_string(self):
        """
        A simple regex based checker.
        """
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(self.email)
            return []
        except:
            return [dict(
                severity=10,
                message='Invalid email address.'
            )]

    def check_valid_mx_records(self):
        """
        Ensures that there are MX records for this domain.
        """
        error = dict(
            severity=7,
            message='No MX records found for the domain.'
        )

        if not self.domain:
            return [error]

        try:
            self.mx_records = mxlookup(self.domain)
            if len(self.mx_records) == 0:
                return [error]
        except ServerError:
            return [error]

        return []

    def check_nothing(self):
        return []