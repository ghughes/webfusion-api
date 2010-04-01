## Admin API for Webfusion dedicated servers

This is a simple Python API to the custom control panel installed by default on [Webfusion](http://www.webfusion.com/) dedicated servers. It is currently quite limited in terms of advanced functionality; please feel free to fork and add to it.

The module is fully compatible with both their Ubuntu Linux and Windows server control panels.

### Usage

Authentication is required before anything else can be done:

    >>> import webfusion
    >>> webfusion.server = 'server1234.dedicated.webfusion.co.uk'
    >>> webfusion.auth('admin', 'password')
    True
    
Listing all accounts:

    >>> webfusion.list_accounts()
    [('foo', 'windows', 'foo.com'), ('bar', 'windows', 'bar.com')]
    
Creating an account with 20MB disk, 100MB transfer, and no features except for MSSQL and Frontpage:

    >>> webfusion.create_acct('baz', 'password', disk=20, mailboxes=0, responders=0, mra=0, transfer=100, cp=False, ssl=False, mysql=False, mssql=True, frontpage=True, ftp=False, stats=False, dns=False)
    (True, None)
    
Now let's add a domain to that account:

    >>> webfusion.add_domain('baz.com', 'baz')
    (True, None)
    
### Notes

When creating an account on a Linux server, you must set `platform='unix'`.

`create_acct` and `add_domain` always return a tuple containing a boolean and error message.

## License

This code is dedicated to the public domain.

## Author

Written by [Greg Hughes](http://ghughes.com/) in November 2009.