This code was developed as part of the CloudFest 2019 Hackathon.

* It does not work with currently available versions of cPanel.
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
