# PrefixCleaner
Cleans every objects of a prefix in RIPE DB

You just need to run it with Python3
It will prompt for the prefix and object type and password.
You have 4 options: "inetnum", "route", "domain" or "all" for all of them. Also you need to enter your default maintainer password (or a maintainer that is authorized for all of objects)

Version 0.0.2:
Creating route objects is possible with this verion.
You need to run create.py with Python3 and fill the requested values.
It will automatically makes smaller subnets with the CIDR size that you choose.

