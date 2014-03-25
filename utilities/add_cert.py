__author__ = 'Zhenyu'

import os
import glob
import shutil

def add_mitmproxy_certificate(cert=os.path.expanduser("~/.mitmproxy/TrustStore.sqlite3")):
    """
    replace the TrustStore.sqlite3 file for each simulator.
    add the certificate in the TrustStore.sqlite3 file in advance. (use iosCertTrustManager)

    refer:
        MITMProxy
        iosCertTrustManager.py
    """
    tmp = os.path.join(os.path.expanduser("~/Library"), "Application Support", "iPhone Simulator", "*.*", "Library", "Keychains")
    paths = glob.glob(tmp)
    for sim_dir in paths:
        shutil.copyfile(cert, os.path.join(sim_dir, "TrustStore.sqlite3"))