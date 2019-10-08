#!/bin/bash

pushd /media/nas/sunkw/grabpages
/usr/bin/python3 grab.py sohu &
/usr/bin/python3 grab.py people &
/usr/bin/python3 grab.py xinhuanet &
/usr/bin/python3 grab.py mydrivers &
/usr/bin/python3 grab.py tianya &
/usr/bin/python3 grab.py cnbeta &
/usr/bin/python3 grab.py jandan &
/usr/bin/python3 grab.py jianshu &
/usr/bin/python3 grab.py jiqizhixin &
/usr/bin/python3 grab.py hupu &
