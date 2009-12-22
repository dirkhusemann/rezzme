RedHat specific README
======================

In contrast to Ubuntu/Debian based systems, RedHat based linux systems
do not have a system wide firefox/thunderbird configuration mechanism
(on Ubuntun/Debian we have /etc/firefox-3.0, /etc/firefox-3.5,
/etc/thunderbird for this purpose). This lack of a system wide,
version independent configuration mechanism means that you need to
configure your firefox and thunderbird clients yourself (and repeat
this after each update!), i'm really sorry about that.

you need to add the following config entries to firefox's and
thundebird's configurations:

    network.protocol-handler.app.rezzme    "/usr/bin/rezzme.py"
    network.protocol-handler.app.rezzmes   "/usr/bin/rezzme.py"

the easiest way to do this is via about:config.

Tip: a very good add-on for both firefox and thunderbird to deal with
about:config is "Mr Tech Toolkit" available at

    https://addons.mozilla.org/en-US/firefox/addon/421

alternatively you could do this via the prefs.js file of firefox
and thunderbird.
