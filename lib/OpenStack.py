# -*- coding: utf-8 -*-

import requests
import json


class OpenstackAPI():

    token = ''
    header = ''
    imageID = ''
    imagelist = []
    flavorlist = []

    def __init__(self, host, compute, username, password):
        self.host = host
        self.url = "http://{}:8774/".format(self.host)
        self.compute = compute
        self.username = username
        self.password = password

# get token
    def getToken(self):
        url = "http://%s:35357/v3/auth/tokens" % (self.host)
        data = {'auth': {
                    'identity': {
                        'methods': ['password'],
                        'password': {
                            'user': {
                                'name': self.username,
                                'domain': {'name': 'Default'},
                                'password': self.password
                            }
                        }
                    },
                }}
        header = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        r = requests.post(url, headers=header, data=json_data)
        print(r.headers)
        print(r.text)
        self.token = r.headers['X-Subject-Token']
        self.ID = r.headers['x-openstack-request-id']
        self.header = {'X-Auth-Token': self.token,
                       'X-Openstack-Request-Id': self.ID}
        print("Token")
        print(self.token)
        print("New Header")
        print(self.header)

# get images
    def getImage(self, findimage=''):
        """ get Images from server
        if don't input findimage, the function don't response anything
        """
        tmplist = {}
        self.imagelist = []
        url = "http://%s:9292/v2/images" % (self.host)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        for value in range(len(json_data['images'])):
            tmplist['id'] = json_data['images'][value]['id']
            tmplist['name'] = json_data['images'][value]['name']
            tmplist['status'] = json_data['images'][value]['status']
            self.imagelist.append(tmplist)
            tmplist = {}

# get image by id
    def getImageDetail(self, imageID):
        url = "http://%s:9292/v2/images/%s" % (self.host, imageID)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        print json_data

# create image
    def CreateImage(self, imagename):
        response = ""
        data = {"name": imagename}
        for value in range(len(self.imagelist)):
            if imagename == self.imagelist[value]["name"]:
                response = self.imagelist[value]["id"]
        if not response:
            url = "http://%s:9292/v2/images" % (self.host)
            data = {"name": imagename}
            json_data = json.dumps(data)
            r = requests.post(url, headers=self.header, data=json_data)
            json_response = json.loads(r.text)
            response = json_response['id']
        return response

    def getServerID(self, servicename):
        url = "http://%s:35357/v3/services" % (self.host)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        for service in json_data['services']:
            if service['name'] == servicename:
                return service['id']
        return None

# get all flavors list
    def getFlavorLists(self):
        print("getFlavorLists")
        tmplist = {}
        self.flavorlist = []
        urlid = self.getServerID('nova')
        url = "{}/v2.1/flavors".format(self.url)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        print(r.headers)
        print(json_data)
        for value in range(len(json_data['flavors'])):
            tmplist['id'] = json_data['flavors'][value]['id']
            tmplist['name'] = json_data['flavors'][value]['name']
            self.flavorlist.append(tmplist)
            tmplist = {}

# get singal Flavor detail
    def getFlavorDetail(self, flavorID, vcpu='', vram='', disk=''):
        url = "http://%s:8774/v2.1/flavors/%s" % (self.host, flavorID)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        if vcpu and vram and disk:
            if vcpu != json_data["flavor"]["vcpus"] or \
               vram != json_data["flavor"]["ram"] or \
               disk != json_data["flavor"]["disk"]:
                return False, flavorID
            return True, flavorID
        else:
            print json_data

# delete a Flavor and no respones
    def deleteFlavor(self, flavorID):
        url = "http://%s:8774/v2.1/flavors/%s" % (self.host, flavorID)
        r = requests.delete(url, headers=self.header)
        if r.status_code == 202:
            return True
        else:
            return False

# create a Flavor and check flavor already exists
    def createFlavor(self, flavorname="test_flavor", ram=1024, cpu=2, disk=10):
        url = "http://%s:8774/v2.1/flavors" % (self.host)
        data = {"flavor": {
                    "name": flavorname,
                    "ram": ram,
                    "vcpus": cpu,
                    "disk": disk,
                    "id": "1",
               }}
        for value in range(len(self.flavorlist)):
            if data["flavor"]["name"] == self.flavorlist[value]["name"]:
                status, flavorID = self.getFlavorDetail(
                                        self.flavorlist[value]["id"],
                                        cpu, ram, disk)
                if status:
                    data["flavor"]["id"] == flavorID
                else:
                    if self.deleteFlavor(flavorID):
                        data["flavor"]["id"] == flavorID
                    json_data = json.dumps(data)
                    r = requests.post(url, headers=self.header, data=json_data)
                    json_data = json.loads(r.text)
        return flavorID

# create a server
    def createServerByAuto(self, imageID, flavorID):
        url = "http://%s:8774/v2.1/servers" % (self.host)
        data = {"server":
                {
                    "name": "auto-allocate-network",
                    "imageRef": imageID,
                    "flavorRef": flavorID,
                 }
                }
        json_data = json.dumps(data)
        r = requests.post(url, headers=self.header, data=json_data)
        json_response = json.loads(r.text)
        print(json_response)

# list servers
    def getServerLists(self):
        url = "http://%s:8774/v2.1/servers" % (self.host)
        r = requests.get(url, headers=self.header)
        json_data = json.loads(r.text)
        print(json_data)
