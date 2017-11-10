# -*- coding: utf-8 -*-

from lib.OpenStack import OpenstackAPI
# from lib.OpenStack import OutputHTML


def main():
    host = "172.17.11.105"
    compute = "172.17.11.110"
    username = "admin"
    password = "NCTU@osrootAdmin"
    imagename = "cirros"
    flavorname = "m1.nano"

# init connect
    api = OpenstackAPI(host, compute, username, password)
    api.getToken()
# image init, create 'imagename'
    api.getImage()
    imageID = api.CreateImage(imagename)
    print("\n==========================================")
    api.getImageDetail(imageID)
# flavor init, create 'flavorname'
    print("\n==========================================")
    # api.getToken()
    print("getServerID")
    print(api.getServerID('nova'))
    print("\n==========================================")
    print("getFlavorLists")
    api.getFlavorLists()
    flavorID = api.createFlavor(flavorname=flavorname)
    api.getFlavorLists()
    print("\n==========================================")
    api.getFlavorDetail(flavorID)
# create server
    api.createServerByAuto(imageID, flavorID)
    api.getServerLists()


if __name__ == "__main__":
    main()
