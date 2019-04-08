This code was developed as part of the CloudFest 2019 Hackathon.

* It does not work with currently available versions of cPanel.
* If you're internal to cPanel, it's using so_support_dispatch branch of cPanelScott/cpanel-domain-connect.git or 11.81.9006.2
* It is a work in progress, under significant developmennt.

To use this:

    # cd /usr/local/cpanel/base/3rdparty
    # git clone <cloneurl>
    # ln -s cpanel-domain-connect/discovery domainconnect_discovery
    # ln -s cpanel-domain-connect/authorization domainconnect_authorization
    # curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    # /usr/local/cpanel/3rdparty/bin/python get-pip.py
    # rm get-pip.py
    # pip install Flask

The followings paths sorta work:

Non-Authenticated:
https://IP:2087/domainconnect/v2/car.com/settings (The domain must exist as a domain in WHM)
https://IP:2087/domainconnect/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template2

Requires authentication with cPanel account:
https://IP:2083/3rdparty/domainconnect_authorization/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template1/apply?domain=car.com&IP=1.1.1.1&RANDOMTEXT=jibberjabber
