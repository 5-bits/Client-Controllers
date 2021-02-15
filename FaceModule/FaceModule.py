import cv2
cv2.namedWindow("Recogniser")
vc = cv2.VideoCapture(0)

b = None
bs = None
center = None

if vc.isOpened(): # try to get the first frame
    rval, b = vc.read()
    bs = b.shape
    center = (bs[1]//2, bs[0]//2)
else:
    rval = False

while rval:
    rval, b = vc.read()
    bill_gray=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    face= cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(bill_gray,scaleFactor=1.1,minNeighbors=5)
    cv2.circle(b, center, 8, (0,255,0), -1)
    for (x,y,w,h) in face:
        cv2.rectangle(b,(x,y),(x+w,y+h),(0,255,0),5)
        cv2.circle(b, (x+w//2, y+h//2), 3, (0,255,0), -1)
        cv2.line(b, (x+w//2, y+h//2), center, (255,0,0), 2)

    cv2.imshow("Recogniser", b)
    rval, b = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

# print(b.shape)

cv2.destroyWindow("Recogniser")
vc.release()
