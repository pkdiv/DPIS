from api import Api

if __name__ == "__main__":
    api = Api()
    imgpath = "E:\\DPIS\\finger.png"
    print(api.call(imgpath))
