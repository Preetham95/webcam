import cv2, time
import numpy as np

def moveWindow(*args,**kwargs):
    return cv2.moveWindow(*args,**kwargs)

def imshow(*args,**kwargs):
    return cv2.imshow(*args,**kwargs)
    
def destroyWindow(*args,**kwargs):
    return cv2.destroyWindow(*args,**kwargs)

def waitKey(*args,**kwargs):
    return cv2.waitKey(*args,**kwargs)

def combine(left, right):
    """Stack images horizontally.
    """
    h = max(left.shape[0], right.shape[0])
    w = left.shape[1] + right.shape[1]
    hoff = left.shape[0]
    
    shape = list(left.shape)
    shape[0] = h
    shape[1] = w
    
    comb = np.zeros(tuple(shape),left.dtype)
    
    # left will be on left, aligned top, with right on right
    comb[:left.shape[0],:left.shape[1]] = left
    comb[:right.shape[0],left.shape[1]:] = right
    
    return comb   

def plotXY(data,size = (240,640),margin = 10,name = "data",labels=[], skip = 3,
           showmax = [], bg = None):
    for x,y in data:
        if len(x) < 2 or len(y) < 2:
            return
    
    n_plots = len(data)
    w = float(size[1])
    h = size[0]/float(n_plots)
    
    z = np.zeros((size[0],size[1],3))
    
    if isinstance(bg,np.ndarray):
        wd = int(bg.shape[1]/bg.shape[0]*h )
        bg = cv2.resize(bg,(wd,int(h)))
        if len(bg.shape) == 3:
            r = combine(bg[:,:,0],z[:,:,0])
            g = combine(bg[:,:,1],z[:,:,1])
            b = combine(bg[:,:,2],z[:,:,2])
        else:
            r = combine(bg,z[:,:,0])
            g = combine(bg,z[:,:,1])
            b = combine(bg,z[:,:,2])
        z = cv2.merge([r,g,b])[:,:-wd,]    
    
    i = 0
    P = []
    for x,y in data:
        x = np.array(x)
        y = -np.array(y)
        
        xx = (w-2*margin)*(x - x.min()) / (x.max() - x.min())+margin
        yy = (h-2*margin)*(y - y.min()) / (y.max() - y.min())+margin + i*h
        
        mx = max(yy)
        if labels:
            if labels[i]:
                for ii in xrange(len(x)):
                    if ii%skip == 0:
                        col = (255,255,255)
                        cv2.putText(z,"%0.0f"%x[ii],(int(xx[ii]),int((i+1)*h)),
                                    cv2.FONT_HERSHEY_PLAIN,1,col)           
        if showmax:
            if showmax[i]:
                col = (0,255,0)    
                ii = np.argmax(-y)
                cv2.putText(z,"%0.0f %s" % (x[ii], showmax[i]),(int(xx[ii]),int((yy[ii]))),
                            cv2.FONT_HERSHEY_PLAIN,2,col)
        
        try:
            pts = np.array([[x_, y_] for x_, y_ in zip(xx,yy)],np.int0)
            i+=1
            P.append(pts)
        except:
            pass
        
    cv2.polylines(z, P, False, (255,255,255),1)
    cv2.imshow(name,z)