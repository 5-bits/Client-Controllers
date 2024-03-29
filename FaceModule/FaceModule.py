import cv2

class FaceModule :

    def __init__(self):
        cv2.namedWindow("Camera")
        self.vc = None
        self.rval = None
        self.b = None
        self.bs = None
        self.center = None
        print("Facemodule initialised")

    def activate(self):
        print("Activating camera...")
        self.vc = cv2.VideoCapture(0)
        if self.vc.isOpened(): # try to get the first frame
            print("Camera activated")
            self.rval, self.b = self.vc.read()
            self.bs = self.b.shape
            self.center = (self.bs[1]//2, self.bs[0]//2)
        else:
            self.rval = False
    
    def continuous(self):
        while self.rval:
            self.rval, self.b = self.vc.read()
            gray=cv2.cvtColor(self.b,cv2.COLOR_BGR2GRAY)
            face= cv2\
                .CascadeClassifier('haarcascade_frontalface_default.xml')\
                .detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10)

            cv2.circle(self.b, self.center, 8, (0,255,0), -1)
            
            for (x,y,w,h) in face:
                cv2.rectangle(self.b,(x,y),(x+w,y+h),(0,255,0),5)
                cv2.circle(self.b, (x+w//2, y+h//2), 3, (0,255,0), -1)
                cv2.line(self.b, (x+w//2, y+h//2), self.center, (255,0,0), 2)
            cv2.imshow("Camera", self.b)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
        
        print("Deactivating camera...")
        self.deactivate()

    def single(self):
        self.rval, self.b = self.vc.read()
        gray=cv2.cvtColor(self.b,cv2.COLOR_BGR2GRAY)
        face= cv2\
                .CascadeClassifier('haarcascade_frontalface_default.xml')\
                .detectMultiScale(gray,scaleFactor=1.1,minNeighbors=10)

        cv2.circle(self.b, self.center, 8, (0,255,0), -1)

        if len(face)>0:
            x,y,w,h =  face[0]
            cv2.rectangle(self.b,(x,y),(x+w,y+h),(0,255,0),5)
            cv2.circle(self.b, (x+w//2, y+h//2), 3, (0,255,0), -1)
            cv2.line(self.b, (x+w//2, y+h//2), self.center, (255,0,0), 2)
            self.printDirection(x,y,w,h)
        self.show()

    def printDirection(self,x,y,w,h):
        nx = x+w//2
        ny = y+h//2

        tolx = 0.75
        toly = 0.75

        if self.center[0]>x+(1-tolx)*w and self.center[0]<x+tolx*w:
            print("O", end=" ")
        elif self.center[0]>nx:
            print("L", end=" ")
        elif self.center[0]<nx:
            print("R", end=" ")

        if self.center[1]>y+(1-toly)*h and self.center[1]<y+toly*h:
            print("O")
        elif self.center[1]>ny:
            print("U")
        elif self.center[1]<ny:
            print("D")


    def show(self):
        cv2.imshow("Camera", self.b)
        key = cv2.waitKey(200)
    
    def deactivate(self):
        cv2.destroyWindow("Camera")
        self.vc.release()
        print("Camera Deactivated")

import time

if __name__=='__main__':
    f = FaceModule()
    f.activate()
    
    target = time.time()+60
    while(time.time()<=target):
        f.single()
    f.deactivate()
