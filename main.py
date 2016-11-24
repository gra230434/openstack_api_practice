#encoding=utf-8

import requests
import json

class OpenstackAPI:
    def __init__(self):
        self.identity = self.IdentityAPI()
        self.image = self.ImageServiceAPI()
        self.flavor = self.FlavorServiceAPI()

    # 定義 flavor
    def FlavorServiceAPI(self):
        header = {"Content-Type":"application/json","X-Auth-Token":""}
        return {"url":"http://controller:8774/v2/flavors","header":header}

    # 定義 image
    def ImageServiceAPI(self):
        header = {
                "Content-Type":"application/json",
                "X-Auth-Token":""
                }
        return {"url":"http://controller:9292/v2/images","header":header}

    # 定義 identity
    def IdentityAPI(self):
        url = "http://controller:35357/v3/auth/tokens"
        body = {
                "auth":{
                    "identity":{
                        "methods":[
                            "password"
                            ],
                        "password":{
                            "user":{
                                "name":"admin",
                                "domain":{
                                    "name":"Default"
                                    },
                                "password":"cloud2016"
                                }
                            }
                        }
                    }
                }
        header = {"Content-Type":"application/json"}

        return {"url":url,"header":header,"body":body}

    # 取得 token
    def getToken(self):
        r = requests.post(self.identity["url"],headers=self.identity["header"],data=json.dumps(self.identity["body"]))
        self.token = r.headers["X-Subject-Token"]
        print("Get a token: "+ self.token)


    # 取得 flavor ，相當於 openstack flavor list，將第一筆 flavor 名字儲存(request 資料可能有問題
    # URL 跟 header 還須更改
    def getFlavor(self):
        self.flavor["header"]["X-Auth-Token"] = self.token
        r = requests.get(self.flavor["url"],headers=self.flavor["header"])
        print(r.text)

    # 取得 image ，相當於 openstack image list，將第一筆image id儲存
    def getImage(self):
        self.image["header"]["X-Auth-Token"] = self.token
        r = requests.get(self.image["url"],headers=self.image["header"])
        self.images = json.loads(r.text)
        self.firstImage = ""
        if len(self.images["images"]) > 0:
            self.firstImage = self.images["images"][0]["id"]
        print("Find a image: "+ self.firstImage)

    #還沒做
    def createInstance(self,token,flover,image):
        print("Nothing...")


def main():
    api = OpenstackAPI()
    api.getToken()
    api.getImage()
    api.getFlavor()


if __name__ == "__main__":
  main()
