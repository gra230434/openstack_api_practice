# OpenStack API Create A Server

## 環境
使用語言: Python 2.7.12<br>
使用函式庫: requests、json<br>
作業系統不限，在 windows 或是在 Linux 上都可以執行

## 事前準備
查看 Python 版本 `python --version` 這邊應該顯示 `Python 2.7.12`

安裝兩個函式庫 requests、json<br>
`pip install requests`<br>
`pip install simplejson`

## 變數更換
所有變數都在main.py中設定，所以使用前必須在這邊先修改變數內容

host : 使用伺服器，domain name 或是 IP<br>
username : 使用者帳號<br>
password : 使用者密碼<br>
imagename : image的名稱<br>
flavorname : flavor的名稱

image 的創建過程
 - 是否以前已經創建過
 - 如果創建過將不會再創新的 image

flavor 的創建過程
 - 是否以前創建過，檢查 name 以及 ID
 - 已經被創建過，將會檢查 vcpu vram disk
 - 如果全部相符，將不創新的 flavor

## 執行程式
`python main.py`<br>
無須輸入其他變數，因為變數應該在main.py中都定義好了。

## 注意
createFlavor 函數會輸入vcpu vram disk的變數，如果不設定將會用下面的變數取代<br>
`vcpu=2, ram=1024, disk=10`
