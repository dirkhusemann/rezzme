rezzme launcher (IBM version)
=============================

the rezzme launcher is a protocol handler that knows how to interpret
rezzme:// style URIs. the rezzme launcher tries to obtain sufficient
information from the target grid via the GridInfo protocol to
configure the virtual world client (usually the SecondLife(R)
client). it currently tries to obtain:

* `login` for the `-loginuri` parameter
* `welcome` for the `-loginpage` parameter
* `economy` for the `-helperuri` parameter

the IBM version of the rezzme launcher in addition requires 

* `authenticator`

to be present and will obtain the avatar name and avatar password via
the authenticator URI after authenticating via Lotus3D collaboration
layer.
