__author__ = "shikun"
import pickle
import os

def write(data, path="data.pickle"):
    with open(path, 'wb') as f:
        pickle.dump(data, f, 0)
def read(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}
            # print("读取文件错误")
    # print("------read-------")
    # print(data)
    return data

def readInfo(path):
    # data = []
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            print(data)
        except EOFError:
            data = []
            # print("读取文件错误")
    # print("------read-------")
    # print(data)
    return data



def writeInfo(data="", path="data.pickle"):
    """

    :type data: dict
    """
    _read = readInfo(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:
        # print("------writeInfo-------")
        # print(result)
        pickle.dump(result, f)

if __name__ == "__main__":
    # write("用例失败重连过一次，失败原因：", "../Log/connect64dd15b8-ca91-11e7-87ae-38c98647adce.pickle")
    pass