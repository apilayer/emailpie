import re

import gevent
from gevent import monkey


def mxlookup(domain):
    from DNS import Base
    from DNS.Base import ServerError

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
    """

    def __init__(self, email, _gevent=True):
        self.email = email
        self.errors = []

        self._gevent = _gevent

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
            monkey.patch_all()
            self.results = [gevent.spawn(check) for check in self.checks]
            gevent.joinall(self.results)

            for result in self.results:
                self.errors += result.value
        else:
            self.results = [check() for check in self.checks]

            for result in self.results:
                self.errors += result

        return self.errors


    ############
    ## CHECKS ##
    ############
    
    def check_valid_email_string(self):
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
        error = dict(
            severity=5,
            message='No MX records found for the domain.'
        )

        try:
            domain = self.email.split('@')[1]
        except IndexError:
            return [error]

        mx_hosts = mxlookup(domain)

        if len(mx_hosts) == 0:
            return [error]

        return []