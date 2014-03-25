__author__ = 'Zhenyu'

"pip install biplist"
import biplist
import os
import glob

def ios_sim_location_authorize(bundle_id, on_off='on'):
    '''
    Give location authorization to app according to the Bundle ID.
    Change the .plist file in simulator folder.
    '''

    tmp = os.path.join(os.path.expanduser("~/Library"), "Application Support", "iPhone Simulator", "*.*", "Library")
    paths = glob.glob(tmp)

    for sim_dir in paths:
        sim_dir = os.path.join(sim_dir, 'Caches')
        if not os.path.exists(sim_dir):
            os.mkdir(sim_dir)
        sim_dir = os.path.join(sim_dir, 'locationd')
        if not os.path.exists(sim_dir):
            os.mkdir(sim_dir)

        existing_path = os.path.join(sim_dir, 'clients.plist')
        if os.path.exists(existing_path):
            plist = biplist.readPlist(existing_path)
        else:
            plist = {}

        if bundle_id not in plist:
            plist[bundle_id] = {}

        plist[bundle_id]["BundleId"] = bundle_id
        plist[bundle_id]["Authorized"] = True if on_off == "on" else False
        plist[bundle_id]["LocationTimeStarted"] = 0

        biplist.writePlist(plist, existing_path)

'''
ios_sim_location_authorize('com.microstrategy.alert')
'''