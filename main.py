# -*- coding: utf-8 -*-

from lib.OpenStack import OpenstackAPI
# from lib.OpenStack import OutputHTML


def main():
    host = "192.168.0.20"
    username = "admin"
    password = "cloud2016"
    imagename = "cirros"
    flavorname = "m1.nano"

# init connect
    api = OpenstackAPI(host, username, password)
    api.getToken()
# image init, create 'imagename'
    exists, imageID = api.getImage(imagename)
    if not exists:
        imageID = api.CreateImage(imagename)
    api.getImageDetail(imageID)

# flavor init, create 'flavorname'
    api.getFlavorLists()
    flavorID = api.createFlavor(flavorname=flavorname)
    api.getFlavorLists()
    api.getFlavorDetail(flavorID)


if __name__ == "__main__":
    main()
