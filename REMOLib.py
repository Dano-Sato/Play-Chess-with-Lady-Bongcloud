###REMO Engine 
#Pygames 모듈을 리패키징하는 REMO Library 모듈
#2D Assets Game을 위한 생산성 높은 게임 엔진을 목표로 한다.
##version 0.2.3 (24-08-23 20:46 Update)
#업데이트 내용
#playVoice 함수 추가
#소소한 디버깅과 주석 수정(08-15 21:01)
#dialogObj의 추가 및 기타 엔진 개선(08-16 00:00)
#copyImage 함수 추가(08-17 10:25)
#Rs.padRect 함수 제거(pygame.Rect.inflate 함수를 사용하면 됨) (08-20 13:37)
#근본적인 버그를 발생시키는 불쾌한 Threading 관련 함수 제거 (08-20 13:59)
#딱히 근본 원인이 아니라서 Threading 함수 원복 (08-20 17:33)
#RTimer 클래스 추가, spriteObj의 애니메이션 기능 RTimer에 연동(버그 픽스) (08-20 23:48)
#Type Hint 추가, buttonLayout 객체의 버튼을 속성처럼 접근 가능. RPoint.x,y 프로퍼티화 (08-21 05:35)
#scriptRenderer 클래스의 타이머 또한 RTimer를 사용. 점프 관련 미세 변경 (08-21 06:22)
#장면 전환(transition) 기능 추가 (08-21 16:49)
#child에 depth를 추가하여 그리는 순서를 조절할 수 있게 함 (08-21 17:24)
#spriteObj를 rect 기준, 혹은 scale,angle 기준으로 조정할 수 있게 함 (08-21 23:32)
#colorize 함수를 imageObj에 귀속(textObj, rectObj는 오작동 요소가 더 많고, color 프로퍼티가 별도로 존재.) (08-21 23:58)
#defaultFont 옵션을 지정할 수 있게 됐다.(08-22 12:05)
#graphicObj 객체를 뷰포트로 지정할 수 있게 됐다. (08-22 12:20)
#scrollLayout 객체를 리팩토링 완료. 사용할 수 있는 수준이 됐다. (08-22 13:39)
#safeInt 객체를 추가. (08-22 11:17)
#imageObj에서 스프라이트 시트를 통해 이미지를 불러올 수 있게 됐다. (08-23 17:39)
#imageObj를 lock 또는 unlock할 수 있게 됐다. (08-23 19:28)
#size 인자 추가 (08-23 20:46)
###

from __future__ import annotations


from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()


import pygame,time,math,copy,pickle,random,pandas
import sys,os
try:
    import pygame.freetype as freetype
except ImportError:
    print ("No FreeType support compiled")
    sys.exit ()

from abc import *
from enum import Enum
import typing


## Idea from Pyside2.QPoint
## includes all of the method of QPoint + additional methods
## 2-Dimensional (x,y) Point
class RPoint():
    '''
    2차원 좌표를 나타내는 클래스\n
    x,y : 좌표값\n
    toTuple() : 튜플로 변환\n
    '''
    def __init__(self,x=(0,0),y=None):
        if y==None:
            self.__x=int(x[0])
            self.__y=int(x[1])
        else:
            self.__x=int(x)
            self.__y=int(y)

    @property            
    def x(self) -> int:
        return self.__x
    @property
    def y(self) -> int:
        return self.__y

    @x.setter    
    def x(self,x:int):
        self.__x = x
    @y.setter
    def y(self,x:int):
        self.__y = x
    
    def __add__(self,p2):
        return RPoint(self.x+p2.x,self.y+p2.y)
    def __sub__(self,p2):
        return RPoint(self.x-p2.x,self.y-p2.y)
    def __mul__(self,m):
        return RPoint(int(self.x*m),int(self.y*m))
    def __rmul__(self,m):
        return RPoint(int(self.x*m),int(self.y*m))
    def __truediv__(self,m):
        return RPoint(int(self.x/m),int(self.y/m))
    def __floordiv__(self,m):
        return self/m 
    def __eq__(self,p2):
        if type(p2) != RPoint:
            return False
        if self.x==p2.x and self.y==p2.y:
            return True
        return False
    
    def toTuple(self) -> typing.Tuple[int,int]:
        return (self.__x,self.__y)
    def transposed(self):
        return RPoint(self.y,self.x)
            
    def __repr__(self):
        return "REMOGame.RPoint({0},{1})".format(self.x,self.y)
    
    
    ##2차원 거리 출력
    def distance(self,p2) -> float:
        return math.dist(self.toTuple(),p2.toTuple())
    ## 포인트 p2로 speed값만큼 이동한 결과를 반환한다. 
    def moveTo(self,p2,speed=None):
        d = self.distance(p2)
        if speed==None: #스피드를 정하지 않을경우, 자연스러운 속도로 정해진다
            speed=max(d/5,2)
        if d <= speed:
            return p2 ##도달
        else:
            result = self
            delta = p2-self
            delta *= (speed/d)
            result += delta
        return result



class RTimer:
    '''
    타이머 클래스\n
    정해진 시간이 지나면 True를 반환한다.\n
    '''
    def __init__(self, duration, startNow=True):
        """
        :param duration: 타이머의 기간(밀리초 단위)
        :param start_now: 즉시 타이머를 시작할지 여부
        """
        self.duration = duration
        self.startTime = pygame.time.get_ticks() if startNow else None

    def start(self, duration=None):
        """타이머를 시작합니다."""
        if duration:
            self.duration = duration
        self.startTime = pygame.time.get_ticks()

    def reset(self):
        """타이머를 리셋하고 다시 시작합니다."""
        self.start()

    def stop(self):
        """타이머를 중지합니다."""
        self.startTime = None

    def isOver(self):
        """타이머가 완료되었는지 확인합니다."""
        if self.startTime is None:
            return False
        return pygame.time.get_ticks() - self.startTime >= self.duration
    
    def isRunning(self):
        '''타이머가 활성화되어 있는지 확인합니다.'''
        if self.startTime is None:
            return False
        return True

    def timeLeft(self):
        """남은 시간을 반환합니다. (밀리초 단위)"""
        if self.startTime is None:
            return self.duration
        elapsed = pygame.time.get_ticks() - self.startTime
        return max(0, self.duration - elapsed)

    def timeElapsed(self):
        """경과된 시간을 반환합니다. (밀리초 단위)"""
        if self.startTime is None:
            return 0
        return pygame.time.get_ticks() - self.startTime


#colorSheet
class Cs():
    '''
    Colors의 약자. 색상을 나타내는 클래스\n
    각종 색상의 RGB값 혹은 hexColor를 rgb 튜플로 만들어준다.\n
    '''
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
    def apply(cls,color,r) -> typing.Tuple[int,int,int]:
        f = lambda x: min(255,x*r)
        return tuple([f(x) for x in color])
    @classmethod
    def dark(cls,color) -> typing.Tuple[int,int,int]:
        return Cs.apply(color,0.4)
    @classmethod
    def dim(cls,color)-> typing.Tuple[int,int,int]:
        return Cs.apply(color,0.8)
    @classmethod
    def light(cls,color)-> typing.Tuple[int,int,int]:
        return Cs.apply(color,1.2)
    @classmethod
    def bright(cls,color)-> typing.Tuple[int,int,int]:
        return Cs.apply(color,1.6)
    
    @classmethod
    def hexColor(cls,hex:str)-> typing.Tuple[int,int,int]:
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
    update_fps = 60
    draw_fps = 144
    __window_resolution = (800,600) # 게임 윈도우 해상도

    def getWindowRes() -> typing.Tuple[int,int]:
        '''
        윈도우 해상도를 반환한다.\n
        '''
        if Rs.isFullScreen():
            return Rs.fullScreenRes
        else:
            return Rs.__window_resolution

    #윈도우 해상도를 변화시킨다.    
    def setWindowRes(res:typing.Tuple[int,int]):
        '''
        윈도우 해상도를 설정한다.\n
        res : (가로,세로) 튜플\n
        주 모니터의 최대 해상도보다 클 경우 강제로 조정된다.
        '''
        ##주 모니터의 최대 해상도보다 클 경우 강제 조정
        ##Test
        max_res = Rs.fullScreenRes
        if res[0]>max_res[0] or res[1]>max_res[1]:
            res = max_res
        Rs.__window_resolution = res
        Rs.__updateWindow()


    screen_size = (1920,1080) # 게임을 구성하는 실제 스크린의 픽셀수
    screen = pygame.Surface.__new__(pygame.Surface)
    _screenCapture  = None
    _screenBuffer = pygame.Surface.__new__(pygame.Surface)


    __fullScreen = False # 풀스크린 여부를 체크하는 인자
    draggedObj = None # 드래깅되는 오브젝트를 추적하는 인자
    dropFunc = lambda:None # 드래깅이 끝났을 때 실행되는 함수
    
    __lastState=(False,False,False)
    __justClicked = [False,False,False] # 유저가 클릭하는 행위를 했을 때의 시점을 포착하는 인자.
    __justReleased = [False,False,False]
    __lastKeyState = None # 마지막의 키 상태를 저장하는 인자.
    __mousePos = RPoint(0,0)
    _mouseTransformer = (1,1) ##마우스 위치를 디스플레이->게임스크린으로 보내기 위해 필요한 변환인자
    @classmethod
    #internal update function
    def _update(cls):

        ###Mouse Pos Transform 처리
        #윈도우 해상도에서 실제 게임내 픽셀로 마우스 위치를 옮겨오는 역할
        Rs.__mousePos = RPoint(pygame.mouse.get_pos()[0]*Rs._mouseTransformer[0],pygame.mouse.get_pos()[1]*Rs._mouseTransformer[1])

        ###Mouse Click Event 처리
        state = pygame.mouse.get_pressed()
        for i,_ in enumerate(state):
            if i==0 and (Rs.__lastState[i],state[i])==(True,False): # Drag 해제.
                ##드래그 해제 이벤트 처리
                Rs.draggedObj=None
                Rs.dropFunc()
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


        ##등록된 팝업들 업데이트
        for popup in Rs.__popupPipeline:
            Rs.__popupPipeline[popup].update()
        
        ##팝업 제거
        for rpopup in Rs.__removePopupList:
            del Rs.__popupPipeline[rpopup]
        Rs.__removePopupList.clear()
        
                
        ##animation 처리
        for animation in Rs.__animationPipeline:
            if animation["obj"].isEnded():
                if animation["stay"]>time.time():
                    continue
                else:
                    Rs.__animationPipeline.remove(animation)
            else:
                animation["obj"].update()
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

        ##transition(장면 전환) 처리
        if Rs.__transitionTimer.isOver():
            Rs.__transitionCallBack()
            Rs.__transitionCallBack = None
            Rs.__transitionTimer.stop()

        Rs.__lastState=state
    
    @classmethod
    def _updateState(cls):
        Rs.__lastKeyState=pygame.key.get_pressed()
        
    @classmethod
    def _draw(cls):
        ##배경화면을 검게 채운다.
        Rs.window.fill(Cs.black)
        ##등록된 팝업들을 그린다.
        for popup in Rs.__popupPipeline:
            Rs.__popupPipeline[popup].draw()

        ##장면 전환 중일 경우, 스크린샷을 대신하여 그린다.
        if Rs.isTransitioning():
            Rs.drawScreenShot()

        ##등록된 애니메이션들을 재생한다.
        for animation in Rs.__animationPipeline:
            animation["obj"].draw()
        for obj in Rs.__fadeAnimationPipeline:
            obj["Obj"].draw()

    ##FullScreen 관련 함수
    @classmethod
    def isFullScreen(cls) -> bool:
        '''
        풀스크린 여부를 반환한다.\n
        '''
        return Rs.__fullScreen

    @classmethod
    def toggleFullScreen(cls):
        '''
        풀스크린 모드를 토글한다.\n
        '''
        Rs.__fullScreen = not Rs.isFullScreen()
        Rs.__updateWindow()

    
    @classmethod
    def setFullScreen(cls,t:bool=True):
        Rs.__fullScreen = t
        Rs.__updateWindow()
    @classmethod
    def __updateWindow(cls):
        if Rs.isFullScreen():
            Rs.window = pygame.display.set_mode(Rs.getWindowRes(),pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            Rs.window = pygame.display.set_mode(Rs.getWindowRes(),pygame.DOUBLEBUF | pygame.HWSURFACE)
        #마우스 위치를 윈도우 해상도->게임 스크린으로 보내는 변환자
        x,y = Rs.getWindowRes()
        Rs._mouseTransformer=(Rs.screen_size[0]/x,Rs.screen_size[1]/y)

        Rs.window.fill(Cs.black)



    ##기타 함수
    @classmethod
    #Return copied graphics object
    def copy(cls,obj) -> graphicObj:
        '''
        그래픽 객체를 복사. (graphicObj)
        '''
        new_obj = graphicObj()
        new_obj.pos = obj.geometryPos
        new_obj.graphic = copy.copy(obj.graphic)
        new_obj.graphic_n = copy.copy(obj.graphic_n)
        return new_obj

    @classmethod
    def copyImage(cls,obj) -> imageObj:
        '''
        이미지 객체를 복사. (imageObj)
        '''
        new_obj = imageObj()
        new_obj.pos = obj.geometryPos
        new_obj.graphic = copy.copy(obj.graphic)
        new_obj.graphic_n = copy.copy(obj.graphic_n)
        new_obj.scale = obj.scale
        new_obj.angle = obj.angle
        return new_obj

    #__init__을 호출하지 않고 해당 객체를 생성한다.
    #vscode 인텔리센스 사용을 위해 쓰는 신택스 슈가 함수.
    @classmethod
    def new(cls,obj):
        return obj.__new__(obj)
    
    @classmethod
    #Tuple to Point
    def Point(cls,tuple,y=None) -> RPoint:
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
    __curVoice = None ##현재 재생된 음성파일을 저장한다.
    @classmethod
    def playSound(cls,fileName:str,*,loops=0,maxtime=0,fade_ms=0,volume=1):
        '''
        사운드 재생. wav와 ogg파일을 지원한다. 중복재생이 가능하다. \n
        loops=-1 인자를 넣을 경우 무한 반복재생.   
        '''
        fileName = Rs.getPath(fileName)
        if fileName not in list(Rs.__soundPipeline):
            Rs.__soundPipeline[fileName] = pygame.mixer.Sound(fileName)         
        mixer = Rs.__soundPipeline[fileName]
        mixer.set_volume(volume*Rs.__masterSEVolume)
        mixer.play(loops,maxtime,fade_ms)
        return mixer
    @classmethod
    def stopSound(cls,fileName:str):
        fileName = Rs.getPath(fileName)
        if fileName not in list(Rs.__soundPipeline):
            return
        mixer = Rs.__soundPipeline[fileName]
        mixer.stop()        
    @classmethod
    def playVoice(cls,fileName:str,*,volume=1):
        '''
        음성 재생. wav와 ogg파일을 지원한다. 효과음(특히 음성)이 중복재생 되는 것을 막아준다. \n
        '''
        if Rs.__curVoice!=None:
            Rs.__curVoice.stop()
        Rs.__curVoice = Rs.playSound(fileName,volume=volume) 

    __currentMusic = None
    __musicVolumePipeline = {}
    __changeMusic = None
    #여기서의 volume값은 마스터값이 아니라 음원 자체의 볼륨을 조절하기 위한 것이다. 음원이 너무 시끄럽거나 할 때 값을 낮춰잡는 용도
    @classmethod
    def playMusic(cls,fileName:str,*,loops=-1,start=0.0,volume=1.0):
        '''
        음악 재생. mp3, wav, ogg파일을 지원한다. 중복 스트리밍은 불가능. \n
        loops=-1 인자를 넣을 경우 무한 반복재생. 0을 넣을 경우 반복 안됨
        볼륨은 0~1 사이의 float이다.
        음원의 자체 볼륨이 너무 크거나 작거나 할 때 조정할 수 있다. 실제론 __masterVolume과 곱해진다.
        '''
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
    def changeMusic(cls,fileName:str,_time=500,volume=1):
        Rs.fadeoutMusic(_time)
        Rs.__changeMusic = {"Name":fileName,"Time":time.time()+_time/1000.0,"Volume":volume}

    @classmethod
    def currentMusic(cls):
        return Rs.__currentMusic       
    ##음악의 볼륨 값을 정한다.##
    @classmethod
    def setVolume(cls,volume:float):
        Rs.__masterVolume = volume
        if Rs.currentMusic() in Rs.__musicVolumePipeline:
            pygame.mixer.music.set_volume(volume*Rs.__musicVolumePipeline[Rs.currentMusic()])
        else:
            pygame.mixer.music.set_volume(volume)
    @classmethod
    def getVolume(cls) -> float:
        return Rs.__masterVolume
    @classmethod
    def setSEVolume(cls,volume:float):
        Rs.__masterSEVolume = volume
    @classmethod
    def getSEVolume(cls) -> float:
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
        '''
        음악 볼륨 슬라이더 객체를 반환한다.\n
        '''


        slider=sliderObj(pos=pos,length=length,thickness=thickness,color=color,isVertical=isVertical,value=1)
        def volumeUpdate():
            Rs.setVolume(slider.value)
        slider.connect(volumeUpdate)
        return slider
    @classmethod
    def SEVolumeSlider(cls,pos=RPoint(0,0),length=300,thickness=13,color=Cs.white,isVertical=False):
        '''
        효과음 볼륨 슬라이더 객체를 반환한다.\n
        '''
        slider=sliderObj(pos=pos,length=length,thickness=thickness,color=color,isVertical=isVertical,value=1)
        def SEVolumeUpdate():
            Rs.setSEVolume(slider.value)
        slider.connect(SEVolumeUpdate)
        return slider

    ###기본적인 드로잉 함수 (사각형 드로잉)
    @classmethod
    #Fill Screen with Color
    def fillScreen(cls,color):
        screenRect = Rs.screen.get_rect()
        Rs.fillRect(color,screenRect)

    #Fill Rectangle with color
    @classmethod
    def fillRect(cls,color,rect,*,special_flags=0):
        Rs.screen.fill(color,rect,special_flags)

    #폰트 파이프라인(Font Pipeline)
    __fontPipeline ={}

    ##기본 폰트 설정
    __defaultFontPipeline = {
        "default":{ "font":"korean_button.ttf","size":15},
        "button":{"font":"korean_button.ttf","size":30},
    }
    #기본 설정된 폰트를 변경
    @classmethod
    def setDefaultFont(cls,key="default",*,font="korean_button.ttf",size=15):
        '''
        기본 폰트를 설정한다.\n
        '''
        Rs.__defaultFontPipeline[key] = {"font":font,"size":size}
        return

    #기본 폰트값을 반환한다.
    @classmethod
    def getDefaultFont(cls,key="default") -> typing.Dict[str,typing.Union[str,int]]:
        '''
        기본 폰트값을 반환한다.\n
        '''
        return Rs.__defaultFontPipeline[key]


    @classmethod    
    def getFont(cls, font:str) -> freetype.Font:
        '''
        폰트 문자열을 입력하면 폰트 객체를 반환하는 함수.\n
        '''

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
    def drawString(cls,text,pos,*,color=(0,0,0),font=None,size=None,bcolor=None,rotation=0,style=freetype.STYLE_DEFAULT) -> pygame.Rect:
        '''
        textObj 선언할 필요 없이 화면에 문자열을 그린다. \n
        텍스트의 경계를 반환한다.\n
        '''
        if font == None:
            font = Rs.__sysFontName
        if size == None:
            size = Rs.__sysSize
        if type(pos) != tuple:
            pos = pos.toTuple()
        if type(text) != str:
            text = str(text)
        return Rs.getFont(font).render_to(Rs.screen, pos, text, color,bcolor,size=size,rotation=rotation,style=style)


    ##벤치마크 관련##
    ##현재 잘 안써서 제거하거나 수정할 예정
    
    @classmethod
    def drawBenchmark(cls,pos=RPoint(0,0),color=Cs.white):
        p1 = RPoint(20,10)+pos
        p2 = RPoint(70,10)+pos
        p3 = RPoint(10,30)+pos
        s = str(int(REMOGame.benchmark_fps["Draw"]))
        Rs.drawString(s,p1,color=color)
        s = str(int(REMOGame.benchmark_fps["Update"]))
        Rs.drawString(s,p2,color=color)

        Rs.drawString("Draw Update",p3,color=color)

    @classmethod
    def removeFrameLimit(cls):
        Rs.setFrameLimit(999)

    @classmethod
    def setFrameLimit(cls,fps):
        Rs.draw_fps = fps


    ###Path Pipeline###
    __pathData={} ## 확장자에 따라 경로를 분류하는 딕셔너리
    __pathPipeline={} ## 파일명과 실제 경로를 연결하는 딕셔너리
    __pathException=[".git",".pyc",".py"] ##해당 글자가 들어있으면 파이프라인에서 제외된다.
    @classmethod
    def _buildPath(cls):
        '''
        현재 파일이 포함된 경로의 내부 폴더들을 전부 참조하여 경로 파이프라인을 빌드하는 함수. 내부적으로 사용된다.\n
        '''
        Rs.__pathData={}
        Rs.__pathPipeline={}
        import os
        #확장자명에 따른 파일분류
        for currentpath, folders, files in os.walk('.'):
            for file in files:
                if file[0]==".": # 숨김 파일은 기본적으로 제외한다.
                    continue
                path = os.path.join(currentpath, file)
                _except = False
                for ex in Rs.__pathException: ## 제외어가 들어간 경우 제외한다. 예를 들어 .git 관련 파일들은 제외
                    if ex in path:
                        _except = True
                if _except:
                    continue
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
        '''
        파일명을 입력하면 실제 경로를 반환하는 함수.\n
        가령 실제 파일 경로가 /Resources/sprites/testGirl.png 여도 \n
        testGirl.png만 해도 찾아내준다. \n
        '''
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
    def assetExist(cls,path) -> bool:
        if path in list(Rs.__pathPipeline):
            return True
        return False
    
    __imagePipeline={}
    @classmethod
    def getImage(cls,path) -> pygame.Surface:
        '''
        이미지를 로드하여 캐싱하는 함수.\n
        '''
        path = Rs.getPath(path)
        if path not in Rs.__imagePipeline:
            Rs.__imagePipeline[path]=pygame.image.load(path).convert_alpha()            
        return Rs.__imagePipeline[path]
    
    #이미지 스프라이트에서 rect영역을 잘라낸 함수 
    __spritePipeline={}
    @classmethod
    def getSprite(cls,path,rect):
        '''
        이미지 스프라이트에서 rect영역만큼 잘라내어 반환하는 함수.\n
        해당 과정에서 캐싱이 일어난다. \n
        '''
        key = (path,str(rect))
        if key not in Rs.__spritePipeline:
            sprite = Rs.getImage(path).subsurface(rect)
            Rs.__spritePipeline[key]=sprite
        return Rs.__spritePipeline[key]
    
    
    ##애니메이션 재생을 위한 함수
    ##애니메이션이 한번 재생되고 꺼진다.
    ##애니메이션은 기본적으로 화면 맨 위에서 재생된다.

    #stay: 애니메이션이 화면에 남아있는 시간.(단위:ms)
    __animationPipeline=[]
    @classmethod
    def playAnimation(cls,sprite,stay=0,*,rect=None,pos=RPoint(0,0),sheetMatrix=(1,1),center=None,scale=1.0,frameDuration=1000/60,angle=0,fromSprite=0,toSprite=None,alpha=255) -> spriteObj:
        obj = spriteObj(sprite,rect,pos=pos,frameDuration=frameDuration,scale=scale,angle=0,sheetMatrix=sheetMatrix,fromSprite=fromSprite,toSprite=toSprite,mode=AnimationMode.PlayOnce)
        obj.alpha = alpha
        if center!=None:
            obj.center = center
        Rs.__animationPipeline.append({"obj":obj,"stay":time.time()+stay/1000.0})
        
        return obj
        
    ##페이드아웃 애니메이션 재생을 위한 함수.
    __fadeAnimationPipeline=[]
    @classmethod
    def fadeAnimation(cls,obj,*,time=30,alpha=255):
        Rs.__fadeAnimationPipeline.append({"Obj":obj,"Max":time,"Time":time,"Alpha":alpha})
    
    @classmethod
    def clearAnimation(cls):
        '''
        재생중인 애니메이션을 모두 지운다.
        '''
        Rs.__animationPipeline.clear()
        Rs.__fadeAnimationPipeline.clear()        
    ##스크린샷 - 현재 스크린을 캡쳐하여 저장한다.
    screenShot = None
    #스크린샷 캡쳐
    @classmethod
    def captureScreenShot(cls):        
        Rs.screenShot = Rs._screenCapture.copy() #마지막으로 버퍼에 남아있는 그림을 가져온다.
    
        return Rs.screenShot

    @classmethod
    def drawScreenShot(cls):
        Rs.screen.blit(Rs.screenShot,(0,0))
        
    ###User Input Functions###
    
    #Mouse Click Detector
    @classmethod
    def mousePos(cls) -> RPoint:
        return Rs.__mousePos
    @classmethod
    def userJustLeftClicked(cls) -> bool:
        return Rs.__justClicked[0]
    
    @classmethod
    def userJustReleasedMouseLeft(cls) -> bool:
        return Rs.__justReleased[0]

    @classmethod
    def userJustReleasedMouseRight(cls) -> bool:
        return Rs.__justReleased[2]

    @classmethod
    def userIsLeftClicking(cls) -> bool:
        return pygame.mouse.get_pressed()[0]

    @classmethod
    def userIsRightClicking(cls) -> bool:
        return pygame.mouse.get_pressed()[2]

    @classmethod
    def userJustRightClicked(cls) -> bool:
        return Rs.__justClicked[2]

    #Key Push Detector
    @classmethod
    def userJustPressed(cls,key) -> bool:
        if Rs.__lastKeyState == None:
            return False
        keyState = pygame.key.get_pressed()
        if (Rs.__lastKeyState[key],keyState[key])==(False,True):
            return True
        else:
            return False
    
    @classmethod
    def userPressing(cls,key) -> bool:
        '''
        키가 눌려져 있는지를 체크하는 함수 \n
        key: ex) pygame.K_LEFT        
        '''
        return pygame.key.get_pressed()[key]
    

    ##Drag and Drop Handler##
    @classmethod
    def dragEventHandler(cls,triggerObj,draggedObj=None,draggingFunc=lambda:None,dropFunc=lambda:None):
        '''
        Drag & Drop Event Handler \n
        triggerObj : 드래그가 촉발되는 객체 \n
        draggedObj : 드래그되는 객체. 설정하지 않을 경우 triggerObj와 같다. \n
        draggingFunc : 드래깅 중 실행되는 함수 \n
        dropFunc : 드래그가 끝날 때 실행되는 함수 \n
        Scene의 update 함수 안에 넣어야 동작합니다.
        '''
        if draggedObj==None:
            draggedObj = triggerObj
        if Rs.userJustLeftClicked() and triggerObj.collideMouse():
            Rs.draggedObj = draggedObj
            Rs.dragOffset = Rs.mousePos()-draggedObj.pos
            Rs.dropFunc = dropFunc
        if Rs.userIsLeftClicking() and Rs.draggedObj == draggedObj:
            draggedObj.pos = Rs.mousePos()-Rs.dragOffset
            draggingFunc()



    ##Draw Function##
    
    __graphicPipeline = {}
    __spritePipeline = {}
    graphicCache ={}
    
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
        '''
        현재 Scene을 교체한다.\n
        '''
        REMOGame.drawLock = True
        REMOGame.setCurrentScene(scene,skipInit)
        REMOGame.drawLock = False

    ##디스플레이 아이콘을 바꾼다.
    @classmethod
    def setIcon(cls,img):
        img = Rs.getImage(img)
        pygame.display.set_icon(img)

    ##드로우 쓰레드에 락을 걸어야 할 때 사용하는 함수
    @classmethod
    def acquireDrawLock(cls):
        '''
        드로우 락을 걸어서, 드로우 쓰레드가 드로우를 하지 못하게 한다.
        Scene의 update 함수 안에서만 사용할것. 안 그러면 데드락이 걸릴 수 있다.
        '''
        REMOGame.drawLock = True 
    ##락 해제
    @classmethod
    def releaseDrawLock(cls):
        '''
        드로우 락을 해제한다.
        Scene의 update 함수 안에서만 사용할것. 안 그러면 데드락이 걸릴 수 있다.
        '''
        REMOGame.drawLock = False
        
        

    ##Random

    #가중치가 있는 랜덤 초이스 함수
    #ex: {1:0.3,2:0.7}... value가 가중치가 된다
    @classmethod
    def randomPick(cls,data:dict):
        m = sum(list(data.values()))
        v = 0
        r = random.random()
        for k in data:
            v+= data[k]/m
            if r<v:
                return k
        return list(data)[-1]


    ##팝업 관련 함수
    ##팝업은, 화면 맨 위쪽에 띄워지는 오브젝트들을 의미한다.
    ##DialogObj 등을 여기에 등록하면 좋다.
    __popupPipeline = {}
    __removePopupList = []
    @classmethod
    def addPopup(cls,popup):
        Rs.__popupPipeline[id(popup)] = popup
    @classmethod
    def removePopup(cls,popup):
        Rs.__removePopupList.append(id(popup))

    @classmethod
    def isPopup(cls,popup):
        '''
        해당 오브젝트가 팝업되어 있는지를 체크하는 함수
        '''
        return id(popup) in Rs.__popupPipeline
    @classmethod
    def mouseCollidePopup(cls):
        '''
        팝업 중 마우스와 충돌하는 팝업이 있는지를 체크하는 함수
        '''
        for popup in Rs.__popupPipeline:
            if Rs.__popupPipeline[popup].collideMouse():
                return True
        return False
    @classmethod
    def popupExists(self):
        '''
        현재 팝업이 존재하는지를 체크하는 함수
        '''
        return len(Rs.__popupPipeline)>0
    

    ##트랜지션 관련 함수
    ##트랜지션은 화면 전환 효과를 의미한다.
    ##Scene을 교체할 때 사용된다.

    __defaultTransition = "swipe"
    __transitionTimer = RTimer(1000,False) ##장면 전환 타이머
    __transitionCallBack = None ##장면 전환을 실제로 실행할 콜백함수

    __transitionOptions ={
        "wave":{"fileName":"scene_transition_02.png","sheetMatrix":(6,5),"time":500},
        "inkSpill":{"fileName":"scene_transition_01.png","sheetMatrix":(7,5),"time":1000},
        "curtain":{"fileName":"scene_transition_03.png","sheetMatrix":(4,5),"time":500},
        "swipe":{"fileName":"scene_transition_04.png","sheetMatrix":(4,5),"time":300},
        "waterFill":{"fileName":"scene_transition_05.png","sheetMatrix":(18,5),"time":1600},
    }

    @classmethod
    def updateTransitionOption(self,opt):
        '''
        장면 전환 옵션을 (추가)업데이트하는 함수.\n
        opt : 딕셔너리. "fileName", "sheetMatrix", "scale", "time"입력 \n
        '''
        Rs.__transitionOptions.update(opt)

    @classmethod
    def setDefaultTransition(cls,transition:str):
        '''
        기본으로 실행될 장면 전환 효과를 설정하는 함수.\n
        '''
        Rs.__defaultTransition = transition

    @classmethod
    def transition(cls,scene,effect:typing.Optional[str]=None):
        '''
        장면 전환 효과를 실행하는 함수.\n
        scene : 전환될 Scene 객체\n
        effect : 효과의 종류를 지정한다. __transitonOptions 항목을 참조.\n
        '''
        if effect==None:
            effect = Rs.__defaultTransition
        option = Rs.__transitionOptions[effect]
        Rs.playAnimation(option["fileName"],sheetMatrix=option["sheetMatrix"],rect=Rs.screen.get_rect(),frameDuration=1000/40,alpha=255)
        Rs.captureScreenShot()
        cls.__transitionTimer.start(option["time"])
        cls.__transitionCallBack = lambda:REMOGame.setCurrentScene(scene)

    ##트랜지션 중인지 확인하는 함수
    @classmethod
    def isTransitioning(cls):
        '''
        트랜지션 중인지를 체크하는 함수.\n
        '''
        return Rs.__transitionTimer.isRunning()

Rs._buildPath() ## 경로 파이프라인을 구성한다.

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

#target_fps에 맞게 그리기 함수를 호출하는 스레드

class drawThread():

    def __init__(self):
        super().__init__()
    def run(self):
        while REMOGame._lastStartedWindow.running:
            if not REMOGame.drawLock:
                try:
                    REMOGame._lastStartedWindow.draw()
                    REMOGame._lastStartedWindow.paint()
                except Exception as err:
                    import traceback
                    traceback.print_exc()
                    continue
                REMOGame.drawClock.tick(REMOGame.target_fps)




## Base Game class
class REMOGame:
    currentScene = Scene()
    __drawThread = drawThread()
    benchmark_fps = {"Draw":0,"Update":0}
    target_fps = 60
    drawLock = False ## 신 교체 중임을 알리는 인자
    clock = pygame.time.Clock() ##프레임 제한을 위한 클락
    drawClock = pygame.time.Clock() ##드로우 쓰레드의 클락
    __showBenchmark = False
    _lastStartedWindow = None
    def __init__(self,window_resolution=(1920,1080),screen_size = (1920,1080),fullscreen=True,*,caption="REMOGame window"):

        ##파이게임 윈도우가 화면 밖을 벗어나는 문제를 해결하기 위한 코드
        if sys.platform == 'win32':
            # On Windows, the monitor scaling can be set to something besides normal 100%.
            # PyScreeze and Pillow needs to account for this to make accurate screenshots.
            import ctypes
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass # Windows XP doesn't support monitor scaling, so just do nothing.

        pygame.init()
        info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
        Rs.fullScreenRes = (info.current_w,info.current_h) ##풀스크린의 해상도를 확인한다.
        Rs.__fullScreen=fullscreen
        Rs.screen_size = screen_size
        Rs.setWindowRes(window_resolution)
        pygame.display.set_caption(caption)
        REMOGame._lastStartedWindow = self
        # Fill the background with white
        Rs.screen = pygame.Surface(screen_size,pygame.SRCALPHA,32).convert_alpha()
        Rs._screenBuffer = Rs.screen.copy()
        Rs.screen.fill(Cs.white)
        Rs.setFullScreen(fullscreen)


    def setWindowTitle(self,title):
        pygame.display.set_caption(title)
        
    #게임이 시작했는지 여부를 확인하는 함수
    @classmethod 
    def gameStarted(cls):
        return REMOGame._lastStartedWindow != None        
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
    
    @classmethod
    def showBenchmark(cls):
        REMOGame.__showBenchmark = True

    def draw(self):
        Rs.screen.fill(Cs.black) ## 검은 화면
        REMOGame.currentScene.draw()
        Rs._draw()
        Rs._screenCapture = Rs.screen.copy()
        Rs._screenBuffer = pygame.transform.smoothscale(Rs._screenCapture,Rs.getWindowRes())
        Rs.window.blit(Rs._screenBuffer,(0,0))
        if REMOGame.__showBenchmark:
            Rs.drawBenchmark()
        pygame.display.flip()

        return
    
    @classmethod
    def exit(cls):
        REMOGame._lastStartedWindow.running = False
        REMOGame.__drawThread.join()

        #pygame.quit()

    #Game Running Method
    def run(self):
        self.running = True
        import threading
        REMOGame.__drawThread = threading.Thread(target=drawThread().run)
        REMOGame.__drawThread.start()

        while self.running:
            try:
                Rs._update()
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        REMOGame.exit()
                if not Rs.isTransitioning():
                    self.update()

                Rs._updateState()

                REMOGame.clock.tick(REMOGame.target_fps)
            except:
                import traceback
                traceback.print_exc()
                self.running = False


    def paint(self):
        pygame.display.update()

### Graphic Objects ###

#abstract class for graphic Object
class graphicObj():


    ##포지션 편집 및 참조 기능
    ##pygame.Rect의 attributes(topleft, topright 등...)를 그대로 물려받습니다.
    #(pos, rect)는 실제론 obj의 parent의 pos를 원점(0,0)으로 하였을 때의 object의 위치와 영역을 의미합니다.

    @property
    def pos(self) -> RPoint:
        return self._pos
    @pos.setter
    def pos(self,pos):
        delta = pos - self._pos
        self._pos = Rs.Point(pos)
        if self.parent==None and id(self) in Rs.graphicCache:
            Rs.graphicCache[id(self)][1]+=delta
        else:
            self._clearGraphicCache()
    def moveTo(self,p2,speed):
        self.pos = self.pos.moveTo(p2,speed)


    def __adjustPosBy(self,attr,_point):
        if type(_point)==RPoint:
            _point = _point.toTuple()
        _rect = self.rect.copy()
        setattr(_rect,attr,_point)
        self.pos = RPoint(_rect.topleft)

    @property
    def size(self):
        return self.rect.size
    @size.setter
    def size(self,size):
        self.rect = pygame.Rect(self.pos.x,self.pos.y,size[0],size[1])

    @property
    def x(self):
        return RPoint(self.rect.x)
    @x.setter
    def x(self,_x):
        self.__adjustPosBy("x",_x)


    @property
    def y(self):
        return RPoint(self.rect.y)
    @y.setter
    def y(self,_y):
        self.__adjustPosBy("y",_y)

    @property
    def center(self):
        return RPoint(self.rect.center)
    @center.setter
    def center(self,_center):
        self.__adjustPosBy("center",_center)


    @property
    def topright(self):
        return RPoint(self.rect.topright)
    @topright.setter
    def topright(self,_topright):
        self.__adjustPosBy("topright",_topright)

    @property
    def bottomright(self):
        return RPoint(self.rect.bottomright)
    @bottomright.setter
    def bottomright(self,_bottomright):
        self.__adjustPosBy("bottomright",_bottomright)


    @property
    def bottomleft(self):
        return RPoint(self.rect.bottomleft)
    @bottomleft.setter
    def bottomleft(self,_bottomleft):
        self.__adjustPosBy("bottomleft",_bottomleft)

    @property
    def midleft(self):
        return RPoint(self.rect.midleft)
    @midleft.setter
    def midleft(self,_midleft):
        self.__adjustPosBy("midleft",_midleft)

    @property
    def midright(self):
        return RPoint(self.rect.midright)
    @midright.setter
    def midright(self,_midright):
        self.__adjustPosBy("midright",_midright)

    @property
    def midtop(self):
        return RPoint(self.rect.midtop)
    @midtop.setter
    def midtop(self,_midtop):
        self.__adjustPosBy("midtop",_midtop)

    @property
    def midbottom(self):
        return RPoint(self.rect.midbottom)
    @midbottom.setter
    def midbottom(self,_midbottom):
        self.__adjustPosBy("midbottom",_midbottom)

    @property
    def centerx(self) -> int:
        return self.rect.centerx
    @centerx.setter
    def centerx(self,_p:int):
        self.__adjustPosBy("centerx",_p)

    @property
    def centery(self) -> int:
        return self.rect.centery
    @centery.setter
    def centery(self,_p:int):
        self.__adjustPosBy("centery",_p)

    ##Rect is combination of (pos,size)
    ##pos : position of the object, size : size of the object
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x,self.pos.y,self.graphic.get_rect().w,self.graphic.get_rect().h)

    #could be replaced
    @rect.setter
    def rect(self,rect:pygame.Rect):
        self.graphic = pygame.transform.smoothscale(self.graphic_n,(rect[2],rect[3]))
        self._pos = RPoint(rect[0],rect[1])
        self._clearGraphicCache()

    @property
    def offsetRect(self) -> pygame.Rect:
        ''' 
        pos를 (0,0)으로 처리한 rect를 반환합니다.
        '''
        return pygame.Rect(0,0,self.graphic.get_rect().w,self.graphic.get_rect().h)


    #geometry란 object가 실제로 screen상에서 차지하는 영역을 의미합니다.
    #getter only입니다.
    @property
    def geometry(self) -> pygame.Rect:
        if self.parent:
            return pygame.Rect(self.parent.geometry.x+self.pos.x,self.parent.geometry.y+self.pos.y,self.rect.width,self.rect.height)
        return self.rect
    
    #object의 실제 스크린 상의 위치 
    @property
    def geometryPos(self) -> RPoint:
        if self.parent:
            return RPoint(self.parent.geometry.x+self.pos.x,self.parent.geometry.y+self.pos.y)
        return self.pos
    
    #object의 스크린상에서의 실제 중심 위치
    @property
    def geometryCenter(self) -> RPoint:
        if self.parent:
            return self.geometryPos+RPoint(self.rect.w,self.rect.h)*0.5
        return self.center
    
    #object의 차일드들의 영역을 포함한 전체 영역을 계산 (캐싱에 활용)
    @property
    def boundary(self) -> pygame.Rect:
        if id(self) in Rs.graphicCache:
            cache,pos = Rs.graphicCache[id(self)]
            return pygame.Rect(pos.x,pos.y,cache.get_rect().w,cache.get_rect().h)

        r = self.geometry
        ## 모든 차일드의 경계를 합친다.
        for l in self.childs.values():
            for c in l:
                r = r.union(c.boundary)
        return r
    
    def getBoundary(self,depth:int=0):
        '''
        해당 depth를 가진 차일드들의 전체 영역을 계산한다.
        '''

        r = None
        for c in self.childs[depth]:
            if r==None:
                r = c.boundary
            else:
                r = r.union(c.boundary)
        return r


    @property
    def alpha(self) -> int:
        '''
        0~255 사이의 알파값을 반환합니다. 255:완전 불투명 0: 투명
        '''
        return self._alpha
    
    @alpha.setter
    def alpha(self,alpha:int):
        '''
        0~255 사이의 알파값을 설정합니다. 255:완전 불투명 0: 투명
        '''
        self._alpha = alpha
        self._clearGraphicCache()

    @property
    def graphic(self) -> pygame.Surface:
        return self._graphic
    
    ##그래픽이 변경되면 캐시를 청소한다.
    @graphic.setter
    def graphic(self,graphic:pygame.Surface):
        self._graphic = graphic
        self._clearGraphicCache()


    ##그래픽 캐시 관련 함수 ##
    #오브젝트의 캐시 이미지를 만든다.
    def _getCache(self):
        if id(self) in Rs.graphicCache:
            try:
                return Rs.graphicCache[id(self)]
            except:
                pass

        # id가 없으므로 childs의 재귀적 union을 통해 전체 영역을 계산
        r = self.boundary
        
        bp = RPoint(r.x,r.y) #position of boundary
        cache = pygame.Surface((r.w,r.h),pygame.SRCALPHA,32).convert_alpha()

        depth_excluded = list(set(self.childs.keys())-self._hidedDepth)
        depth_excluded.sort()

        negative_depths = []
        positive_depths = []
        for d in depth_excluded:
            if d<0:
                negative_depths.append(d)
            else:
                positive_depths.append(d)
            


        ##depth가 음수인 차일드들을 먼저 그린다.
        for depth in negative_depths:
            l = self.childs[depth]
            for c in l:
                ccache,cpos = c._getCache()
                p = cpos-bp
                cache.blit(ccache,p.toTuple(),special_flags=pygame.BLEND_ALPHA_SDL2)

        cache.blit(self.graphic,(self.geometryPos-bp).toTuple())

        ##depth가 양수인 차일드들을 그린다.
        for depth in positive_depths:
            l = self.childs[depth]
            if depth==0 and self.isViewport(): ##뷰포트일 경우, depth 0의 차일드는 rect 안쪽에 그려진다.
                viewport = pygame.Surface((self.rect.w,self.rect.h),pygame.SRCALPHA,32).convert_alpha()
                gp = self.geometryPos
                for c in l:
                    ccache,cpos = c._getCache()
                    cache_boundary = pygame.Rect(cpos.x,cpos.y,ccache.get_rect().w,ccache.get_rect().h)

                    if cache_boundary.colliderect(self.geometry):
                        viewport.blit(ccache,(cpos-gp).toTuple(),special_flags=pygame.BLEND_ALPHA_SDL2)

                cache.blit(viewport,(gp-bp).toTuple())
            else:
                for c in l:
                    ccache,cpos = c._getCache()
                    p = cpos-bp
                    cache.blit(ccache,p.toTuple(),special_flags=pygame.BLEND_ALPHA_SDL2)

        cache.set_alpha(self.alpha)
        return [cache,bp]

    #object의 차일드를 포함한 그래픽을 캐싱한다.
    def _cacheGraphic(self):
        try:
            Rs.graphicCache[id(self)]=self._getCache()
        except:
            pass

    ##캐시 청소 (그래픽을 새로 그리거나 위치를 옮길 때 캐시 청소가 필요)    
    def _clearGraphicCache(self):
        # print(str(self),"cache cleared") ## for DEBUG
        if hasattr(self,"parent") and self.parent:
            self.parent._clearGraphicCache()
        if id(self) in Rs.graphicCache:
            Rs.graphicCache.pop(id(self))

    ##객체 소멸시 캐시청소를 해야 한다.
    def __del__(self):
        self._clearGraphicCache()
    ###

    def showChilds(self,depth):
        '''
        해당 depth를 가진 차일드를 보이게 한다.
        '''
        if depth in self._hidedDepth:
            self._hidedDepth.remove(depth)
            self._clearGraphicCache()
        
    def hideChilds(self,depth):
        '''
        해당 depth를 가진 차일드를 숨긴다.
        '''
        if depth not in self._hidedDepth:
            self._hidedDepth.add(depth)
            self._clearGraphicCache()

    def getChilds(self,depth=0):
        '''
        해당 depth를 가진 차일드들을 반환한다.
        '''
        return self.childs[depth]

    def __init__(self,rect=pygame.Rect(0,0,0,0)):
        self.graphic_n = pygame.Surface((rect.w,rect.h),pygame.SRCALPHA,32).convert_alpha()
        self.graphic = self.graphic_n.copy()
        self._pos = RPoint(0,0)
        self.childs = {0:[]} ##차일드들을 depth별로 저장한다.
        self._hidedDepth = set() #숨길 depth를 저장한다.
        self.parent = None
        self._depth = None #부모에 대한 나의 depth를 저장한다.
        self._alpha = 255
        self.__isViewport = False # 뷰포트인지 여부를 저장한다. 뷰포트일 경우 depth 0의 차일드는 rect 안쪽에 그려집니다.
        return
    
    def setAsViewport(self,to=True):
        '''
        뷰포트로 설정한다. 그래픽 객체가 뷰포트일 경우, depth 0의 차일드는 rect 안쪽에 그려진다.
        '''
        self.__isViewport = to
    
    def isViewport(self):
        return self.__isViewport

    #Parent - Child 연결관계를 만듭니다.
    #depth는 차일드의 레이어를 의미합니다. depth가 음수이면 부모 아래에, 0 이상이면 부모 위에 그려집니다.
    def setParent(self,_parent,*,depth=0):

        ##기존 부모관계 청산
        if self.parent !=None:
            self.parent.childs[self._depth].remove(self)
            if self._depth == 0 and hasattr(self.parent,'adjustLayout'): ##부모가 레이아웃 오브젝트일 경우, 자동으로 레이아웃을 조정한다.
                self.parent.adjustLayout()

            self._depth = None
            self.parent._clearGraphicCache()

        ##새로운 부모관계 설정
        self.parent = _parent
        if _parent != None:
            if depth not in _parent.childs:
                _parent.childs[depth] = []
            _parent.childs[depth].append(self)
            if depth == 0 and hasattr(_parent,'adjustLayout'): ##부모가 레이아웃 오브젝트일 경우, 자동으로 레이아웃을 조정한다.
                _parent.adjustLayout()
            self._depth = depth
        self._clearGraphicCache()


    #Could be replaced
    def draw(self):        
        if self.alpha==0: ## 알파값이 0일경우는 그리지 않는다
            return
        if id(self) not in Rs.graphicCache:
            self._cacheGraphic()
        cache,p = self._getCache()
        Rs.screen.blit(cache,p.toTuple())

                
    def collidepoint(self,p):
        return self.geometry.collidepoint(Rs.Point(p).toTuple())
    def collideMouse(self):
        return self.collidepoint(Rs.mousePos())
    def isJustClicked(self):
        return Rs.userJustLeftClicked() and self.collidepoint(Rs.mousePos())

   ###merge method: 차일드와 현재의 객체를 병합한다.
    def merge(self):
        self.graphic_n = self._getCache()[0]
        if hasattr(self,'angle'):
            self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)
        else:
            self.graphic = self.graphic_n
        self.childs = {0:[]}        
#image file Object         
class imageObj(graphicObj):
    
    def __init__(self,_imgPath=None,_rect=None,*,pos=None,angle=0,scale=1,isLocked = False):
        '''
        _imgPath : 이미지 경로 혹은 스프라이트 아틀라스 지정 가능. \n
        [이미지 경로, sheetMatrix, index] 형태로 입력할 경우 스프라이트시트로부터 이미지를 불러온다.\n
        ex) 5*7행렬의 스프라이트 시트에서 3번째 이미지를 불러오고 싶을 경우 [이미지 경로, (5,7), 3]을 입력한다.\n
        isLocked : 잠금 이미지를 추가할지 여부를 결정한다. 기본값은 False이다.\n
        '''
        super().__init__()
        if isLocked:
            self.lock()
        else:
            self.lockObj = None # 잠금 이미지 오브젝트

        if _imgPath:
            if type(_imgPath) ==str:
                self.graphic_n = Rs.getImage(_imgPath)
                self.graphic = self.graphic_n.copy()
            else:
                ##스프라이트 시트로부터 이미지를 불러올 경우 즉,
                ##인자로 [이미지 경로, sheetMatrix, index]가 들어올 경우
                _path, _matrix, _index = _imgPath
                sheet = Rs.getImage(_path)
                spriteSize = (sheet.get_rect().w//_matrix[1],sheet.get_rect().h//_matrix[0])
                target_rect = pygame.Rect((_index%_matrix[1])*spriteSize[0],(_index//_matrix[1])*spriteSize[1],spriteSize[0],spriteSize[1])
                self.graphic_n = Rs.getSprite(_path,target_rect)


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


    #Fill object with Color
    def fill(self,color,*,special_flags=pygame.BLEND_MAX):
        
        self.graphic_n = self.graphic_n.copy() # 파이프라인을 망가뜨리지 않기 위해 복사본을 만든다.
        self.graphic_n.fill(color,special_flags=special_flags)
        self.graphic.fill(color,special_flags=special_flags)
        self._clearGraphicCache()

    def colorize(self,color,alpha=255):
        '''
        이미지에 단색을 입히는 함수
        Bug: 현재로선 spriteObj와는 호환이 안됨.
        '''
        self.fill((0,0,0,255),special_flags=pygame.BLEND_RGBA_MULT)
        self.fill(color[0:3]+(0,),special_flags=pygame.BLEND_RGBA_ADD)
        self.alpha = alpha
        self._clearGraphicCache()
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
        self._scale = round(scale,2)
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)

    ##이미지 교환 함수     
    def setImage(self,path):
        self.graphic = Rs.getImage(path)
        self.graphic_n = Rs.getImage(path)
        self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)


    ##이미지 잠금 관련 함수
    #이미지 오브젝트에 잠금 이미지를 추가할 수 있다.
    #갤러리, 업적 등의 해금을 표현할 수 있습니다.

    def isLocked(self):
        '''
        이미지 오브젝트가 잠겨있는지를 체크하는 함수
        '''
        if self.lockObj:
            return True
        return False

    def lock(self,*,depth=2,scale=1):
        '''
        이미지 오브젝트에 잠금 이미지를 추가합니다. \n
        뎁스 2에 잠금 이미지를 추가하며, 원한다면 뎁스를 조절할 수 있습니다. \n
        해당 이미지 오브젝트의 최상위 뎁스에 잠금 이미지를 추가해야 정상 작동합니다. \n
        자물쇠 아이콘의 크기를 조절하려면 scale 인자를 조절하면 됩니다. \n
        이후 잠금 이미지는 .lockObj 어트리뷰트를 통해 접근할 수 있습니다. \n
        '''
        lockImage = Rs.copyImage(self)
        lockImage.colorize(Cs.dark(Cs.grey))
        lockImage.pos = RPoint(0,0)
        lockImage.setParent(self,depth=depth)
        lock = imageObj("ui_locked.png",scale=scale)
        lock.center = self.offsetRect.center
        lock.setParent(lockImage)
        self.lockObj = lockImage
        return lock
    
    def unlock(self):
        '''
        이미지 오브젝트의 잠금을 해제합니다.
        '''
        if self.lockObj:
            self.lockObj.setParent(None)
            self.lockObj.pos = self.pos
            Rs.fadeAnimation(self.lockObj)
            self.lockObj = None
 
        
    
            
##Rectangle Object. could be rounded
class rectObj(graphicObj):
    def _makeRect(self,rect,color,edge,radius):
        self.graphic_n = pygame.Surface((rect.w,rect.h),pygame.SRCALPHA,32).convert_alpha()
        pygame.draw.rect(self.graphic_n,Cs.apply(color,0.7),pygame.Rect(0,0,rect.w,rect.h),border_radius=radius+1)
        pygame.draw.rect(self.graphic_n,Cs.apply(color,0.85),pygame.Rect(edge,edge,rect.w-2*edge,rect.h-2*edge),border_radius=radius+2)

        pygame.draw.rect(self.graphic_n,color,pygame.Rect(2*edge,2*edge,rect.w-4*edge,rect.h-4*edge),border_radius=radius)
        self.graphic = self.graphic_n.copy()
        
    def __init__(self,rect,*,radius=None,edge=0,color=Cs.white,alpha=255):
        '''
        radius: 사각형의 모서리의 둥근 정도
        edge: 테두리의 두께
        radius 값을 넣지 않을 경우 적당히 둥글게 만들어진다. radius=0을 넣을 경우 완전한 사각형이 된다.
        '''
                
        super().__init__()
        if radius==None:
            radius = int(min(rect.w,rect.h)*0.2)

        self._makeRect(rect,color,edge,radius)
        self.pos = Rs.Point(rect.topleft)
        self.alpha=alpha
        self._color = color
        self._radius = radius
        self._edge = edge

    @property
    def edge(self) -> int:
        return self._edge

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self,radius:int):
        temp = self.rect.copy()
        self._radius = radius
        self._makeRect(temp,self.color,self.edge,radius)

    @property
    def color(self) -> typing.Tuple[int,int,int]:
        return self._color

    @color.setter
    def color(self,color:typing.Tuple[int,int,int]):
        temp = self.rect.copy()
        self._color = color
        self._makeRect(temp,color,self.edge,self.radius)


class textObj(graphicObj):
    def __init__(self,text="",pos=(0,0),*,font=None,size=None,color=Cs.white,angle=0):
        '''
        size: 폰트 사이즈
        angle: 폰트 회전 각도(int,시계방향)
        '''
        super().__init__()
        if font==None:
            font = Rs.getDefaultFont("default")["font"]
        if size==None:
            size = Rs.getDefaultFont("default")["size"]
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
    def color(self) -> typing.Tuple[int,int,int]:
        return self.__color

    #컬러값을 변경할 때는 영역이 바뀌지 않는다.
    @color.setter
    def color(self,_color:typing.Tuple[int,int,int]):
        temp = copy.copy(self.rect)
        self.__color = _color
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.rect = copy.copy(temp)
        self._clearGraphicCache()

    @property
    def size(self) -> float:
        return self.__size
    @size.setter
    def size(self,_size:float):
        self.__size = _size
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()

    @property
    def angle(self) -> int:
        return self.__angle
    @angle.setter
    def angle(self,_angle:int):
        self.__angle = _angle
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()

    @property
    def font(self) -> str:
        return self.__font
    @font.setter
    def font(self,_font:str):
        self.__font = _font
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()

    @property
    def text(self) ->str:
        return self.__text
    @text.setter
    def text(self,_text:str):
        self.__text = _text
        self.graphic_n = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        self.graphic = Rs.getFont(self.__font).render(self.__text,self.__color,None,size=self.__size,rotation=self.__angle)[0].convert_alpha()
        


#수정할 예정
#이미지의 List를 인자로 받는 스프라이트 클래스.
#(애니메이션)움직이게 할 수 있다.
class spriteObj(imageObj):
    #sheetMatrix : sprite sheet의 행렬값. 예를 들어 3*5(3행5열) 스프라이트 시트일 경우 (3,5) 입력
    def __init__(self,_imageSource=None,_rect=None,*,pos=RPoint(0,0),sheetMatrix=(1,1),startFrame=None,frameDuration=1000/60,angle=0,scale=1,fromSprite=0,toSprite=None,mode=AnimationMode.Looped):
        '''
        _imageSource : 이미지 경로 혹은 이미지 리스트 \n
        _rect : 이미지의 위치와 크기 \n
        pos : 이미지의 위치 \n
        sheetMatrix : 스프라이트 시트의 행렬값 (행 개수, 열 개수) \n
        startFrame : 시작 프레임 \n  
        frameDuration : 프레임 간격 \n
        angle : 이미지의 각도 \n
        scale : 이미지의 크기 \n
        fromSprite : 시작 스프라이트 \n
        toSprite : 끝 스프라이트 \n
        mode : 애니메이션 모드 \n

        간혹 첫 프레임이 씹힐 수 있는데, 이 때는 frameTimer.reset()을 하고 시작하면 됩니다. \n
        spriteObj는 rect를 명시적으로 전달할 경우, rect를 기준으로 이미지를 조정합니다. \n
        rect를 전달하지 않을 경우, scale,angle을 기준으로 이미지를 조정합니다. \n

        이후 rect 인자를 수정할 경우, 다시 rect를 기준으로 이미지를 조정합니다. \n
        이후 scale, angle 인자를 수정할 경우, 다시 scale, angle을 기준으로 이미지를 조정합니다. \n

        '''
        super(imageObj,self).__init__()
        self.frameTimer = RTimer(frameDuration,False) #프레임 타이머
        self._frame = 0
        self.mode = mode # 기본 애니메이션 모드 세팅은 루프를 하도록.
        self.sprites = [] #스프라이트들의 집합
        self.adjustByRect = False
        

        ##스프라이트 집합을 만든다.
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

        self._angle = 0
        self._scale = 1 
        self.angle = angle
        if scale != None:
            self.scale = scale
        self.pos = Rs.Point(pos)
        self.fromSprite = fromSprite
        if toSprite != None:
            self.toSprite = toSprite
        else:
            self.toSprite = len(self.sprites)-1
        if _rect!=None:
            self.rect = _rect
            self.adjustByRect = True       
        print(self.rect)
        if startFrame==None:
            self.frame = fromSprite # 스프라이트 현재 프레임. 시작 프레임에서부터 시작한다.
        else:
            self.frame = startFrame

        self.frameTimer.start()

    @property
    def rect(self):
        return super().rect
    
    @rect.setter
    def rect(self,_rect):
        '''
        rect를 조정할 경우, 다시 rect 기준으로 sprite를 조정합니다.
        '''
        self.adjustByRect=True
        imageObj.rect.fset(self,_rect)
    
    @property
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self,frame):
        if frame > self.toSprite:
            frame = self.fromSprite
        self._frame=frame
        self.graphic_n = self.sprites[self.frame]
        if self.adjustByRect:
            self.graphic = pygame.transform.smoothscale(self.graphic_n,(self.rect.w,self.rect.h))
        else:
            self.graphic = pygame.transform.rotozoom(self.graphic_n,self.angle,self.scale)
        self.frameTimer.reset()

    @property
    def scale(self):
        return super().scale
    
    @scale.setter
    def scale(self,_scale):
        '''
        scale을 조정할 경우, 다시 scale,angle 기준으로 sprite를 조정합니다.
        '''
        self.adjustByRect=False
        imageObj.scale.fset(self,_scale)

    @property
    def angle(self):
        return super().angle
    
    @angle.setter
    def angle(self,_angle):
        '''
        angle을 조정할 경우, 다시 scale,angle 기준으로 sprite를 조정합니다.
        '''
        self.adjustByRect=False
        imageObj.angle.fset(self,_angle)

    ##스프라이트 재생이 끝났는지 확인한다.
    #루프모드일 경우 항상 거짓 반환
    def isEnded(self):
        if self.mode == AnimationMode.PlayOnce and self.frame == self.toSprite:
            return True
        return False

    #스프라이트를 재생한다.
    def update(self):
        max = self.toSprite
            
        if self.frameTimer.isOver():
            if self.mode == AnimationMode.Looped:
                self.frame+=1
            else:
                if self.frame == max:
                    return
                else:
                    self.frame+=1

#spacing : 오브젝트간 간격
#pad : layout.pos와 첫 오브젝트간의 간격
class layoutObj(graphicObj):
    def __init__(self,rect=pygame.Rect(0,0,0,0),*,pos=None,spacing=10,childs=[],isVertical=True):
        '''
        그래픽 오브젝트를 일렬로 정렬하는 레이아웃 오브젝트입니다.
        childs[0] (depth 0)의 오브젝트들이 정렬됩니다.
        '''

        super().__init__()
        self.spacing = spacing
        self.pad = RPoint(0,0) ## 레이아웃 오프셋


        self.graphic_n = pygame.Surface((rect.w,rect.h),pygame.SRCALPHA,32).convert_alpha() # 빈 Surface
        self.graphic = self.graphic_n.copy()
        if pos==None:
            self.pos = RPoint(rect.x,rect.y)
        else:
            if type(pos)!=RPoint:
                self.pos = RPoint(pos[0],pos[1])
            else:
                self.pos = pos
        self.isVertical = isVertical

            
        for child in childs:
            child.setParent(self)
                    
        ##rect 지정이 안 되어 있을경우 자동으로 경계로 조정한다.
        if rect==pygame.Rect(0,0,0,0):
            self.adjustBoundary()
    
    def adjustBoundary(self):
        '''
        레이아웃의 경계를 차일드에 맞게 조정한다.
        '''
        self.graphic_n = pygame.Surface((self.boundary.w,self.boundary.h),pygame.SRCALPHA,32).convert_alpha() # 빈 Surface
        self.graphic = self.graphic_n.copy()



    #레이아웃 내부 객체들의 위치를 조정한다.
    def adjustLayout(self):
        if self.isVertical:
            def delta(c):
                d = c.rect.h
                return RPoint(0,d+self.spacing)
        else:
            def delta(c):
                d = c.rect.w
                return RPoint(d+self.spacing,0)

        lastChild = None
        for child in self.childs[0]:

            if lastChild != None:
                child.pos = lastChild.pos+delta(lastChild)
            else:
                child.pos = self.pad
            lastChild = child
        self._clearGraphicCache()

    ##레이아웃을 업데이트한다.
    # depths : 업데이트할 depth들을 지정한다. 기본값은 0
    def update(self,*,depths=[0]):
        for depth in depths:
            for child in self.childs[depth]:
                # child가 update function이 있을 경우 실행한다.
                if hasattr(child, 'update') and callable(getattr(child, 'update')):
                    child.update()



    def __getitem__(self, key):
        return self.childs[0][key]
    
    def __setitem__(self, key, value):
        self.childs[0][key] = value
        self.childs[0][key].setParent(self)

         
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
        '''
        font : 폰트 이름(.ttf로 끝나는 string)
        size : 폰트 사이즈
        color : 폰트 색상
        textWidth : 한 줄의 텍스트 길이
        alpha : 투명도
        '''
        if font==None:
            font = Rs.getDefaultFont("default")["font"]
        if size==None:
            size = Rs.getDefaultFont("default")["size"]
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
        super().__init__(pos=pos,childs=ObjList,spacing=size/4)
        self._clearGraphicCache()

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
    def __init__(self,_imgPath=None,_rect=None,*,pos=None,angle=0,scale=1,func=lambda:None,enabled=True,enableShadow=True):
        '''
        이미지를 버튼으로 활용하는 오브젝트
        '''

        super().__init__(_imgPath,_rect,pos=pos,angle=angle,scale=scale)
        self.hoverObj = Rs.copyImage(self) #마우스가 버튼 위에 있을 때 밝은 효과를 보여줄 이미지
        self.hoverObj.colorize(Cs.white,alpha=60)
        self.hoverObj.pos = RPoint(0,0)
        self.hoverObj.setParent(self,depth=0)
        self.enabled = enabled
        self.func = func
        
        if enableShadow:
            self.shadow = Rs.copyImage(self) #그림자 효과를 보여줄 이미지
            self.shadow.colorize(Cs.black,alpha=30)
            self.shadow.setParent(self,depth=-1)
            self.shadow.pos = RPoint(5,5)
        else:
            self.shadow = None

   #버튼을 누르면 실행될 함수를 등록한다.
    def connect(self,func):
        '''
        버튼을 눌렀을 때 실행될 함수를 등록한다.
        '''
        self.func = func

    def update(self):
        
        if self.enabled:
            if self.collideMouse():
                if Rs.userIsLeftClicking():
                    self.hideChilds(0) #마우스를 누르고 있을 때 밝은 효과를 숨긴다.
                else:
                    self.showChilds(0) #마우스가 버튼 위에 있을 때 밝은 효과를 보여준다.

                if Rs.userJustLeftClicked():
                    self.func() #마우스를 눌렀을 때 등록된 함수를 실행한다.
            else:
                self.hideChilds(0) # 마우스가 버튼 위에 없을 때 밝은 효과를 숨긴다.                    

            
class textButton(rectObj):
    def __init__(self,text:str="",rect:pygame.Rect=pygame.Rect(0,0,100,50),*,edge=1,radius=None,color=Cs.tiffanyBlue,
                 font:typing.Optional[str]=None,size:typing.Optional[int]=None,fontColor = Cs.white,
                 enabled=True,func=lambda:None,alpha=245):
        '''
        text: 버튼에 표시될 텍스트 \n
        rect: 버튼의 위치와 크기 \n
        edge: 버튼의 모서리 두께 \n
        radius: 버튼의 모서리 둥글기 \n
        color: 버튼의 색깔 \n
        font: 텍스트의 폰트 \n
        size: 텍스트의 크기 \n
        fontColor: 텍스트의 색깔 \n
        enabled: 버튼 활성화 여부 \n
        func: 버튼 클릭시 실행할 함수 \n
        alpha: 버튼의 투명도 \n
        '''

        if font==None:
            font = Rs.getDefaultFont("button")["font"]
        if size==None:
            size = Rs.getDefaultFont("button")["size"]


        ##텍스트 오브젝트 생성
        self.textObj = textObj(text,RPoint(0,0),font=font,size=size,color=fontColor) 
        
        ##텍스트 오브젝트의 크기에 따라 버튼의 크기를 조정
        rect.w = max(self.textObj.rect.w+20,rect.w)
        rect.h = max(self.textObj.rect.h+20,rect.h)
        super().__init__(rect,color=color,edge=edge,radius=radius)

        ##그림자 오브젝트 생성
        self.shadow = imageObj('rectShadow.png')
        self.shadow.alpha = 255
        self.shadow.rect = self.offsetRect.inflate(28,28)
        self.shadow.rect.midtop = self.offsetRect.midtop
        self.shadow.setParent(self,depth=-1)

        self.shadow1 = rectObj(self.offsetRect,color=Cs.black,radius=radius)
        self.shadow1.pos = RPoint(1,1)
        self.shadow1.alpha = 100
        self.shadow1.setParent(self,depth=-1)

        ##마우스가 버튼 위에 올라갔을 때의 효과를 위한 오브젝트 생성
        self.hoverRect = rectObj(self.offsetRect,color=Cs.white,radius=radius)
        self.hoverRect.alpha = 80
        self.hoverRect.setParent(self,depth=0)
        self.enabled = enabled
        if not self.enabled:
            self.hideChilds(0)

        self.func = func #clicked function
        self.alpha = alpha
        self.textObj.setParent(self,depth=1)
        self.textObj.center = self.offsetRect.center

    @property
    def text(self):
        return self.textObj.text
    @text.setter
    def text(self,text):
        self.textObj.text = text
        self.textObj.center = self.offsetRect.center

    @property
    def fontColor(self):
        return self.textObj.color

    @fontColor.setter
    def fontColor(self,color):
        self.textObj.color = color
        self._clearGraphicCache()

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,color):
        temp = copy.copy(self.rect)
        self._color = color
        self._makeRect(temp,color,self.edge,self.radius)
        self.hoverRect = rectObj(self.rect,color=Cs.white)
        self.hoverRect.alpha = 80

   #버튼을 누르면 실행될 함수를 등록한다.
    def connect(self,func):
        '''
        버튼을 눌렀을 때 실행될 함수를 등록한다.
        '''
        self.func = func

    def update(self):
        if self.enabled:
            if self.collideMouse():
                if Rs.userIsLeftClicking():
                    self.hideChilds(0) #마우스를 누르고 있을 때 밝은 효과를 숨긴다.
                else:
                    self.showChilds(0) #마우스가 버튼 위에 있을 때 밝은 효과를 보여준다.

                if Rs.userJustLeftClicked():
                    self.func()
            else:
                self.hideChilds(0) # 마우스가 버튼 위에 없을 때 밝은 효과를 숨긴다.                    



##실제로 대사를 한 글자씩 출력하기 위한 오브젝트.        
##npc의 대사 출력 등에 활용하면 좋다.
class textBubbleObj(longTextObj):
    def __init__(self,text="",pos=RPoint(0,0),*,font=None,size=None,color=Cs.white,textWidth=100,alpha=255, bgExist=True, bgColor = Cs.black, liveTimer=None,speed=2):
        '''
        NPC 대사 출력 등에 활용할 수 있는 말풍선 오브젝트. \n
        text : 대사 내용 \n
        pos : 대사 위치 \n
        font : 폰트 \n
        size : 폰트 사이즈 \n
        color : 폰트 색상 \n
        textWidth : 한 줄의 텍스트 길이 \n
        alpha : 투명도 \n
        bgExist : 말풍선 배경이 존재하는지 여부 \n
        bgColor : 말풍선 배경 색상 \n
        liveTimer : 말풍선 효과를 낼 경우, 해당 오브젝트가 살아있는 시간을 의미 \n

        일반적인 업데이트 함수 대신 .updateText() 함수를 통해 업데이트를 해주면 된다.
        
        '''
        super().__init__(text,pos=pos,font=font,size=size,color=color,textWidth=textWidth,alpha=alpha)
        self.fullBoundary = copy.copy(self.boundary) ## 텍스트가 전부 출력되었을 경우의 경계를 저장.
        self.fullSentence = self.text #전체 텍스트를 저장.
        self.text = ""
        self.speed = speed #텍스트를 읽어들이는 속도(프레임 단위)
        self.liveTimer = liveTimer ## 말풍선 효과를 낼 경우, 해당 오브젝트가 살아있는 시간을 의미
        
        if bgExist:
            self.bg = textButton("",self.fullBoundary.inflate(40,40),color=bgColor,enabled=False)
        else:
            self.bg = None

    ##대사 출력이 되고 있는지 확인한다.
    def isVisible(self):
        return self.liveTimer>0
        
    ##update 함수를 대체하는 함수.
    def updateText(self):
        if self.liveTimer!=None and self.liveTimer>0:
            super().update()
            i = len(self.text)
            temp = False
            if i < len(self.fullSentence):
                if self.liveTimer%self.speed==0:
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



##REMO Engine의 File I/O를 다루는 클래스.
##TODO: Path pipeline도 여기 안으로 옮긴다.

class REMODatabase:


    ##File Input/Output
    
    ##피클로 파이썬 객체를 저장한다. 보통 딕셔너리나 리스트 계열을 저장할때 사용
    @classmethod
    def saveData(cls,path,data):
        '''
        path : 저장할 파일의 경로\n
        data : 저장할 파이썬 객체(딕셔너리, 리스트 등)
        '''
        if os.path.isfile(path):
            control = 'wb'
        else:
            control = 'xb'
        pickle.dump(data,open(path,control))

    ##저장된 파이썬 객체를 불러온다.
    @classmethod
    def loadData(cls,path):
        '''
        path : 불러올 파일의 경로\n
        path에 저장된 파이썬 객체를 불러온다.
        '''
        return pickle.load(open(path,'rb'))
    


    ### 비주얼 노벨 계열 스크립트 파일 I/O 함수
    scriptPipeline ={}
    scriptExtension = '.scr'
    ##Script I/O

    ##.scr 파일은 텍스트 편집기를 통해서 간단하게 편집할 수 있습니다.
    ##.scr 파일의 문법은 별도의 파일에서 설명됩니다.
            
    ##현재 존재하는 .scr 파일을 묶어서 .scrs 파일로 만드는 함수.
    ##input을 통해 사용할 .scr파일을 지정할 수 있다. ['text1','text2'] 같은 식으로 쓰면 됨.
    ##{'text1.scr':*lines*, 'text2.scr':*lines*} 형식으로 파이프라인에 저장됨.
    ## prefix를 통해서 지정된 .scr 파일만 묶어서 저장할 수 있다. ex)GAME1_script1.scr GAME1_script2.scr
    ##        
    def zipScript(outputName,inputs=None,prefix=""):
        '''
        outputName : 저장할 .scrs 파일의 이름\n
        inputs : 묶을 .scr 파일의 이름 리스트(전체 파일들을 묶을 경우 None)\n
        prefix : 묶을 .scr 파일의 이름 중 특정 접두사를 가진 파일만 묶을 수 있음\n
        경로 내의 .scr 파일을 묶어서 .scrs 파일로 만든다.
        '''
        zipped = {}
        if inputs==None:
            current_directory = os.getcwd()
            script_files = [f for f in os.listdir(current_directory) if f.endswith(REMODatabase.scriptExtension) and prefix in f]
        else:
            script_files = [x+'.scr' for x in inputs]

        for f in script_files:
            file = open(f,'r',encoding='UTF-8')
            lines = file.readlines()
            lines = [l.strip() for l in lines if l.strip()!=""]
            zipped[f]=lines

        REMODatabase.saveData(outputName+REMODatabase.scriptExtension+'s',zipped)
        print(zipped)

        return zipped

    ##.scr 파일을 불러와 파이프라인에 저장한다.
    def loadScript(fileName):
        '''
        fileName : 불러올 .scr 파일의 이름\n
        '''
        if not fileName.endswith('.scr'):
            fileName += '.scr'
        file = open(fileName,'r',encoding='UTF-8')
        lines = file.readlines()
        REMODatabase.scriptPipeline[fileName] = lines


    ##.scrs 파일을 불러와 파이프라인에 저장한다.
    def loadScripts(fileName):
        '''
        fileName : 불러올 .scrs 파일의 이름\n
        '''
        if not fileName.endswith('.scrs'):
            fileName += '.scrs'
        path = Rs.getPath(fileName)
        REMODatabase.scriptPipeline.update(REMODatabase.loadData(path))


    ##.xlsx 파일을 불러와 dictionary의 list 형태로 저장한다.    
    def loadExcel(fileName,orient='index',indexNum=0):
        '''
        fileName : 불러올 .xlsx 파일의 이름\n
        orient: dictionary의 방향. 'index'로 지정할 경우 indexNum의 열을 key로 사용한다.\n
        'records'로 지정할 경우 각 시트를 dictionary list로 불러옵니다.\n
        '''
        path = Rs.getPath(fileName)
        excel_data = pandas.read_excel(path, None)  # None loads all sheets

        # Convert each sheet in the Excel file to a list of dictionaries
        sheets_dict = {}
        if orient=='records':
            for sheet_name, data in excel_data.items():
                sheets_dict[sheet_name] = data.to_dict(orient='records')
        elif orient=='index':
            for sheet_name, data in excel_data.items():
                # Assuming the first column is to be used as the key
                if not data.empty:
                    sheets_dict[sheet_name] = data.set_index(data.columns[indexNum]).to_dict(orient='index')
        else:
            raise ValueError("orient must be 'records' or 'index'")


        return sheets_dict


##스크립트 렌더링을 위한 레이아웃들을 저장하는 클래스.
class scriptRenderLayouts:
    layouts = {
        #1920*1080 스크린을 위한 기본 레이아웃.
        "default_1920_1080":
        {
            "name-rect":pygame.Rect(300,600,200,60), #이름이 들어갈 사각형 영역
            'name-alpha':200, #이름 영역의 배경 알파값. 입력하지 않을경우 불투명(255)
            "font":"korean_script.ttf", # 폰트. 기본으로 지원되는 한국어 폰트(맑은고딕). 영어 한국어 지원 가능
            "font-size":40, # 폰트 크기
            "script-rect":pygame.Rect(100,680,1700,380), ##스크립트가 들어갈 사각형 영역
            "script-pos":RPoint(200,710), ##스크립트 텍스트의 위치
            "script-text-width":1500, ##스크립트의 좌우 텍스트 최대길이
            "script-alpha":200 ## 스크립트 영역의 배경 알파값. 입력하지 않을경우 255(완전 불투명)
            ### 추가 옵션들
            ##"name-image":이름 영역의 이미지를 지정할 수 있습니다.
            ##"script-image" : 스크립트 영역의 이미지를 지정할 수 있습니다.
            ###
        }
        ##TODO: 유저 커스텀 레이아웃을 추가해 보세요. 네이밍 양식을 지켜서!
    }

    @classmethod
    def updateLayout(cls,name:str,layout:dict):
        '''
        name : 레이아웃의 이름\n
        layout : 레이아웃의 딕셔너리. 양식은 scriptRenderLayouts.layouts 참고\n
        '''
        cls.layouts[name] = layout


##작성한 비주얼노벨 스크립트를 화면에 그려주는 오브젝트 클래스.
class scriptRenderer():
    ##감정 벌룬 스프라이트(emotion-ballon.png)에 담겨진 감정의 순서를 나열한다.
    emotions = ["awkward","depressed","love","excited","joyful","angry","surprised","curious","sad","idea","ok","zzz","no"]
    emotionSpriteFile = "emotion-ballon.png" # 감정 벌룬 스프라이트의 파일 이름
    emotionTime = 1700 ##1700ms동안 감정 벌룬이 재생된다.


    ##렌더러를 초기화한다. (clear의 역할을 함)
    def _init(self):
        ##기본 이미지 초기화
        self.imageObjs = [] #화면에 출력될 이미지들
        self.charaObjs=[None,None,None] #화면에 출력될 캐릭터들
        self.moveInstructions = [[],[],[]] #캐릭터들의 움직임에 대한 지시문
        self.emotionObjs = [] # 화면에 출력될 (캐릭터의) 감정들
        self.emotionTimer = time.time() ## 감정 출력될 때 스크립트를 멈추는 타이머
        self.bgObj = rectObj(Rs.screen.get_rect(),color=Cs.black,radius=0) #배경 이미지
        self.nameObj = textButton()

        ##스크립트 텍스트 오브젝트
        self.scriptObj = longTextObj("",pos=self.layout["script-pos"],font=self.font,size=self.layout["font-size"],textWidth=self.layout["script-text-width"])

        self.frameTimer = RTimer(1000/60) ##프레임 타이머

    def clear(self):
        self._init()


    #textSpeed:값이 클수록 느리게 재생된다.
    def __init__(self,fileName,*,textSpeed:float = 5.0,layout="default_1920_1080",endFunc = lambda :None):
        '''
        textSpeed: 값이 클수록 느리게 재생된다.
        target_fps가 60보다 낮을 경우 캐릭터의 움직임이 느려질 수 있다.
        '''
        if not fileName.endswith('.scr'):
            fileName += '.scr'
        if fileName in REMODatabase.scriptPipeline:
            self.data = REMODatabase.scriptPipeline[fileName]
        else:
            raise Exception("script file:"+fileName+" not loaded. use method: REMODatabase.loadScripts")



        self.layout = scriptRenderLayouts.layouts[layout]
        self.index = 0
        self.font = self.layout["font"]
        
        self.currentScript = "" #현재 출력해야 되는 스크립트
        self.endFunc = endFunc #스크립트가 끝날 경우 실행되는 함수.

        self.textSpeed=textSpeed
        self.textFrameTimer = RTimer((1000/60)*self.textSpeed) ##텍스트 출력 속도를 조절하는 타이머

        self._init()

        self.endMarker = rectObj(pygame.Rect(0,0,7,10)) ##스크립트 재생이 끝났음을 알려주는 점멸 마커

        ##점멸을 위한 내부 인자들.
        self.endMarker.switch = True
        self.endMarker.timer = time.time()
        self.endMarker.tick = 0.5 ##0.5초마다 점멸 

        ##스크립트 영역 배경 오브젝트
        if "script-image" in self.layout:
            ##TODO: 이미지를 불러온다.
            self.scriptBgObj = imageButton(self.layout["script-image"],self.layout["script-rect"],hoverMode=False)
            None
        else:
            self.scriptBgObj = textButton("",self.layout["script-rect"],color=Cs.hexColor("111111"))
            self.scriptBgObj.hoverRect.alpha=5

        if "script-alpha" in self.layout:
            self.scriptBgObj.alpha = self.layout["script-alpha"]

        ##스크립트의 배경을 클릭하면, 다음 스크립트를 불러온다.
        def nextScript():
            if not self.scriptLoaded():
                self.scriptObj.text = self.currentScript
            elif not self.isEnded():
                ##다음 스크립트를 불러온다.
                self.index+=1
                self.updateScript()
                self.endMarker.switch = False
            else:
                ##파일의 재생이 끝남.
                self._init() ## 초기화(오브젝트를 비운다)
                self.endFunc()
                print("script is ended")

        self.scriptBgObj.connect(nextScript)
        self.updateScript()



    ##현 스크립트 재생이 끝났는지를 확인하는 함수
    def scriptLoaded(self):
        return self.scriptObj.text == self.currentScript

    ##전체 파일을 다 읽었는지 확인하는 함수.
    def isEnded(self):
        if self.index == len(self.data)-1:
            return True
        return False

    @property
    def currentLine(self):
        return self.data[self.index]
    
    ##렌더러의 폰트 변경.
    def setFont(self,font):
        self.scriptObj.font = font
        self.nameObj.textObj.font = font

    ##캐릭터에게 움직임을 지시한다.
    ##num:캐릭터 번호
    def makeMove(self,num,moves):
        moveInst = self.moveInstructions[num]
        for j,move in enumerate(moves):
            if j<len(moveInst):
                moveInst[j]=moveInst[j]+move
            else:
                moveInst.append(move)



    def updateScript(self):


        
        ### '#'태그 처리
        # #bgm -> 배경음악 설정. volume 인자가 있다.
        ## ex: '#bgm music.mp3 volume=0.7'
        # #sound -> 효과음 설정. volume 인자가 있다.
        ## ex: '#sound sound1.wav volume=0.3'
        # #bg -> 배경 설정
        ## ex: '#bg bg1.png'
        # #image -> 이미지를 설정한다. pos, scale 인자가 있다.
        ## ex: '#image Man1.png pos=RPoint(50,80) scale=1'
        # #clear -> (배경을 제외한)이미지들을 제거한다. '#clear' 만으로 작동.
        # #chara #chara1 #chara2 #chara3 -> 캐릭터를 설정한다. pos, scale 인자가 있으며, 파일명만 넣을 경우
        while self.currentLine[0]=="#":
            ##TODO: 블록 작성
            l = self.currentLine.split()
            tag = l[0] # tag : '#bgm','#bg','#image'같은 부분
            if tag=='#clear':
                ##이미지들을 지운다.
                self.imageObjs=[]
                self.charaObjs=[None,None,None]
                self.moveInstructions = [[],[],[]] ## 움직임 초기화
                self.index+=1
                continue

            fileName = None # 파일명
            parameters = {} # parameters : 태그와 파일명을 제외한 인자들.
            
            ##각 니블 분석
            #예를 들면, 'volume=1' 인자는 parameters에 {'volume':'1'}로 저장된다.
            for nibble in l[1:]:
                if '=' in nibble:
                    param_name,param_value = nibble.split("=")
                    parameters[param_name]=param_value
                else:
                    #'.'가 들어있는 니블은 파일명 ex)"test.png"
                    if '.' in nibble:
                        fileName = nibble
                    else: ##기타 명령어
                        if nibble=='jump': ##점프한다.
                            parameters['jump']=12



            ###태그 처리 분기문## 
            ##배경음악 재생
            if tag=='#bgm':
                if 'volume' in parameters:
                    _volume = float(parameters['volume'])
                else:
                    _volume = 1.0
                
                Rs.changeMusic(fileName,volume=_volume)
            ##효과음 재생                
            elif tag=='#sound':
                if 'volume' in parameters:
                    _volume = float(parameters['volume'])
                else:
                    _volume = 1.0
                
                Rs.playSound(fileName,volume=_volume)
            ##배경 교체
            elif tag=='#bg':
                self.bgObj = imageObj(fileName,Rs.screen.get_rect())

            ##캐릭터 관련 태그                
            elif '#chara' in tag: ## #chara1 #chara2 #chara3 #chara(=#chara1)
                if tag=='#chara':
                    num=0
                else:
                    num = int(tag[-1])-1
                if 'pos' in parameters:
                    _pos = eval(parameters['pos'])
                else:
                    _pos = RPoint(0,0)            
                if 'scale' in parameters:
                    _scale = float(parameters['scale'])
                else:
                    _scale = 1

                ##캐릭터 스프라이트 처리
                if fileName:
                    if self.charaObjs[num]:
                        self.charaObjs[num].setImage(fileName)
                    else:
                        self.charaObjs[num] = imageObj(fileName,pos=_pos,scale=_scale)

                ##감정 표현 처리
                if 'emotion' in parameters:
                    try:
                        emotion = parameters['emotion']
                        i = scriptRenderer.emotions.index(emotion)
                        e_pos = RPoint(self.charaObjs[num].rect.centerx,30)
                        Rs.playAnimation(scriptRenderer.emotionSpriteFile,stay=scriptRenderer.emotionTime,pos=e_pos,sheetMatrix=(13,8),fromSprite=8*i,toSprite=8*(i+1)-1,frameDuration=125,scale=2)
                        self.emotionTimer = time.time()+scriptRenderer.emotionTime/1000.0
                    except:

                        raise Exception("Emotion not Supported: "+emotion+", currently supported are:"+str(scriptRenderer.emotions))

                ##캐릭터 점프
                if 'jump' in parameters:

                    ##점프 지시를 넣는다.
                    j_pos = -int(parameters['jump'])
                    jumpInstruction = []
                    if j_pos>0:
                        d=-2
                    else:
                        d=2
                    temp = j_pos
                    sum = temp
                    while sum != 0:
                        jumpInstruction.append(RPoint(0,temp))
                        temp+=d
                        sum += temp                        
                    jumpInstruction.append(RPoint(0,temp))

                    self.makeMove(num,jumpInstruction)
                
                ##캐릭터 수평이동
                if 'move' in parameters:
                    m_pos = int(parameters['move'])
                    moveInstruction = []
                    temp = m_pos
                    while temp!=0:
                        if abs(temp)<=2:
                            d = temp
                        else:
                            d =temp*0.05
                            if 0<d<1:
                                d=1
                            elif -1<d<0:
                                d=-1
                            d= int(d)
                        temp-=d
                        moveInstruction.append(RPoint(d,0))
                    
                    self.makeMove(num,moveInstruction)



            elif tag=='#image':
                if 'pos' in parameters:
                    _pos = eval(parameters['pos'])
                else:
                    _pos = RPoint(0,0)
            
                if 'scale' in parameters:
                    _scale = float(parameters['scale'])
                else:
                    _scale = 1

                obj = imageObj(fileName,pos=_pos,scale=_scale)
                self.imageObjs.append(obj)
            else:
                raise Exception("Tag Not Supported, please check the script file(.scr): "+self.currentLine)
            ###

            if self.index == len(self.data)-1:
                return
            self.index+=1

        ##스크립트 처리##
        ##ex: '민혁: 너는 왜 그렇게 생각해?'
        if ":" in self.currentLine:
            name,script = self.currentLine.split(":")
            script = script.strip()

            self.nameObj = textButton(name,rect=self.layout["name-rect"],font=self.font,size=self.layout['font-size'],enabled=False,color=Cs.hexColor("222222"))
            if "name-alpha" in self.layout:
                self.nameObj.alpha = self.layout["name-alpha"]
            self.currentScript = script
        else:
            self.nameObj.textObj.text = ""
            self.currentScript = self.currentLine.strip()
        self.scriptObj.text=""




        
    def update(self):
        '''
        함수가 복잡하므로 이 함수 실행 전에 Rs.acquireDrawLock()을 통해 락을 걸어주는 것이 좋다.
        '''

        ##캐릭터의 움직임 업데이트
        if self.frameTimer.isOver():
            for i,moveInst in enumerate(self.moveInstructions):
                if moveInst != []:
                    move = moveInst.pop(0)
                    self.charaObjs[i].pos += move
            self.frameTimer.reset()


        ##감정 애니메이션이 재생중일 땐 스크립트를 재생하지 않는다.
        if self.emotionTimer>time.time():
            if self.scriptObj.text != "":
                self.scriptObj.text = ""
            return

        self.scriptBgObj.update()

        #Script를 화면에 읽어들이는 함수.
        if self.textFrameTimer.isOver():
            temp = False
            if not self.scriptLoaded():
                ##미세조정: 스크립트가 위아래로 왔다리 갔다리 하는 것을 막기 위한 조정임.
                i = len(self.scriptObj.text)
                fullText = self.currentScript
                while i < len(fullText) and fullText[i] != " ":
                    i+=1
                parsedText = fullText[:i]
                l1 = self.scriptObj.getStringList(self.scriptObj.text)[:-1]
                l2 = self.scriptObj.getStringList(parsedText)[:-1]
                try:
                    while len(l1[-1]) > len(l2[-1]):
                        self.scriptObj.text = self.currentScript[:len(self.scriptObj.text)+1]
                        l1 = self.scriptObj.getStringList(self.scriptObj.text)[:-1]
                        temp = True
                except:
                    pass
                if not temp:
                    self.scriptObj.text = self.currentScript[:len(self.scriptObj.text)+1]
            self.textFrameTimer.reset()

        ##점멸 마커 업데이트
        if self.scriptLoaded():
            ##점멸 표시
            if time.time()>self.endMarker.timer:
                self.endMarker.timer = time.time()+self.endMarker.tick 
                self.endMarker.switch = not self.endMarker.switch
            
            markerPos = RPoint(self.scriptObj.childs[0][-1].geometry.bottomright)+RPoint(20,0)
            if self.endMarker.bottomleft != markerPos:
                self.endMarker.bottomleft = markerPos




    def draw(self):
        self.bgObj.draw()
        for imageObj in self.imageObjs:
            imageObj.draw()
        for chara in self.charaObjs:
            if chara:
                chara.draw()
        self.scriptBgObj.draw()
        self.scriptObj.draw()
        if self.scriptLoaded() and self.endMarker.switch:
            self.endMarker.draw()
        if self.nameObj.textObj.text!="":
            self.nameObj.draw()
            self.nameObj.textObj.draw()
        for emotion in self.emotionObjs:
            emotion.draw()







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
        super().__init__(rect=pygame.Rect(pos.x,pos.y,0,0),spacing=spacing[1],childs=temp)
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
            rect = pygame.Rect(pos.x,pos.y,thickness,length)
        else:
            rect = pygame.Rect(pos.x,pos.y,length,thickness)

        super().__init__(rect,color=Cs.dark(color)) ## BUG


        self.gauge = rectObj(rect,color=color) # 슬라이더 바의 차오른 정도 표현 (게이지)
        self.gauge.setParent(self)        
        self.button = rectObj(pygame.Rect(0,0,thickness*2,thickness*2),color=color) # 슬라이더 바의 버튼
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

    def update(self):
        ## 이 부분 dragEventHandler로 처리 할 수 있을듯 하다.
        if Rs.userJustLeftClicked() and (self.collideMouse() or self.button.collideMouse()):
            Rs.draggedObj = self
        if Rs.userIsLeftClicking() and Rs.draggedObj == self:
            if self.isVertical:
                d = Rs.mousePos().y-self.geometryPos.y
            else:
                d = Rs.mousePos().x-self.geometryPos.x
            d /= float(self.length)
            d = max(0,d)
            d = min(1,d)
            self.value = d
            self.adjustObj()
            self.__function()

        None
        
        
class buttonLayout(layoutObj):
    '''
    버튼들을 간편하게 생성할 수 있는 버튼용 레이아웃 \n
    example: buttonLayout(["Play Game","Config","Exit"],RPoint(50,50))    
    '''
    def __init__(self,buttonNames=[],pos=RPoint(0,0),*,spacing=10,
                 isVertical=True,buttonSize=RPoint(200,50),buttonColor = Cs.tiffanyBlue,
                 fontSize=None,fontColor=Cs.white,font="korean_button.ttf",
                 buttonAlpha=225):
        self.buttons = {}
        buttonSize = Rs.Point(buttonSize)
        buttonRect = pygame.Rect(0,0,buttonSize.x,buttonSize.y)
        for name in buttonNames:
            self.buttons[name]=textButton(name,buttonRect,font=font,size=fontSize,color=buttonColor,fontColor=fontColor,alpha=buttonAlpha)            
            setattr(self,name,self.buttons[name])
        super().__init__(pos=pos,spacing=spacing,isVertical=isVertical,childs=list(self.buttons.values()))
    def __getitem__(self,key) -> textButton:
        return self.buttons[key]
    def __setitem__(self, key, value):
        if key in self.buttons:
            self.buttons[key].setParent(None)
        self.buttons[key]=value
        self.buttons[key].setParent(self)
        self.adjustLayout()
    def __getattr__(self, key) -> typing.Union[textButton,typing.Any]:
        '''
        버튼을 객체의 속성처럼 접근할 수 있게 해준다.
        띄어쓰기가 존재할 경우 _로 대체하여 쓰면 된다.
        '''
        key = key.replace('_', ' ')  # 키에서 _를 띄어쓰기로 변환
        try:
            # 다른 속성에 접근할 수 없는 경우에만 데이터 딕셔너리에서 찾기
            return self.__dict__[key]
        except KeyError:
            # 속성으로 접근할 수 없을 경우, 데이터 딕셔너리에서 찾기
            key = key.replace('_', ' ')  # 속성 이름에 _를 띄어쓰기로 변환 (선택사항)
            if key in self.buttons:
                return self.buttons[key]
            raise AttributeError(f"'{self.__class__.__name__}' object has no button '{key}'")        




class scrollLayout(layoutObj):
    scrollbar_offset = 10 # 스크롤바의 오프셋
    '''
    스크롤이 가능한 레이아웃입니다.
    '''

    def getScrollbarPos(self):
        if self.isVertical:
            s_pos = RPoint(self.rect.w+2*self.scrollBar.thickness,scrollLayout.scrollbar_offset)            
        else:
            s_pos = RPoint(scrollLayout.scrollbar_offset,self.rect.h+2*self.scrollBar.thickness)
        return s_pos

    def __init__(self,rect=pygame.Rect(0,0,0,0),*,spacing=10,pad=10,childs=[],isVertical=True,scrollColor = Cs.white,isViewport=True):
        '''
        spacing: 차일드 사이의 간격\n
        isVertical: 수직 스크롤인지 수평 스크롤인지\n
        scrollColor: 스크롤바의 색깔\n
        isViewport: 뷰포트로 설정할지 여부\n
        뷰포트로 설정시 rect 영역 안쪽만 그려집니다.\n
        pad : 스크롤 레이아웃의 패딩값입니다. 스크롤로 조절되지 않는 축의 패딩값입니다.\n
        '''

        super().__init__(rect=rect,spacing=spacing,childs=childs,isVertical=isVertical)
        if self.isVertical:
            self.pad = RPoint(pad,0)
        else:
            self.pad = RPoint(0,pad)

        self.setAsViewport(isViewport)
        if isVertical:
            s_length = self.rect.h
        else:
            s_length = self.rect.w
        self.scrollBar = sliderObj(pos=RPoint(0,0),length=s_length-2*scrollLayout.scrollbar_offset,isVertical=isVertical,color=scrollColor) ##스크롤바 오브젝트

        self.scrollBar.setParent(self,depth=1) ##스크롤바는 레이아웃의 뎁스 1 자식으로 설정됩니다.
        self.scrollBar.pos =self.getScrollbarPos()

        ##스크롤바를 조작했을 때 레이아웃을 조정합니다.
        def __ScrollHandle():
            if self.isVertical:
                l = -self.getBoundary().h+self.rect.h
                self.pad = RPoint(self.pad.x,self.scrollBar.value*l)
                self.adjustLayout()
            else:
                l = -self.getBoundary().w+self.rect.w
                self.pad = RPoint(self.scrollBar.value*l,self.pad.y)
                self.adjustLayout()
        self.scrollBar.connect(__ScrollHandle)

    def collideMouse(self):
        return self.geometry.collidepoint(Rs.mousePos().toTuple())

    def update(self):

        ##마우스 클릭에 대한 업데이트
        for child in self.childs[0]:
            # child가 update function이 있을 경우 실행한다.
            if hasattr(child, 'update') and callable(getattr(child, 'update')):
                child.update()
        
        ##스크롤바에 대한 업데이트
        self.scrollBar.update()


        return




##다이얼로그 창을 나타내는 오브젝트
##버튼이 달려있는 팝업창이다.
class dialogObj(rectObj):
    def __init__(self,rect,title="",content="",buttons=[],*,radius=10,edge=1,color=Cs.black,alpha=255,
                 font="korean_button.ttf",title_size=40,content_size=30,fontColor=Cs.white,
                 spacing=20,buttonSize=(200,50)):
        '''
        dialogObj는 다이얼로그 창을 나타내는 오브젝트입니다.\n
        color: 팝업창의 색깔입니다.\n
        title_size: 제목의 폰트 크기입니다.\n
        content_size: 내용의 폰트 크기입니다.\n
        spacing : 제목과 내용 사이의 간격입니다.\n
        title은 비울 수 있습니다.\n
        '''
        super().__init__(rect,color=color,alpha=alpha,radius=radius,edge=edge)
        #TODO: title, content, buttons 선언

        if title!="":
            self.title = textObj(title,pos=(spacing,spacing),size=title_size,font=font,color=fontColor)
            self.content = longTextObj(content,pos=(spacing,spacing*2+self.title.rect.height),size=content_size,font=font,color=fontColor,textWidth=rect.w-2*spacing)
            self.title.setParent(self)
            self.title.centerx = rect.w//2
        else:
            self.title=None
            self.content = longTextObj(content,pos=(spacing,spacing*2),size=content_size,font=font,color=fontColor,textWidth=rect.w-2*spacing)

        self.buttons = buttonLayout(buttons,pos=RPoint(0,0),fontSize=30,buttonSize=buttonSize,spacing=10,fontColor=fontColor,buttonColor=Cs.light(color),isVertical=False)
        self.content.centerx = rect.w//2
        self.buttons.midbottom = (rect.w//2,rect.h-spacing)

        self.content.setParent(self)
        self.buttons.setParent(self)

        self.buttons.update()

    def update(self):
        self.buttons.update()
        return

    def __getitem__(self,key):
        return self.buttons[key]
    def __setitem__(self, key, value):
        self.buttons[key]=value

    def show(self):
        '''
        다이얼로그 창을 화면에 띄웁니다.
        '''
        Rs.addPopup(self)
    def hide(self):
        '''
        다이얼로그 창을 화면에서 숨깁니다.
        '''
        Rs.removePopup(self)

    def isShown(self):
        '''
        다이얼로그 창이 화면에 띄워져 있는지 확인합니다.
        '''
        return Rs.isPopup(self)

                



class safeInt:
    bigNumber = 2147483648
    '''
    안전한 정수형 클래스입니다.
    실제 값을 저장하지 않으며 getter에서만 반환됩니다.
    '''

    def __makeOffset(self):
        return random.randint(-safeInt.bigNumber,safeInt.bigNumber)

    def __init__(self,value:int):
        self.__m = self.__makeOffset()
        self.__n = value - self.__m
        print(self.__m,self.__n)

    @property
    def value(self):
        return self.__m + self.__n
    
    @value.setter
    def value(self,value):
        self.__m = self.__makeOffset()
        self.__n = value - self.__m

    def __add__(self,other):
        return safeInt(self.value+other)
    def __sub__(self,other):
        return safeInt(self.value-other)
    def __mul__(self,other):
        return safeInt(self.value*other)
    def __truediv__(self,other):
        return safeInt(self.value//other)
    def __str__(self):
        return str(self.value)
    def __int__(self):
        return self.value
    def __float__(self):
        return float(self.value)
    def __repr__(self) -> str:
        return "safeInt({0})".format(str(self.value))