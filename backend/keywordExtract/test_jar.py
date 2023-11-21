import os

import jpype
import threading
from jpype import *

class PyJar:
    def __init__(self, path):
        self.path = path

    def initialize(self):
        if not jpype.isJVMStarted():
            jvmPath = jpype.getDefaultJVMPath()
            jpype.startJVM(jvmPath, "-ea", r"-Djava.class.path={}".format(self.path))

    def finalize(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()

    def jClass(self, classpath):
        return jpype.JClass(classpath)


def javaMain(txt_path='test_data50',jar_path="storyteller_3.jar"):
    # jar = PyJar("keywordExtract/storyforest8.jar")
    # txt_path='test_data50'
    file_list=os.listdir(txt_path)
    if len(file_list)>0:
        file_name=txt_path+'/' +file_list[0]
        os.remove(file_name)

    jar = PyJar("keywordExtract/storyteller_3.jar")

    jar.initialize()
    # pr
    storyteller = jar.jClass("edu.ualberta.storyteller.storylayer.StoryLayer")  # 取得Java类

    print("storyteller", storyteller)
    
    storyteller.main([])

    # jar.finalize()

def testJavaMain():
    # t1=threading.Thread(target=javaMain(),args=('test_data50',"keywordExtract/storyteller_test.jar"))
    # t2 = threading.Thread(target=javaMain(), args=('test_data_ori', "keywordExtract/storyteller_ori.jar"))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()

    jar_path1="keywordExtract/storyteller_3.jar"
    jar_path2="keywordExtract/storyteller_3.jar"
    jar_path="-Djava.class.path=%s;%s"%(jar_path1,jar_path2)
    try:
        jpype.startJVM(jpype.getDefaultJVMPath(),"-ea",jar_path)
    except:
        pass
    storyteller=jpype.JClass("edu.ualberta.storyteller.storylayer.StoryLayer")
    storytellerOri = jpype.JClass("edu.ualberta.storyteller.storylayer.StoryLayerOri")
    storyteller.main([])
    storytellerOri.main([])
    # jpype.shutdownJVM()
    # javaMain('test_data50',"keywordExtract/storyteller_test.jar")
    # javaMain('test_data_ori', "keywordExtract/storyteller_ori.jar")

if __name__ == '__main__':
    javaMain('test_data50',"keywordExtract/storyteller_3.jar")