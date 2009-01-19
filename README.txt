rezzme launcher
===============

the rezzme launcher is a protocol handler that knows how to interpret
rezzme:// style URIs. the rezzme launcher tries to obtain sufficient
information from the target grid via the GridInfo protocol to
configure the virtual world client (usually the SecondLife(R)
client). it currently tries to obtain:

* `login` for the `-loginuri` parameter
* `welcome` for the `-loginpage` parameter
* `economy` for the `-helperuri` parameter

in addition the launcher will check for the 'authenticator' key:

* `authenticator` 

if it is present, rezzme will obtain the avatar name and avatar
password via the authenticator URI.


windows install note
====================

unless you quit any running rezzme system tray "icons", you will have
to reboot once the rezzme installer has done its job. due to the
design of windows there is not much we can do about this. sorry.

