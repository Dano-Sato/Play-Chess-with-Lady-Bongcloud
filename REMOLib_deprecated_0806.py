##Pygames 모듈을 리패키징하는 REMO Library 모듈##
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame,time,math,copy,pickle,random
import sys,os
try:
    import pygame.freetype as freetype
except ImportError:
    print ("No FreeType support compiled")
    sys.exit ()

from abc import *
from enum import Enum


## Idea from Pyside2.QPoint
## includes all of the method of QPoint + additional methods
class RPoint():
    def __init__(self,x=(0,0),y=None):
        if y==None:
            self.__x=int(x[0])
            self.__y=int(x[1])
        else:
            self.__x=int(x)
            self.__y=int(y)
            
    def x(self):
        return self.__x
    def y(self):
        return self.__y
    
    def setX(self,x):
        self.__x = x
    def setY(self,x):
        self.__y = x
    
    def __add__(self,p2):
        return RPoint(self.x()+p2.x(),self.y()+p2.y())
    def __sub__(self,p2):
        return RPoint(self.x()-p2.x(),self.y()-p2.y())
    def __mul__(self,m):
        return RPoint(int(self.x()*m),int(self.y()*m))
    def __rmul__(self,m):
        return RPoint(int(self.x()*m),int(self.y()*m))
    def __truediv__(self,m):
        return RPoint(int(self.x()/m),int(self.y()/m))
    def __floordiv__(self,m):
        return self/m 
    def __eq__(self,p2):
        if type(p2) != RPoint:
            return False
        if self.x()==p2.x() and self.y()==p2.y():
            return True
        return False
    
    def toTuple(self):
        return (self.__x,self.__y)
    def transposed(self):
        return RPoint(self.y(),self.x())
            
    def __repr__(self):
        return "REMOGame.RPoint({0},{1})".format(self.x(),self.y())
    
    
    ##2차원 거리 출력
    def distance(self,p2):
        return math.dist(self.toTuple(),p2.toTuple())
    ## 포인트 p2로 speed값만큼 이동한 결과를 반환한다. 
    def moveTo(self,p2,speed):
        d = self.distance(p2)
        if d <= speed:
            result = p2
        else:
            result = self
            delta = p2-self
            delta *= (speed/d)
            result += delta
        return result



#colorSheet
class Cs():
    white=(255, 255, 255)
    grey=(128,128,128)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,255,0)
    blue=(0,0,255)
    yellow=(255,255,0)
    cyan = (0,255,255)
    orange=(255,165,0)
    purple=(160,32,240)
    pink=(255,192,203)
    beige = (245,245,220)
    brown = (150, 75, 0)
    aquamarine = (127,255,212)
    salmon = (250,128,114)
    ebony = (85,93,80)
    cognac = (154, 70, 61)
    mint = (62, 180, 137)
    lint = (186, 204, 129)
    tiffanyBlue = (10, 186, 181)
    dustyRose = (220, 174, 150)
    burgundy = (128, 0, 32)
    
    __hexCodePipeline = {}

    @classmethod
    def apply(cls,color,r):
        f = lambda x: min(255,x*r)
        return tuple([f(x) for x in color])
    @classmethod
    def dark(cls,color):
        return Cs.apply(color,0.4)
    @classmethod
    def dim(cls,color):
        return Cs.apply(color,0.8)
    @classmethod
    def light(cls,color):
        return Cs.apply(color,1.2)
    @classmethod
    def bright(cls,color):
        return Cs.apply(color,1.6)
    
    @classmethod
    def hexColor(cls,hex):
        hex = hex.upper()
        if hex in list(Cs.__hexCodePipeline):
            return Cs.__hexCodePipeline[hex]
        else:
            rgb = tuple(int(hex[i:i+2], 16)  for i in (0, 2, 4))
            Cs.__hexCodePipeline[hex]=rgb
            return rgb


class AnimationMode(Enum):
    Looped = 1
    PlayOnce = 2    

## REMO Standalone
class Rs:
    target_fps = 60
    screen_size = (800,600)
    screen = None
    __fullScreen = False # 풀스크린 여부를 체크하는 인자
    draggedObj = None # 드래깅되는 오브젝트를 추적하는 인자
    __toggleTimer = 0 # 풀스크린 토글할 때 연속토글이 일어나지 않도록 시간을 재주는 타이머.
    
    __lastState=(False,False,False)
    __justClicked = [False,False,False] # 유저가 클릭하는 행위를 했을 때의 시점을 포착하는 인자.
    __justReleased = [False,False,False]
    __lastKeyState = None # 마지막의 키 상태를 저장하는 인자.
    @classmethod
    #internal update function
    def _update(cls):
        if Rs.__toggleTimer>0:
            Rs.__toggleTimer-=1
        ###Mouse Click Event 처리
        state = pygame.mouse.get_pressed()
        for i,_ in enumerate(state):
            if i==0 and (Rs.__lastState[i],state[i])==(True,False): # Drag 해제.
                Rs.draggedObj=None
            #버튼 클릭 여부를 확인.
            if (Rs.__lastState[i],state[i])==(False,True):
               Rs.__justClicked[i]=True
            else:
               Rs.__justClicked[i]=False
            
            #버튼 릴리즈 여부를 확인
            if (Rs.__lastState[i],state[i])==(True,False):
                Rs.__justReleased[i]=True
            else:
                Rs.__justReleased[i]=False
                
        ##animation 처리
        for animation in Rs.__animationPipeline:
            if animation.isEnded():
                Rs.__animationPipeline.remove(animation)
            else:
                animation.update()
        for obj in Rs.__fadeAnimationPipeline:
            if obj["Time"]==0:
                Rs.__fadeAnimationPipeline.remove(obj)
            else:
                obj["Time"]-=1
                obj["Obj"].alpha = int(obj["Alpha"]*obj["Time"]/obj["Max"])
            
        ##change Music 처리
        if Rs.__changeMusic != None:
            if Rs.__changeMusic["Time"]<time.time():
                Rs.playMusic(Rs.__changeMusic["Name"],volume=Rs.__changeMusic["Volume"])
                Rs.__changeMusic = None

        Rs.__lastState=state
    
    @classmethod
    def _updateState(cls):
        Rs.__lastKeyState=pygame.key.get_pressed()
        
    @classmethod
    def _draw(cls):
        ##등록된 애니메이션들을 재생한다.
        for animation in Rs.__animationPipeline:
            animation.draw()
        for obj in Rs.__fadeAnimationPipeline:
            obj["Obj"].draw()

    ##FullScreen 관련 함수
    @classmethod
    def isFullScreen(cls):
        return Rs.__fullScreen

    @classmethod
    def toggleFullScreen(cls):
        Rs.__fullScreen = not Rs.isFullScreen()
        Rs.updateScreen()
    
    @classmethod
    def setFullScreen(cls,t=True):
        Rs.__fullScreen = t
        Rs.updateScreen()
    @classmethod
    def updateScreen(cls):
        if Rs.isFullScreen():
            Rs.screen = pygame.display.set_mode(Rs.screen_size,pygame.FULLSCREEN)
        else:
            Rs.screen = pygame.display.set_mode(Rs.screen_size)

        import pygame._sdl2 as sdl2

        window = sdl2.Window.from_display_module()
        window.position = sdl2.WINDOWPOS_CENTERED
        window.show()


    ##기타 함수
    @classmethod
    #Return copied graphics object
    def copy(cls,obj):
        new_obj = graphicObj()
        new_obj.pos = obj.geometryPos
        new_obj.graphic = copy.copy(obj.graphic)
        new_obj.graphic_n = copy.copy(obj.graphic_n)
        return new_obj

    #__init__을 호출하지 않고 해당 객체를 생성한다.
    #인텔리센스 사용을 위해 쓰는 신택스 슈가 함수.
    @classmethod
    def new(cls,obj):
        return obj.__new__(obj)
    
    @classmethod
    #Tuple to Point
    def Point(cls,tuple,y=None):
        if y==None:
            if type(tuple)==RPoint:
                return tuple
            else:
                return RPoint(tuple[0],tuple[1])
        else:
            return RPoint(tuple,y)


    ##음악 재생 함수

    __soundPipeline={}
    __masterSEVolume = 1
    __masterVolume = 1
    #사운드 재생. wav와 ogg파일을 지원한다. 중복재생이 가능하다.
    #loops=-1 인자를 넣을 경우 무한 반복재생.
    @classmethod
    def playSound(cls,fileName,*,loops=0,maxtime=0,fade_ms=0,volume=1):
        fileName = Rs.getPath(fileName)
        if fileName not in list(Rs.__soundPipeline):
            Rs.__soundPipeline[fileName] = pygame.mixer.Sound(fileName)         
        mixer = Rs.__soundPipeline[fileName]
        mixer.set_volume(volume*Rs.__masterSEVolume)
        mixer.play(loops,maxtime,fade_ms)
    @classmethod
    def stopSound(cls,fileName):
        fileName = Rs.getPath(fileName)
        if fileName not in list(Rs.__soundPipeline):
            return
        mixer = Rs.__soundPipeline[fileName]
        mixer.stop()        

    __currentMusic = None
    __musicVolumePipeline = {}
    __changeMusic = None
    #음악 재생. mp3, wav, ogg파일을 지원한다. 중복 스트리밍은 불가능.
    #loops=-1 인자를 넣을 경우 무한 반복재생. 0을 넣을 경우 반복 안됨
    #여기서의 volume값은 마스터값이 아니라 음원 자체의 볼륨을 조절하기 위한 것이다. 음원이 너무 시끄럽거나 할 때 값을 낮춰잡는 용도
    @classmethod
    def playMusic(cls,fileName,*,loops=-1,start=0.0,volume=1):
        pygame.mixer.music.load(Rs.getPath(fileName))
        pygame.mixer.music.set_volume(volume*Rs.__masterVolume)
        pygame.mixer.music.play(loops,start)
        Rs.__currentMusic = fileName
        Rs.__musicVolumePipeline[Rs.currentMusic()] = volume ##볼륨 세팅값을 저장

    @classmethod
    def stopMusic(cls):
        pygame.mixer.music.stop()
        
    @classmethod
    ##fadeout in time(milliseconds)
    def fadeoutMusic(cls,time=500):
        pygame.mixer.music.fadeout(time)

    ##페이드아웃을 통해 자연스럽게 음악을 전환하는 기능        
    @classmethod
    def changeMusic(cls,fileName,_time=500,volume=1):
        Rs.fadeoutMusic(_time)
        Rs.__changeMusic = {"Name":fileName,"Time":time.time()+_time/1000.0,"Volume":volume}

    @classmethod
    def currentMusic(cls):
        return Rs.__currentMusic       
    ##음악의 볼륨 값을 정한다.##
    @classmethod
    def setVolume(cls,volume):
        Rs.__masterVolume = volume
        if Rs.currentMusic() in Rs.__musicVolumePipeline:
            pygame.mixer.music.set_volume(volume*Rs.__musicVolumePipeline[Rs.currentMusic()])
        else:
            pygame.mixer.music.set_volume(volume)
    @classmethod
    def getVolume(cls):
        return Rs.__masterVolume
    @classmethod
    def setSEVolume(cls,volume):
        Rs.__masterSEVolume = volume
    @classmethod
    def getSEVolume(cls):
        return Rs.__masterSEVolume
        

    @classmethod
    def pauseMusic(cls):
        pygame.mixer.music.pause()

    @classmethod
    def unpauseMusic(cls):
        pygame.mixer.music.unpause()
    @classmethod
    def fadeoutMusic(cls,fadeout_ms=1000):
        pygame.mixer.music.fadeout(fadeout_ms)
        
    ##볼륨 슬라이더##
    @classmethod
    def musicVolumeSlider(cls,pos=RPoint(0,0),length=300,thickness=13,color=Cs.white,isVertical=False):
        slider=sliderObj(pos=pos,length=length,thickness=thickness,color=color,isVertical=isVertical,value=1)
        def volumeUpdate():
            Rs.setVolume(slider.value)
        slider.connect(volumeUpdate)
        return slider
    @classmethod
    def SEVolumeSlider(cls,pos=RPoint(0,0),length=300,thickness=13,color=Cs.white,isVertical=False):
        slider=sliderObj(pos=pos,length=length,thickness=thickness,color=color,isVertical=isVertical,value=1)
        def SEVolumeUpdate():
            Rs.setSEVolume(slider.value)
        slider.connect(SEVolumeUpdate)
        return slider

    ###기본적인 드로잉 함수 (사각형 드로잉)
    @classmethod
    #Fill Screen with Color
    def fillScreen(cls,color):
        screenRect = (0,0,Rs.screen_size[0],Rs.screen_size[1])
        Rs.fillRect(color,screenRect)

    #Fill Rectangle with color
    @classmethod
    def fillRect(cls,color,rect,*,pad=0,special_flags=0):
        Rs.screen.fill(color,Rs.padRect(rect,pad),special_flags)

    #가장자리를 pad만큼 늘린 사각형 리턴
    #Pad 음수일 경우 줄인다.
    #Pad는 숫자일 수도 있고 (3,5)와 같은 튜플일수도 있다.
    @classmethod
    def padRect(cls,rect,pad):
        if type(pad)==int:
            return pygame.Rect(rect[0]-pad,rect[1]-pad,rect[2]+2*pad,rect[3]+2*pad)
        else:
            #pad[0]->pad_width, pad[1]->pad_height
            return pygame.Rect(rect[0]-pad[0],rect[1]-pad[1],rect[2]+2*pad[0],rect[3]+2*pad[1])          

    #폰트 파이프라인(Font Pipeline)
    __fontPipeline ={}
    __sysFontName = "BMDOHYEON_ttf.ttf"
    __sysSize = 15
    _buttonFontSize = 25

    #기본 설정된 폰트를 변경
    @classmethod
    def setSysFont(cls,*,font="BMDOHYEON_ttf.ttf",size=15,buttonFontSize=25):
        Rs.__sysFontName = font
        Rs.__sysSize = size
        Rs._buttonFontSize = buttonFontSize
        return

    #기본 폰트값을 반환한다.
    @classmethod
    def getSysFont(cls):
        return (Rs.__sysFontName,Rs.__sysSize)


    #폰트 문자열을 입력하면 폰트 객체를 반환하는 함수.
    @classmethod    
    def getFont(cls, font):
        if '.ttf' in font:
            font = Rs.getPath(font)

            if font in list(Rs.__fontPipeline):
                return Rs.__fontPipeline[font]
            else:
                    try:
                        fontObj = freetype.Font(font,100)
                    except:
                        print("Font import error in:"+font)
                        fontObj = freetype.SysFont('comicsansms',0)
        else:
            try:
                fontObj = freetype.SysFont(font,100)
            except:
                print("Font import error in:"+font)
                fontObj = freetype.SysFont('comicsansms',0)
        cls.__fontPipeline[font]=fontObj
        return fontObj

    #color : Font color, font: Name of Font, size : size of font, bcolor: background color
    #Returns the boundary of text
    @classmethod
    def drawString(cls,text,pos,*,color=(0,0,0),font=None,size=None,bcolor=None,rotation=0,style=freetype.STYLE_DEFAULT):
        if font == None:
            font = Rs.__sysFontName
        if size == None:
            size = Rs.__sysSize

        '''
        if font in list(Rs.__fontPipeline):
            fontObj = Rs.__fontPipeline[font]
            return fontObj.render_to(Rs.screen, pos, text, color,bcolor,size=size,rotation=rotation,style=style)
        else:
            try:
                fontObj = freetype.SysFont(font,0)
            except:
                fontObj = freetype.SysFont('comicsansms',0)
            cls.__fontPipeline[font] = fontObj
        '''
        return Rs.getFont(font).render_to(Rs.screen, pos, text, color,bcolor,size=size,rotation=rotation,style=style)

    ###Path Pipeline###
    __pathData={}
    __pathPipeline={}
    @classmethod
    def _buildPath(cls):
        Rs.__pathData={}
        Rs.__pathPipeline={}
        import os
        #확장자명에 따른 파일분류
        for currentpath, folders, files in os.walk('.'):
            for file in files:
                if file[0]==".": # 숨김 파일은 기본적으로 제외한다.
                    continue
                path = os.path.join(currentpath, file)
                extension = path.split('.')[-1]
                if extension in list(Rs.__pathData):
                    Rs.__pathData[extension].append(path)
                else:
                    Rs.__pathData[extension]=[path]
                if file not in list(Rs.__pathPipeline):
                    Rs.__pathPipeline[file]=path
                else:
                    print("possible file conflict in",file,":",path,Rs.__pathPipeline[file])
                    
    #해당 파일의 실제 경로를 스마트하게 찾아주는 함수.
    #가령 실제 파일이 /Resources/sprites/testGirl.png 여도
    #testGirl.png만 해도 찾아내준다.
    @classmethod
    def getPath(cls,path):
        if path in list(Rs.__pathPipeline):
            return Rs.__pathPipeline[path]

        extension = path.split('.')[-1]
        if extension not in list(Rs.__pathData):
            raise Exception(path,"is not exists!")        
        if path in Rs.__pathData[extension]:
             Rs.__pathPipeline[path]=path
             return path
        else:
            for p in Rs.__pathData[extension]:
                if path in p:
                    print("path",path,"is attached to",p)
                    Rs.__pathPipeline[path]=p
                    return p
        raise Exception(path,"is not exists!")
    
    ##해당 파일이 실제로 존재하는지를 체크하는 함수
    @classmethod    
    def assetExist(cls,path):
        if path in list(Rs.__pathPipeline):
            return True
        return False
    
    __imagePipeline={}
    @classmethod
    def getImage(cls,path):
        path = Rs.getPath(path)
        if path not in Rs.__imagePipeline:
            Rs.__imagePipeline[path]=pygame.image.load(path)
        return Rs.__imagePipeline[path]
    
    #이미지 스프라이트에서 rect영역을 잘라낸 함수 
    __spritePipeline={}
    @classmethod
    def getSprite(cls,path,rect):
        key = (path,str(rect))
        if key not in Rs.__spritePipeline:
            sprite = pygame.Surface(rect.size,pygame.SRCALPHA)
            sprite.blit(Rs.getImage(path),(0,0),rect)
            Rs.__spritePipeline[key]=sprite
        return Rs.__spritePipeline[key]
    
    
    ##애니메이션 재생을 위한 함수
    ##애니메이션이 한번 재생되고 꺼진다.
    ##애니메이션은 기본적으로 화면 맨 위에서 재생된다.
    __animationPipeline=[]
    @classmethod
    def playAnimation(cls,sprite,*,rect=None,pos=RPoint(0,0),sheetMatrix=(1,1),center=None,scale=1.0,tick=1,angle=0,fromSprite=0,toSprite=None,alpha=255):
        obj = spriteObj(sprite,rect,pos=pos,tick=tick,scale=scale,angle=0,sheetMatrix=sheetMatrix,fromSprite=fromSprite,toSprite=toSprite,mode=AnimationMode.PlayOnce)
        obj.alpha = alpha
        if center!=None:
            obj.center = center
        Rs.__animationPipeline.append(obj)
        
        
    ##페이드아웃 애니메이션 재생을 위한 함수.
    __fadeAnimationPipeline=[]
    @classmethod
    def fadeAnimation(cls,obj,*,time=30,alpha=255):
        Rs.__fadeAnimationPipeline.append({"Obj":obj,"Max":time,"Time":time,"Alpha":alpha})
        
    ##스크린샷 - 현재 스크린을 캡쳐하여 저장한다.
    screenShot = None
    #스크린샷 캡쳐
    @classmethod
    def captureScreenShot(cls):        
        Rs.screenShot = pygame.Surface(Rs.screen.get_rect().size,pygame.SRCALPHA)
        Rs.screenShot.blit(Rs.screen,(0,0))
        return Rs.screenShot

    @classmethod
    def drawScreenShot(cls):
        Rs.screen.blit(Rs.screenShot,(0,0))
        
    ###User Input Functions###
    
    #Mouse Click Detector
    @classmethod
    def mousePos(cls):
        return RPoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    @classmethod
    def userJustLeftClicked(cls):
        return Rs.__justClicked[0]
    
    @classmethod
    def userJustReleasedMouseLeft(cls):
        return Rs.__justReleased[0]

    @classmethod
    def userJustReleasedMouseRight(cls):
        return Rs.__justReleased[2]

    @classmethod
    def userIsLeftClicking(cls):
        return pygame.mouse.get_pressed()[0]

    @classmethod
    def userIsRightClicking(cls):
        return pygame.mouse.get_pressed()[2]

    @classmethod
    def userJustRightClicked(cls):
        return Rs.__justClicked[2]

    #Key Push Detector
    @classmethod
    def userJustPressed(cls,key):
        if Rs.__lastKeyState == None:
            return False
        keyState = pygame.key.get_pressed()
        if (Rs.__lastKeyState[key],keyState[key])==(False,True):
            return True
        else:
            return False
    
    @classmethod
    def userPressing(cls,key):
        return pygame.key.get_pressed()[key]


    ##Draw Function##
    
    __graphicPipeline = {}
    
    def drawArrow(start, end,*,lcolor=Cs.white, tricolor=Cs.white,trirad=40, thickness=20,alpha=255):
        if type(start)==RPoint:
            start = start.toTuple()
        if type(end)==RPoint:
            end = end.toTuple()
        key = ("ArrowObj",start,end,lcolor,tricolor,trirad,thickness,alpha)
        if key in list(Rs.__graphicPipeline):
            screen = Rs.__graphicPipeline[key]
        else:
            w,h = Rs.screen.get_size()
            screen = pygame.Surface((w,h),pygame.SRCALPHA,32).convert_alpha()

            if type(start)==RPoint:
                start = start.toTuple()
            if type(end)==RPoint:
                end = end.toTuple()
            rad = math.pi/180.0
            pygame.draw.line(screen, lcolor, start, end, thickness)
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi/2
            pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                                end[1] + trirad * math.cos(rotation)),
                                            (end[0] + trirad * math.sin(rotation - 120*rad),
                                                end[1] + trirad * math.cos(rotation - 120*rad)),
                                            (end[0] + trirad * math.sin(rotation + 120*rad),
                                                end[1] + trirad * math.cos(rotation + 120*rad))))    

            screen.set_alpha(alpha)
            if len(Rs.__graphicPipeline)>1000:
                Rs.__graphicPipeline={}
            Rs.__graphicPipeline[key]=screen
        Rs.screen.blit(screen,(0,0))
        
    def drawLine(color,point1,point2,*,width=1):
        pygame.draw.line(Rs.screen,color,Rs.Point(point1).toTuple(),Rs.Point(point2).toTuple(),width)
        
        
    ##단순히 모듈 통일을 위해 만든 쇼트컷 함수...
    ##현재 신을 교체해준다.
    @classmethod
    def setCurrentScene(cls,scene,skipInit=False):
        REMOGame.setCurrentScene(scene,skipInit)

    ##디스플레이 아이콘을 바꾼다.
    @classmethod
    def setIcon(cls,img):
        img = Rs.getImage(img)
        pygame.display.set_icon(img)

        
        
    ##File Input/Output
    
    @classmethod
    def saveData(self,path,data):
        if os.path.isfile(path):
            control = 'wb'
        else:
            control = 'xb'
        pickle.dump(data,open(path,control))
        



class Scene(ABC):

    def __init__(self):
        self.initiated=False
        return
    def _init(self):
        if self.initiated==False:
            self.initOnce()
            self.initiated = True
        self.init()
        
    #Scene을 불러올 때마다 initiation 되는 메소드 부분 
    def init(self):
        return
    
    #Scene을 처음 불러올때만 initiation 되는 메소드
    def initOnce(self):
        return

    def update(self):
        #update childs
        #if child has update method, it updates child
        return
    def draw(self):
        #draw childs
        return

## Base Game class
class REMOGame:
    currentScene = Scene()

    __lastStartedWindow = None
    def __init__(self,screen_size=(1920,1080),fullscreen=True,*,caption="REMOGame window"):
        Rs._buildPath() ## 경로 파이프라인을 구성한다.
        pygame.init()
        Rs.__fullScreen=fullscreen
        Rs.screen_size = screen_size
        Rs.updateScreen()
        pygame.display.set_caption(caption)
        REMOGame.__lastStartedWindow = self
        # Fill the background with white
        Rs.screen.fill(Cs.white)


    def setWindowTitle(self,title):
        pygame.display.set_caption(title)
        
    #게임이 시작했는지 여부를 확인하는 함수
    @classmethod 
    def gameStarted(cls):
        return REMOGame.__lastStartedWindow != None        
    #classmethod로 기획된 이유는 임의의 상황에서 편하게 호출하기 위해서이다.
    # initiation 과정을 스킵할 수 있음
    @classmethod
    def setCurrentScene(cls,scene,skipInit=False):
        REMOGame.currentScene = scene
        if not skipInit:
            REMOGame.currentScene._init()

    def update(self):
        REMOGame.currentScene.update()
        return

    def draw(self):
        REMOGame.currentScene.draw()
        Rs._draw()
        return
    
    @classmethod
    def exit(cls):
        REMOGame.__lastStartedWindow.running = False
        #pygame.quit()

    #Game Running Method
    def run(self):
        self.running = True
        prev_time = time.time()
        while self.running:
            Rs._update()
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    REMOGame.exit()
            self.update()
            Rs.fillScreen(Cs.white)
            self.draw()
            self.paint()
            Rs._updateState()
            ##Timing code, set frame to target_fps(60fps)
            curr_time = time.time()#so now we have time after processing
            diff = curr_time - prev_time#frame took this much time to process and render
            delay = max(1.0/Rs.target_fps - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
            time.sleep(delay)
            fps = 1.0/(delay + diff)#fps is based on total time ("processing" diff time + "wasted" delay time)
            prev_time = curr_time
            #pygame.display.set_caption("{0}: {1:.2f}".format(title, fps))

    def paint(self):
        pygame.display.update()

### Graphic Objects ###

#abstract class for graphic Object
class graphicObj():
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,pos):
        self._pos = Rs.Point(pos)
        
    def moveTo(self,p2,speed):
        self.pos = self.pos.moveTo(p2,speed)

    @property
    def center(self):
        return RPoint(self.pos.x()+self.rect.w//2,self.pos.y()+self.rect.h//2)
    @center.setter
    def center(self,_center):
        if type(_center)==tuple:
            _center = RPoint(_center[0],_center[1])
        self.pos = RPoint(_center.x()-self.rect.w//2,_center.y()-self.rect.h//2)

    ##Rect is combination of (pos,size)
    ##pos : position of the object, size : size of the object
    @property
    def rect(self):
        return pygame.Rect(self.pos.x(),self.pos.y(),self.graphic.get_rect().w,self.graphic.get_rect().h)

    #could be replaced
    @rect.setter
    def rect(self,rect):
        self.graphic = pygame.transform.smoothscale(self.graphic_n,(rect[2],rect[3]))
        self._pos = RPoint(rect[0],rect[1])

    #geometry란 object가 실제로 screen상에서 차지하는 영역을 의미합니다.
    #getter only입니다.
    @property
    def geometry(self):
        if self.parent:
            return pygame.Rect(self.parent.geometry.x+self.pos.x(),self.parent.geometry.y+self.pos.y(),self.rect.width,self.rect.height)
        return self.rect
    
    #object의 실제 스크린 상의 위치 
    @property
    def geometryPos(self):
        if self.parent:
            return RPoint(self.parent.geometry.x+self.pos.x(),self.parent.geometry.y+self.pos.y())
        return self.pos
    
    #object의 스크린상에서의 실제 중심 위치
    @property
    def geometryCenter(self):
        if self.parent:
            return self.geometryPos+RPoint(self.rect.w,self.rect.h)*0.5
        return self.center
        
    
    def __init__(self):
        self.graphic = pygame.Surface((0,0))
        self.graphic_n = pygame.Surface((0,0))
        self._pos = RPoint(0,0)
        self.childs = []
        self.parent = None
        self.alpha = 255
        return
    
    #Parent - Child 연결관계를 만듭니다.
    def setParent(self,_parent):
        if self.parent !=None:
            self.parent.childs.remove(self)
        self.parent = _parent
        if _parent != None:
            _parent.childs.append(self)
            if hasattr(_parent,'adjustLayout'):
                _parent.adjustLayout()


    #Could be replaced
    def draw(self):
        alpha_graphic = self.graphic.convert_alpha()
        alpha_graphic.set_alpha(self.alpha)
        Rs.screen.blit(alpha_graphic,self.geometry)
        for child in self.childs:
            child.draw()

    #Fill object with Color
    def fill(self,color,*,special_flags=pygame.BLEND_MAX):
        self.graphic_n.fill(color,special_flags=special_flags)
        self.graphic.fill(color,special_flags=special_flags)
        
    def colorize(self,color,alpha=255):
        self.fill((0,0,0,alpha),special_flags=pygame.BLEND_RGBA_MULT)
        self.fill(color[0:3]+(0,),special_flags=pygame.BLEND_RGBA_ADD)
        
    def collidepoint(self,p):
        return self.geometry.collidepoint(Rs.Point(p).toTuple())
    def collideMouse(self):
        return self.collidepoint(Rs.mousePos())
    def isJustClicked(self):
        return Rs.userJustLeftClicked() and self.collidepoint(Rs.mousePos())
    
#image file Object         
class imageObj(graphicObj):
    def __init__(self,_imgPath=None,_rect=None,*,pos=None,angle=0,scale=1):
        super().__init__()
        if _imgPath:
            self.graphic = Rs.getImage(_imgPath)
            self.graphic_n = Rs.getImage(_imgPath)
        if _rect:
            self.rect = _rect
        
        if pos:
            self.pos = Rs.Point(pos)
        self._angle = 0
        self._scale = 1
        self.angle = angle
        self.scale = scale
        if _rect:
            self.rect = _rect

    #angle = 이미지의 각도 인자
    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self,angle):
        #originalRect = self.graphic_n.get_rect()
        #self.graphic = pygame.transform.smoothscale(self.graphic_n,(int(originalRect.w*self.scale),int(originalRect.h*self.scale)))
        self._angle = int(angle)    
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)
    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self,scale):
        #originalRect = self.graphic_n.get_rect()
        #self.graphic = pygame.transform.smoothscale(self.graphic_n,(int(originalRect.w*scale),int(originalRect.h*scale)))
        self._scale = scale
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)

    ##이미지 교환 함수     
    def setImage(self,path):
        self.graphic = Rs.getImage(path)
        self.graphic_n = Rs.getImage(path)
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)
        
        
        
    
            
##Rectangle Object. could be rounded
class rectObj(graphicObj):
    def _makeRect(self,rect,color,edge,radius):
        self.graphic = pygame.Surface((rect.w,rect.h),pygame.SRCALPHA,32).convert_alpha()
        pygame.draw.rect(self.graphic,Cs.apply(color,0.7),pygame.Rect(0,0,rect.w,rect.h),border_radius=radius+1)
        pygame.draw.rect(self.graphic,Cs.apply(color,0.85),pygame.Rect(edge,edge,rect.w-2*edge,rect.h-2*edge),border_radius=radius+2)

        pygame.draw.rect(self.graphic,color,pygame.Rect(2*edge,2*edge,rect.w-4*edge,rect.h-4*edge),border_radius=radius)
        self.graphic_n = copy.copy(self.graphic)
        
    def __init__(self,rect,*,radius=None,pad=0,edge=0,color=Cs.white,alpha=255):
        super().__init__()
        if radius==None:
            radius = int(min(rect.w,rect.h)*0.2)

        temp = Rs.padRect(rect,pad)
        self._makeRect(temp,color,edge,radius)
        #self.graphic.set_colorkey((0,0,0))
        self.alpha=alpha
        self.pos = RPoint(rect.x,rect.y)-RPoint(pad,pad)
        self._color = color
        self._radius = radius
        self._edge = edge

    @property
    def edge(self):
        return self._edge

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self,radius):
        temp = copy.copy(self.rect)
        self._radius = radius
        self._makeRect(temp,self.color,self.edge,radius)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self,color):
        temp = copy.copy(self.rect)
        self._color = color
        self._makeRect(temp,color,self.edge,self.radius)


class textObj(graphicObj):
    def __init__(self,text="",pos=(0,0),*,font=None,size=None,color=Cs.white,angle=0):
        super().__init__()
        if font==None:
            font = Rs.getSysFont()[0]
        if size==None:
            size = Rs.getSysFont()[1]
        self.graphic = Rs.getFont(font).render(text,color,None,size=size,rotation=angle)[0].convert_alpha()
        self.graphic_n = Rs.getFont(font).render(text,color,None,size=size,rotation=angle)[0].convert_alpha()
        self._rect = self.graphic.get_rect()
        self.__color = color
        self.__size = size
        self.__angle = angle
        self.__font = font
        self.__text = text
        self.pos = Rs.Point(pos)
    @property
    def color(self):
        return self.__color

    #컬러값을 변경할 때는 영역이 바뀌지 않는다.
    @color.setter
    def color(self,_color):
        temp = copy.copy(self.rect)
        self.__color = _color
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.rect = copy.copy(temp)
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self,_size):
        self.__size = _size
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
    @property
    def angle(self):
        return self.__angle
    @angle.setter
    def angle(self,_angle):
        self.__angle = _angle
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
    @property
    def font(self):
        return self.__font
    @font.setter
    def font(self,_font):
        self.__font = _font
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self,_text):
        self.__text = _text
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        


#수정할 예정
#이미지의 List를 인자로 받는 스프라이트 클래스.
#(애니메이션)움직이게 할 수 있다.
class spriteObj(imageObj):
    #sheetMatrix : sprite sheet의 행렬값. 예를 들어 3*5(3행5열) 스프라이트 시트일 경우 (3,5) 입력
    def __init__(self,_imageSource=None,_rect=None,*,pos=RPoint(0,0),sheetMatrix=(1,1),startFrame=None,tick=1,angle=0,scale=1,fromSprite=0,toSprite=None,mode=AnimationMode.Looped):
        super(imageObj,self).__init__()
        self.tick = tick # 스프라이트 교환주기. 1프레임마다 다음프레임으로 교체
        self.curTick = 0 # 스프라이트의 현재 틱
        if startFrame==None:
            self.frame = fromSprite # 스프라이트 현재 프레임. 시작 프레임에서부터 시작한다.
        else:
            self.frame = startFrame
        self.mode = mode # 기본 애니메이션 모드 세팅은 루프를 하도록.
        self.sprites = [] #스프라이트들의 집합
        if _imageSource:
            if type(_imageSource) == str: #SpriteSheet를 인자로 받을 경우
                sheet = Rs.getImage(_imageSource)
                spriteSize = (sheet.get_rect().w//sheetMatrix[1],sheet.get_rect().h//sheetMatrix[0])
                for y in range(sheetMatrix[0]):
                    for x in range(sheetMatrix[1]):
                        t_rect = pygame.Rect(x*spriteSize[0],y*spriteSize[1],spriteSize[0],spriteSize[1])
                        self.sprites.append(Rs.getSprite(_imageSource,t_rect))
            else:
                for image in _imageSource:
                    self.sprites.append(Rs.getImage(image))
        self.graphic_n = self.sprites[self.frame]
        '''
        if _rect:
            self.rect = _rect
            if _images:
                for i,_ in enumerate(self.img):
                    self.img[i] = pygame.transform.scale(self.img[i],(self.rect.w,self.rect.h))
                    self._img_n[i] = pygame.transform.scale(self._img_n[i],(self.rect.w,self.rect.h))
        '''

        self._angle = 0
        self._scale = 1 
        self.angle = angle
        self.scale = scale
        self.pos = pos
        self.fromSprite = fromSprite
        if toSprite != None:
            self.toSprite = toSprite
        else:
            self.toSprite = len(self.sprites)-1
        if _rect!=None:
            self.rect = _rect        

    ##스프라이트 재생이 끝났는지 확인한다.
    #루프모드일 경우 항상 거짓 반환
    def isEnded(self):
        if self.mode == AnimationMode.PlayOnce and self.frame == self.toSprite:
            return True
        return False

    #스프라이트를 교체한다.
    def update(self):
        max = self.toSprite
            
        if self.curTick < self.tick-1:
            self.curTick+=1
        else:
            self.curTick=0
            if self.mode == AnimationMode.Looped:
                self.frame+=1
                if self.frame > max:
                    self.frame=self.fromSprite
            else:
                if self.frame == max:
                    return
                else:
                    self.frame+=1
        self.graphic_n = self.sprites[self.frame]
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)

#spacing : 오브젝트간 간격
#pad : layout.pos와 첫 오브젝트간의 간격
class layoutObj(graphicObj):
    def __init__(self,rect=pygame.Rect(0,0,0,0),*,pos=None,spacing=10,pad=RPoint(0,0),style=None,
                 childs=[],isVertical=True):
        super().__init__()
        self.spacing = spacing
        self.pad = pad

        self.graphic = pygame.Surface((rect.w,rect.h)) # 빈 Surface
        self.graphic_n = pygame.Surface((rect.w,rect.h))
        if pos==None:
            self.pos = RPoint(rect.x,rect.y)
        else:
            if type(pos)!=RPoint:
                self.pos = RPoint(pos[0],pos[1])
            else:
                self.pos = pos
        temp = pad
        self.isVertical = isVertical
        if self.isVertical:
            def delta(c):
                return RPoint(0,c.rect.h+spacing)
        else:
            def delta(c):
                return RPoint(c.rect.w+spacing,0)
            
        for child in childs:
            child.setParent(self)
            
        self.update()
        
        ##rect 지정이 안 되어 있을경우 자동으로 경계로 조정한다.
        if rect==pygame.Rect(0,0,0,0):
            rect = self.boundary
        
    @property
    def boundary(self):
        width,height=self.pad.x(),self.pad.y()
        if self.isVertical:
            for child in self.childs:
                height+=child.rect.h
                if child != self.childs[-1]:
                    height+=self.spacing
                width=max(width,self.pad.x()+child.rect.w)
        return pygame.Rect(self.pos.x(),self.pos.y(),width,height)

    #레이아웃 내부 객체들의 위치를 조정한다.
    def adjustLayout(self):
        lastChild = None
        for child in self.childs:
            if self.isVertical:
                def delta(c):
                    return RPoint(0,c.rect.h+self.spacing)
            else:
                def delta(c):
                    return RPoint(c.rect.w+self.spacing,0)

            if lastChild != None:
                child.pos = lastChild.pos+delta(lastChild)
            else:
                child.pos = self.pad
            lastChild = child
            

    def update(self):
        for child in self.childs:
            # child가 update function이 있을 경우 실행한다.
            if hasattr(child, 'update') and callable(getattr(child, 'update')):
                child.update()
                
    def __getitem__(self, key):
        return self.childs[key]
    
    def __setitem__(self, key, value):
        self.childs[key] = value
        self.childs[key].parent = self
        self.adjustLayout()

         
#긴 텍스트를 처리하기 위한 오브젝트.
class longTextObj(layoutObj):
    @classmethod
    def _cutString(cls,font,size,str,textWidth):
        
        
        index_whitespaces = [i for i,j in enumerate(str) if j==" "] # 띄어쓰기 위치를 모두 찾아낸다.
        index_whitespaces+=[len(str)]
        if len(index_whitespaces)<=1:
            return [str]
        #0~index까지 string을 font로 렌더링했을 때의 width를 반환
        def getWidth(index):
            return font.get_rect(str[:index_whitespaces[index]],size=size).w

        #이진 서치를 통해 최적의 Width를 찾아냄. (closest Width to the TextWidth)
        low, high = 0, len(index_whitespaces)-1
        cutPoint = high-1
        while low <= high:
            mid = (low+high)//2
            stringWidth = getWidth(mid)
            if stringWidth >= textWidth:
                high = mid-1
            else:
                low = mid+1
            
            if abs(textWidth-stringWidth) < abs(textWidth-getWidth(cutPoint)):
                cutPoint = mid
        result = [str[:index_whitespaces[cutPoint]]]
        result.extend(longTextObj._cutString(font,size,str[index_whitespaces[cutPoint]+1:],textWidth))
        return result

    def __init__(self,text="",pos=RPoint(0,0),*,font=None,size=None,color=Cs.white,textWidth=100,alpha=255):
        if font==None:
            font = Rs.getSysFont()[0]
        if size==None:
            size = Rs.getSysFont()[1]
        self.alpha = alpha 
        self._updateTextObj(pos,text,font,size,color,textWidth)
        self._text = text
        self._font=font
        self._color=color
        self._size = size
        self._textWidth = textWidth
        # cut string into string list, chopped with textWidth
        ##Test##

    def _update(self):
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)

    def _updateTextObj(self,pos,text, font, size, color,textWidth):    
        stringParts = longTextObj._cutString(Rs.getFont(font),size,text,textWidth)
        if stringParts[-1]=="":
            stringParts =stringParts[:-1]
        ObjList = []
        for str in stringParts:
            t = textObj(str,font=font,size=size,color=color)
            t.alpha = self.alpha
            ObjList.append(t)
        if type(pos) == tuple:
            pos = RPoint(pos[0],pos[1])
        super().__init__(pygame.Rect(pos.x(),pos.y(),0,0),childs=ObjList,spacing=size/4)

    #현재 textWidth에 의해 나눠질 text 집합을 불러온다.
    def getStringList(self,text):
        return longTextObj._cutString(Rs.getFont(self.font),self.size,text,self.textWidth)
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self,size):
        self._size = size
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)                    

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,color):
        self._color = color
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)                    
    @property
    def font(self):
        return self._font
    @font.setter
    def font(self,font):
        self._font = font
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)                    
    @property
    def textWidth(self):
        return self._textWidth
    @textWidth.setter
    def textWidth(self,textWidth):
        self._textWidth = textWidth
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)                    
 
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self,txt):
        self._text = txt
        self._updateTextObj(self.pos,self.text,self.font,self.size,self.color,self.textWidth)                    
            
        #text childs를 생성한다.


##이미지를 버튼으로 활용하는 오브젝트
class imageButton(imageObj):
    def __init__(self,_imgPath=None,_rect=None,*,pos=None,angle=0,scale=1,func=lambda:None,hoverMode=True,enableShadow=True):
        super().__init__(_imgPath,_rect,pos=pos,angle=angle,scale=scale)
        self.hoverObj = Rs.copy(self)
        self.hoverObj.colorize(Cs.white,alpha=60)
        self.hoverMode = hoverMode
        self.func = func
        
        if enableShadow:
            self.shadow = Rs.copy(self)
            self.shadow.colorize(Cs.black,alpha=30)
            print(self.shadow)
        else:
            self.shadow = None
    
    def update(self):
        if Rs.userJustLeftClicked() and self.collideMouse() and self.hoverMode:
            self.func()
        self.hoverObj.center = self.geometry.center
        if self.shadow != None:
            self.shadow.center = Rs.Point(self.geometry.center)+RPoint(0,5)
        
    def draw(self):
        if self.shadow:
            self.shadow.draw()
        super().draw()
        if self.hoverMode and self.collideMouse() and not Rs.userIsLeftClicking():
            self.hoverObj.draw()

    #버튼을 누르면 실행될 함수를 등록한다.
    def connect(self,func):
        self.func = func
          
            

#hoverMode : 마우스 호버링 시 밝게 빛나는 모드.
class textButton(rectObj):
    hoverAlpha = 30 ## hoverRect의 알파값.
    
    def __init__(self,text="",rect=pygame.Rect(0,0,0,0),*,edge=1,font="BMDOHYEON_ttf.ttf",size=None,color=Cs.tiffanyBlue,func=lambda:None,hoverMode=True,fontColor=Cs.white,alpha=200):
        if size==None:
            size = Rs._buttonFontSize
        self.textObj = textObj(text,RPoint(0,0),font=font,size=size,color=fontColor)
        rect.w = max(self.textObj.rect.w+20,rect.w)
        rect.h = max(self.textObj.rect.h+20,rect.h)
        super().__init__(rect,color=color,edge=edge)
        self.hoverRect = rectObj(rect,color=Cs.white)
        self.hoverRect.alpha = textButton.hoverAlpha
        self.hoverMode = hoverMode

        self.shadow1 = rectObj(rect,color=Cs.black)
        self.shadow1.alpha = 30
        self.shadow = imageObj('rectShadow.png')
        self.shadow.alpha = 100
        self.shadow.rect = Rs.padRect(self.rect,20)
        self.func = func #clicked function
        self.alpha = alpha
        self.update()
    @property
    def text(self):
        return self.textObj.text
    @text.setter
    def text(self,text):
        self.textObj.text = text
        self.update()
        
    @property
    def fontColor(self):
        return self.textObj.color

    @fontColor.setter
    def fontColor(self,color):
        self.textObj.color = color

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,color):
        temp = copy.copy(self.rect)
        self._color = color
        self._makeRect(temp,color,self.edge,self.radius)
        self.hoverRect = rectObj(self.rect,color=Cs.white)
        self.hoverRect.alpha = textButton.hoverAlpha


    def update(self):
        if Rs.userJustLeftClicked() and self.collideMouse() and self.hoverMode:
            self.func()
        self.hoverRect.center = self.geometry.center
        self.textObj.center = self.geometry.center
        self.shadow1.center = Rs.Point(self.geometry.center)+RPoint(3,3)
        self.shadow.center = Rs.Point(self.geometry.center)+RPoint(0,10)
    def setAlpha(self,alpha):
        alpha = max(alpha,0)
        alpha = min(alpha,255)
        self.alpha = alpha
        self.textObj.alpha = alpha
        self.shadow.alpha = alpha
        self.shadow1.alpha = alpha
        self.hoverRect.alpha = min(alpha,30)
    def draw(self):
        self.shadow.draw()
        self.shadow1.draw()
        super().draw()
        if self.hoverMode and self.collideMouse() and not Rs.userIsLeftClicking():
            self.hoverRect.draw()
        self.textObj.draw()
    #버튼을 누르면 실행될 함수를 등록한다.
    def connect(self,func):
        self.func = func
    
    def setParent(self,parent):
        super().setParent(parent)
        self.update()
        

##TODO: 실제로 대사를 한 글자씩 출력하기 위한 오브젝트.        
class ScriptObj(longTextObj):
    def __init__(self,text="",pos=RPoint(0,0),*,font=None,size=None,color=Cs.white,textWidth=100,alpha=255, bgExist=False, bgColor = Cs.black, liveTimer=None):
        super().__init__(text,pos=pos,font=font,size=size,color=color,textWidth=textWidth,alpha=alpha)
        self.fullBoundary = copy.copy(self.boundary) ## 텍스트가 전부 출력되었을 경우의 경계를 저장.
        self.fullSentence = self.text #전체 텍스트를 저장.
        self.text = ""
        self.liveTimer = liveTimer ## 말풍선 효과를 낼 경우, 해당 오브젝트가 살아있는 시간을 의미
        
        if bgExist:
            self.bg = textButton("",Rs.padRect(self.fullBoundary,20),color=bgColor,hoverMode=False)
        else:
            self.bg = None
        
    ##update 함수를 대체하는 함수.
    def updateText(self):
        if self.liveTimer!=None and self.liveTimer>0:
            super().update()
            i = len(self.text)
            temp = False
            if i < len(self.fullSentence):
                while i < len(self.fullSentence) and self.fullSentence[i]!=" ":
                    i+=1
                parsedText = self.fullSentence[:i]
                l1 = self.getStringList(self.text)[:-1]
                l2 = self.getStringList(parsedText)[:-1]
                try:
                    while len(l1[-1]) > len(l2[-1]):
                        self.text = self.fullSentence[:len(self.text)+1]
                        l1 = self.getStringList(self.text)[:-1]
                        temp = True
                except:
                    pass
                if not temp:
                    self.text = self.fullSentence[:len(self.text)+1]
            else:
                if self.liveTimer != None and self.liveTimer>0:
                    self.liveTimer -=1
            
            if self.liveTimer != None and self.liveTimer<25:
                self.alpha = int(self.liveTimer*8)
                if self.bg:
                    self.bg.alpha = int(self.liveTimer*8)
                self._update()
            
            if self.bg:
                self.bg.pos = self.geometryPos-RPoint(20,20)

    def draw(self):
        if self.liveTimer!=None and self.liveTimer>0:
            if self.bg:
                self.bg.draw()
            super().draw()            
        
    
        
    


# x*y의 grid 형태를 가진 타일링 오브젝트.
# pad : 타일 사이의 간격을 의미함.
class gridObj(layoutObj):
    def __init__(self,pos=RPoint(0,0),tileSize=(0,0),grid=(0,0),*,radius=5 ,spacing=(0,0),color=Cs.white):
        #super().__init__()
        temp = []
        for i in range(grid[1]):
            rowObj = layoutObj(rect=pygame.Rect(0,0,0,tileSize[1]),spacing=spacing[0],isVertical=False)
            for j in range(grid[0]):
                tileObj = rectObj(pygame.Rect(0,0,tileSize[0],tileSize[1]),radius=radius,color=color)
                tileObj.setParent(rowObj)
            temp.append(rowObj)
        super().__init__(rect=pygame.Rect(pos.x(),pos.y(),0,0),spacing=spacing[1],childs=temp)
        self.grid = grid
        self.tileSize = tileSize

    #현재 마우스가 그리드 (x,y)에 위치함을 나타내는 함수    
    def getMouseIndex(self):
        result = (-1,-1) # 충돌하지 않음을 의미하는 값
        for i in range(self.grid[1]):
            for j in range(self.grid[0]):
                if self[i][j].collideMouse():
                    result = (j,i)
        return result
                


##스크롤바 혹은 슬라이더 바

class sliderObj(rectObj):
    def __init__(self,pos=RPoint(0,0),length=50,*,thickness=10,color=Cs.white,isVertical=True,value=0.0,function = lambda:None):
        pos=Rs.Point(pos)
        if isVertical:
            rect = pygame.Rect(pos.x(),pos.y(),thickness,length)
        else:
            rect = pygame.Rect(pos.x(),pos.y(),length,thickness)

        super().__init__(rect,color=Cs.dark(color)) ## BUG


        self.gauge = rectObj(rect,color=color)
        self.gauge.setParent(self)        
        self.button = rectObj(pygame.Rect(0,0,thickness*2,thickness*2),color=color)
        self.button.setParent(self)

        self.isVertical = isVertical
        self.thickness = thickness
        self.length = length
        
        self.value = value
        self.__function = function
        
        self.adjustObj()
        
    def connect(self,func):
        self.__function = func
    def adjustObj(self):
        l = int(self.length*self.value)
        if self.isVertical:
            self.button.center = RPoint(self.thickness//2,l)
            self.gauge.rect = pygame.Rect(0,0,self.thickness,l)
        else:
            self.button.center = RPoint(l,self.thickness//2)
            self.gauge.rect = pygame.Rect(0,0,l,self.thickness)
        self.__function()

    def update(self):
        if Rs.userJustLeftClicked() and (self.collideMouse() or self.button.collideMouse()):
            Rs.draggedObj = self
        if Rs.userIsLeftClicking() and Rs.draggedObj == self:
            if self.isVertical:
                d = Rs.mousePos().y()-self.geometryPos.y()
            else:
                d = Rs.mousePos().x()-self.geometryPos.x()
            d /= float(self.length)
            d = max(0,d)
            d = min(1,d)
            self.value = d
            ##TODO: Value 조정
        self.adjustObj()
        None
        
        
##버튼들을 간편하게 생성할 수 있는 버튼용 레이아웃
##example: buttonLayout(["Play Game","Config","Exit"],RPoint(50,50))
class buttonLayout(layoutObj):
    def __init__(self,buttonNames=[],pos=RPoint(0,0),*,spacing=10,
                 isVertical=True,buttonSize=RPoint(200,50),buttonColor = Cs.tiffanyBlue,
                 fontSize=None,fontColor=Cs.white,font="BMDOHYEON_ttf.ttf",
                 buttonAlpha=200):
        self.buttons = {}
        buttonSize = Rs.Point(buttonSize)
        buttonRect = pygame.Rect(0,0,buttonSize.x(),buttonSize.y())
        for name in buttonNames:
            self.buttons[name]=textButton(name,buttonRect,font=font,size=fontSize,color=buttonColor,fontColor=fontColor,alpha=buttonAlpha)            
        super().__init__(pos=pos,spacing=spacing,isVertical=isVertical,childs=list(self.buttons.values()))
    def __getitem__(self,key):
        return self.buttons[key]
    def __setitem__(self, key, value):
        if key in self.buttons:
            self.buttons[key].setParent(None)
        self.buttons[key]=value
        self.buttons[key].setParent(self)
        self.adjustLayout()
        
                
