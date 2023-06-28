from model import Stockfish
import chess
from REMOLib import *



stockFishPath = "stockfish-windows-2022-x86-64-avx2.exe"

talkScript = {
    'greeting': ['it\'s a nice day, sir.',
                 'Hello, sir, How are you today?',
                 'Good day to you, sir.',
                 'Greetings, dear sir. It\'s a pleasure to see you today.',
                 "Good afternoon, sir. I hope you're doing well today.",
                 "It's lovely to see you today, sir.",
                 "Greetings, sir. I trust you're having a good day so far.",
                 "It's always a pleasure to see you, sir.",
                 "It's wonderful to have you here today, sir."                 
                 ],
    'praise':['nice job, sir.',
              "Excellent move, sir!",
              "Impressive move, sir!",
              "That's a good idea, sir!",
              "You have a talent for this, sir.",
              "I'm impressed by your play, sir.",
              "Well played, sir.",
              "You have a good sense of the game, sir.",
              "Your courage impresses me.",
              "Well played, even in the face of a challenge.",
              "This game just got more exciting.",
              "You have a real talent for this game.",
              "I'm curious to see how it unfolds.",
              "Your move has caught my attention, sir.",
              "You keep the game fascinating, sir.",
              "You always bring an interesting twist to the game, sir.",
              "I appreciate your unique approach to the match, sir.",
              ],
    'blunder':["Don't worry, sir. we all make mistakes.",
               "No problem, sir. Keep playing.",
               "It's okay, sir. Let's keep going.",
               "You'll get it next time, sir.",
               "That move may not be the best option, sir.",
               "I think there might be a better option, sir.",
               "Perhaps you could try a different move, sir.",
               "We're here to have fun, after all.",
               "You're certainly keeping me entertained.",
               "Don't worry, it happens to the best of us.",
               "Looks like the chess pieces have a mind of their own today.",
               "Interesting... choice!",
               "I didn't see that one coming at all.",
               "It's a game-changer, no doubt about it.",
               "I'm in awe... of your skill, Sir.",
               "Your strategic brill...iance knows no bounds!",
               "Your brilliant move leaves me in awe... of your creativity.",
               "Can I call you the Chess Wizard, sir?"
               ],
    'talking':["Spending time with you is always a pleasure, sir.",
               "I always look forward to seeing you, sir.",
               "I'm grateful for your friendship, sir.",
               "Take care of yourself, sir. Your health and well-being are important.",
               "Chess can teach you how to anticipate your opponent's moves, sir.",
               "Chess can enhance your concentration and focus, sir.",
               "I always enjoy spending time with you, sir.",
               "I appreciate your presence, sir.",
               "Being with you is always a delight, sir.",
               "It's always a joy to spend time with you, sir.",
               "The weather is beautiful today, sir.",
               "It's such a lovely day, sir.",
               "The sun is shining so brightly, sir.",
               "It's a great day for some friendly competition, sir.",
               "The weather is perfect for a game, sir.",
               "The beautiful day makes for our chess game, sir.",
               "My heart longs for your presence, sir.",               
               ],
    'newgame':["Let's enjoy a game together, sir.",
               "I'm eager to start the game, sir.",
               "Shall we begin the game, sir?"
               ],
    'mate':["I'm sorry to say, sir, but it looks like I have won this match."],
    'shy':['...Where are you watching, sir?',
           "...I didn't know that you are interested in my feminine parts...",
           "...I see your eager face...",
           "...May I know what is on your mind,sir...?",
           "...Is there anything you would like to talk about, sir?",
           "...You look excited, sir.",
           "...You seem enthusiastic about this, sir."],
    'thinking':['Hmmmm.........',
                'Let me see, sir...',
                'Ummmm........',
                "Hmm, okay...",
                "Hmm, I see...",
                "Let me think...",
                "Hmm, interesting...",
                "Well, possibly..."
                ],
    'undo-ok':['Well... Ok, sir, just this once.',
               "I'll permit it this time, sir.",
               "Alright, sir, but just this once.",
               "Well, for this time only, sir.",
               "Well, as a special case, sir.",
               "I'll grant your request this time, sir.",
               "I'll allow it just this once, sir."],
    'undo-reject':["No, sir, I wouldn't let you do that.",
                   "I'm afraid that wouldn't be appropriate, sir.",
                   "I can't allow that, sir.",
                   "I'm sorry, sir, but that's against the rules.",
                   "I can't let you do that, sir.",
                   "I'm sorry, sir, but I can't agree to that.",
                   "I'm afraid I have to say no, sir.",
                   "That's not something I can allow, sir."
                   ],
    'hint-ok':["I think # would be a good option, sir.",
               "Have you considered #, sir?",
               "Perhaps # would be a good idea, sir.",
               "I suggest you consider #, sir."],
    'hint-reject':["It's crucial to think independently in chess, sir.",
                   "You must learn to think for yourself in chess, sir.",
                   "In chess, following your own intuition is often the best approach, sir.",
                   "Thinking by yourself is essential to improving your chess skills, sir.",
                   "Just a moment, sir. Let me gather my thoughts.",
                   "Allow me a second, sir. I'm considering about it.",
                   "I need a moment to think, sir. Please bear with me.",
                   "I'm taking a moment to think, sir."                   
                   ],
    'hint-disabled':["You'll have to solve this one without my help, sir.",
                     "I'm afraid I can't give you any more hints, sir.",
                     "It's up to you to figure out the next move, sir.",
                     "I believe you can do this without any more hints, sir."],
    'conversation':["My family name is Bongcloud, sir. You can call me Charlotte.",
                   "The Bongcloud opening has been passed down in my family for centuries, sir.",
                   "In my family, the Bongcloud opening is considered a sacred chess move.",
                   "I hope you're having a pleasant day, sir.",
                   "I trust you're having a good day, sir.",
                   "It is my pleasure to serve you, sir.",
                   "I feel so lucky to be spending this beautiful day with you, sir.",
                   "Sir, I couldn't imagine a more perfect day to be with you.",
                   "Sir, The beauty of this day pales in comparison to the joy you bring me.",
                   "I'm happy to provide guidance, sir, but I don't want to give you too much help.",
                   "Hints are good, but not too many, sir.",
                   "You bring light to my life, sir.",
                   "Every moment with you is precious, sir.",
                   "I feel so lucky to have you in my life, sir.",
                   "You make my world a better place, sir.",
                   "Do you understand the beauty of the Bongcloud opening?",
                   "The Bongcloud opening requires boldness and creativity, sir.",
                   "The Bongcloud opening can add excitement and unpredictability to your game, sir.",
                   "Thank you for playing with me, Mister. I hope we have a great match.",
                   "I'm excited to play against you, Sir. May the best player win!",
                   "Enjoy the game, Sir. Let's give our best.",
                   "May this game bring you joy, Sir. Let's both give our absolute best.",
                   "Believe in yourself, Sir, for you are capable of great things.",
                   "Take heart, Sir, for brighter days await.",
                   "In this game and beyond, Sir, you're destined for greatness.",
                   "You have the potential, Sir. Turn the game in your favor!",
                   "Trust your abilities, Sir.",
                   "Believe in yourself, Sir.",
                   "Sir, the chessboard is your canvas. Paint it with your brilliance!",
                   "Keep your chin up, Sir.",
                   "Embrace hope, Sir.",
                   "With each move, Sir, you demonstrate your skill and determination.",                                                                          
                    "Spending time with you is all I desire, sir.",
                    "My happiness is being with you, sir.",
                    "I feel complete when I'm with you, sir.",
                    "You're my favorite place to be, sir.",
                    "You're my sunshine in a world of gray, sir.",
                    "Being near you is pure happiness, sir.",
                    "With you, I've found where I belong, sir."

                   ],
    'costume':["Well, sir, do you find this attire more to your liking?",
               "I have altered my garments, sir. I hope it meets your discerning taste.",
               "Kindly appraise this new attire, sir.",
               "Do you prefer this outfit, sir?",
               "Is this attire satisfactory, sir?",
               "How do you find this attire, sir?",
               "Is this what you had in mind, sir?",
               "Do you approve of this change, sir?",
               "Does this suit your taste, sir?",
               "Is this attire satisfactory, sir?",
               "Is this new outfit pleasing, sir?",
               "I hope this pleases you, sir."
    ],
    'swap':["Sir. I shall play your side, and you mine.",
            "Sir. I shall adopt your side, offering us a novel chess experience.",
            "It invites us to adapt and think differently.",
            "It adds an interesting twist to the game.",
            "It adds a touch of excitement, doesn't it?",                                                
            ]
}
game_geometry_n = {
    'lady':{'Pos':RPoint(1250,0),'Scale':0.7,'Hand':1.0,'breasts':pygame.Rect(1400,530,270,150)},   
    'board':{'TileSize':100,'Pos':RPoint(100,60),'MyDeadPos':pygame.Rect(880,940,0,0),'HerDeadPos':pygame.Rect(920,80,0,0)},
    'talk':{'Pos':RPoint(1100,200),'TextSize':20,'TextWidth':350},
    'chessTable': {'Pos':RPoint(600,600),'Scale':1.0},
    'button':{'button1':pygame.Rect(0,0,200,50),'button2':pygame.Rect(0,0,400,50),'button3':pygame.Rect(0,0,100,50),'pos1':RPoint(1000,300),'pos2':RPoint(1350,750),'pos3':RPoint(1600,800),'talkButton':pygame.Rect(1260,250,100,100),'pgn':RPoint(940,820)},
    'sys':{'FontSize':13,'ButtonFontSize':25,},
    'credit':{'Pos':RPoint(1000,400),'Button':pygame.Rect(1600,100,100,50)}
}


##게임의 저작권을 설명하는 크레딧
##출시 후에는 제데로 된 링크로 바꾸어야 한다.
credit = """
The game's source code is opened for request under GNU GENERAL PUBLIC LICENSE Version 3 (GPL v3).
Steamworks SDK is not linked with the whole code.
The game uses stockfish (Open  Source Chess Engine) and python-chess library.
the github source code link is https://github.com/Dano-Sato/Play-Chess-with-Lady-Bongcloud. current bgm is """

##음악 저작권을 설명하는 크레딧
musicCredits = {
    "peaceful.mp3":"""Sunset Landscape by Keys of Moon | https://soundcloud.com/keysofmoon
Creative Commons CC BY 4.0
    """,
    "Nighttime-Stroll.mp3":"""Nighttime Stroll by Artificial.Music | https://soundcloud.com/artificial-music/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/
    """,
    "Sakuya.mp3":""" Sakuya by PeriTune | https://peritune.com/
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/4.0/
"""    
}

musicSheet = {"Calm":'peaceful.mp3',"Jazz":"Nighttime-Stroll.mp3","Japan":"Sakuya.mp3"}
costumeSheet = {"Normal":"lady_bongcloud.png","Bunny":"lady_bongcloud_bunny.png","Beast":"lady_bongcloud_beast.png"}
modeSheet = {"FullScreen":True,"Window":False}
musicVolumeSheet = {"Japan":0.2} #음량 조절용 시트

default_screen_size = (1920,1080)
window =Rs.new(REMOGame)

class Obj():
    stockfish = Stockfish(path=stockFishPath,parameters={"Threads":4})
    game_geometry = copy.deepcopy(game_geometry_n)
    board = chess.Board()
    thinkOfAI = ""
    think = 'chessgame-ai.think'
    hint = 'chessgame-ai.hint'
    configPath = 'chessgame.config'
    default_config = {"Resolution":1920,"FullScreen":"FullScreen","Music":"Calm","Costume":"Normal","UserIsWhite":False,"Swapped":False,"Volume":1.0,"HintCount":0,"Board":chess.Board(),"PGN":""} # config 정보를 저장
    config = {}
    AIcondition = 0.3
    hintCountMax = 4
    pieceVolume={"P":0.2,"N":0.5,"B":0.5,"R":0.7,"Q":1} ## 피스가 죽을 때 내는 볼륨
    heart = "♥"
    emptyHeart = "♡"
    cursor = Rs.new(imageObj)
    
    @classmethod
    def renewCondition(cls):
        Obj.AIcondition = random.random()*0.6
        
    ###왕은 되돌아가서는 안된다.
    ##왕이 원래자리로 되돌아가는지 체크하는 함수
    @classmethod
    def checkKingBack(cls,b,move):
        s = move[:2]
        e = move[2:4]
        if str(b.piece_at(chess.parse_square(s))).upper()=="K" and e in ["e1","e8"]:
            return True
        return False        
        
                
        
        
    

def updateGeoAndOpenGame():
    r = Obj.config["Resolution"]/1920.0
    fullScreen = modeSheet[Obj.config["FullScreen"]]
    Obj.game_geometry = {}
    for key in list(game_geometry_n):
        Obj.game_geometry[key]={}
        for attr in list(game_geometry_n[key]):
            if type(game_geometry_n[key][attr])==tuple:
                x,y = game_geometry_n[key][attr]            
                Obj.game_geometry[key][attr]=(int(x*r),int(y*r))
            elif type(game_geometry_n[key][attr])==RPoint:
                Obj.game_geometry[key][attr]=game_geometry_n[key][attr]*r
            elif type(game_geometry_n[key][attr])==pygame.Rect:
                x,y,w,h = game_geometry_n[key][attr]
                Obj.game_geometry[key][attr]=pygame.Rect(int(x*r),int(y*r),int(w*r),int(h*r))
            elif type(game_geometry_n[key][attr])==int:
                Obj.game_geometry[key][attr] = int(game_geometry_n[key][attr]*r)
            else:
                Obj.game_geometry[key][attr] = game_geometry_n[key][attr]*r
    adder = int(5/r)
    Obj.game_geometry['sys']['FontSize'] += adder
    Obj.game_geometry['sys']['ButtonFontSize'] += adder//2
    Obj.game_geometry['talk']['TextSize']+=adder
    Rs.setSysFont(size=Obj.game_geometry['sys']['FontSize'],buttonFontSize=Obj.game_geometry['sys']['ButtonFontSize'])
    w,h = default_screen_size

    #pygame.display.quit()
    if REMOGame.gameStarted():
        REMOGame.exit()
 
    screen_size = (int(w*r),int(h*r))

    window = REMOGame(screen_size,fullScreen,caption="Play Chess with Lady Bongcloud")
    REMOGame.setCurrentScene(Scenes.mainScene)
    window.run()
    
def stockFishHintProcess(fen,path):
    stockfish = Obj.stockfish
    c = random.randint(3000,3500)
    stockfish.set_elo_rating(c)
    stockfish.set_fen_position(fen)
    l = stockfish.get_top_moves(3)
    if len(l)>0:
        bestMove = l[0]
        makeAIHintData(bestMove["Move"],fen,path=Obj.hint)
                
def stockFishProcess(time,fen,path,bongcloudOpened,isBestMode):
    color = fen.split(' ')[1]
    if color == 'b':
        def moveFilter(x):
            if x["Centipawn"]==None:
                return False
            return -300 < x["Centipawn"] < 100
    else:
        def moveFilter(x):
            if x["Centipawn"]==None:
                return False
            return -100 < x["Centipawn"] < 300
    stockfish = Obj.stockfish
    if random.random()>0.3:
        stockfish.set_elo_rating(3000)
    else: # Dojitko Move
        stockfish.set_elo_rating(Obj.AIcondition)
    stockfish.set_fen_position(fen)
    
    eval = stockfish.get_evaluation()
    tMoves = stockfish.get_top_moves(5)
    tMoves = tMoves[::-1]
    move = ""

    b = chess.Board(fen)
    ##봉클라우드를 위해 킹이 되돌아가는 무브를 제거한다.
    _topMoves=[]
    if len(tMoves)>1:
        for move in tMoves:
            m = move["Move"]
            s = m[:2]
            e = m[2:4]
            if str(b.piece_at(chess.parse_square(s))).upper()=="K" and e in ["e1","e8"]:
                continue
            else:
                _topMoves.append(move)
    else:
        move = tMoves[-1] # Make Best Move
        makeAIData(move,eval=eval,topMoves=_topMoves)
        return
    
    if isBestMode:
        move = _topMoves[-1] # Make Best Move
        makeAIData(move,eval=eval,topMoves=_topMoves)
        return
    
    #Pawn opening for bongcloud
    if not bongcloudOpened:
        bongcloud_pawn_moves = ['d2d3','d2d4','e2e3','e2e4','f2f3','f2f4','d7d6','d7d5','e7e6','e7e5','f7f6','f7f5']
        b = chess.Board(fen)
        l = [str(x) for x in list(b.legal_moves)] # legal moves
        kingMoves = filter(lambda x:'e1' in x or 'e8' in x,l) # legal moves that king can move
        ev = []
        for move in kingMoves:
            if move[2:4] in ["e1","e8"]:
                continue
            b = chess.Board(fen)
            b.push_san(move)
            stockfish.set_fen_position(b.fen())
            if -400<stockfish.get_evaluation()['value']<400: #moderate
                ev.append([move,stockfish.get_evaluation()["value"]])
        
        if ev==[]:
            ev = [] # Evaluation of bongcloud move
            
            random.shuffle(bongcloud_pawn_moves)

            for move in bongcloud_pawn_moves:
                if move in l:
                    b = chess.Board(fen)
                    b.push_san(move)
                    stockfish.set_fen_position(b.fen())
                    if color=='w':
                        if -200<stockfish.get_evaluation()['value']: #moderate move
                            ev.append([move,stockfish.get_evaluation()["value"]])
                        break
                    else:
                        if stockfish.get_evaluation()['value']<200: #moderate move
                            ev.append([move,stockfish.get_evaluation()["value"]])
                        break
                    
        rlist = []
        for e in ev:
            _move = e[0]
            if _move[2:4] in["e1","e8"]:
                rlist.append(e)
        for r in rlist:
            ev.remove(r)
        if len(ev)>0:
            _move,cp = random.choice(ev)
            makeAIData({"Move":_move,"Centipawn":cp,'Mate':None},eval=eval,topMoves=_topMoves)        
            return

        
    moderate_moves = list(filter(moveFilter,_topMoves))
    if len(moderate_moves)>0:
        move = random.choice(moderate_moves)
    if type(move)==str:
        move = _topMoves[-1]
    if move not in _topMoves:
        move = _topMoves[-1]
    makeAIData(move,eval=eval,topMoves=_topMoves)
    
def makeAIData(move="",*,eval="",topMoves="",path=Obj.think):
    if os.path.isfile(path):
        control = 'wb'
    else:
        control = 'xb'
    pickle.dump({"Move":move,'Time':time.time(),"Eval":eval,"TopMoves":topMoves},open(path,control))

def makeAIHintData(move="",fen="",*,path=Obj.hint):
    if os.path.isfile(path):
        control = 'wb'
    else:
        control = 'xb'
    pickle.dump({"Move":move,"Fen":fen},open(path,control))
    

        

class mainScene(Scene):
    fenToSprite = 'KQBNRPkqbnrp' # fen과 sprite index를 대응하는 표    
    tileSize = 100
    @classmethod
    def playMusic(cls,m):
        if m in musicVolumeSheet:
            volume = musicVolumeSheet[m]
        else:
            volume = 1
        Rs.playMusic(musicSheet[m],volume=volume)
        configScene.credit.text = credit + musicCredits[Rs.currentMusic()]
        
    def makeChessObj(self,algCode):
        index = mainScene.fenToSprite.index(algCode)
        scale = Obj.game_geometry['board']['TileSize']/400.0
        obj = spriteObj("chess_sprite.png",pos=RPoint(0,0),sheetMatrix=(2,6),fromSprite=index,toSprite=index,scale=scale)
        obj.code = algCode # objects has it's algebraic code
        obj.center = RPoint(Obj.game_geometry['board']['TileSize']//2,Obj.game_geometry['board']['TileSize']//2)

        if algCode in list(self.chessObjs):
            self.chessObjs[algCode].append(obj)
        else:
            self.chessObjs[algCode]=[obj]
        return obj

    
    def initChessObj(self):
        self.chessObjs={}
        for code in mainScene.fenToSprite:
            for _ in range(20):
                self.makeChessObj(code)
                self.progress+=0.15
            
    
    def updateBoard(self):
        ##Make and place Chess Objects
        fen = Obj.config["Board"].fen()
        i = 0
        index = [0,0]
        while index[1]<8:
            if index[0]==8:
                index[1]+=1
                index[0]=0
            elif fen[i]=='/':
                continue
            elif '1'<=fen[i]<='8':
                r = range(int(fen[i]))
                for _ in r:
                    if Obj.config["UserIsWhite"]:
                        x,y = [index[0],index[1]]
                    else:
                        x,y = [7-index[0],7-index[1]]
                    if self.boardDisplay[y][x].chessObj != None:
                        obj = self.boardDisplay[y][x].chessObj
                        self.chessObjs[obj.code].append(obj)
                        obj.setParent(None)
                        self.boardDisplay[y][x].chessObj = None
                    index[0]+=1
            elif fen[i] in mainScene.fenToSprite:
                if Obj.config["UserIsWhite"]:
                    x,y = [index[0],index[1]]
                else:
                    x,y = [7-index[0],7-index[1]]
                    
                if self.boardDisplay[y][x].chessObj != None:
                    if self.boardDisplay[y][x].chessObj.code != fen[i]: #다른 오브젝트가 있는 경우 
                        #해당 오브젝트 제거
                        obj = self.boardDisplay[y][x].chessObj
                        self.chessObjs[obj.code].append(obj)
                        obj.setParent(None)

                        #새 오브젝트 추가
                        newObj = self.chessObjs[fen[i]].pop()
                        self.boardDisplay[y][x].chessObj = newObj
                        newObj.setParent(self.boardDisplay[y][x])
                else:
                    #새 오브젝트 추가
                    newObj = self.chessObjs[fen[i]].pop()
                    self.boardDisplay[y][x].chessObj = newObj
                    newObj.setParent(self.boardDisplay[y][x])

                index[0]+=1
            i+=1
            
        ##TODO: Update dead objects
        chessboard = fen.split()[0]
        myChilds = []
        herChilds = []

        s = 0
        

        self.myDeadObj = layoutObj(Obj.game_geometry['board']['MyDeadPos'],isVertical=False,spacing=s,childs=myChilds)
        self.herDeadObj = layoutObj(Obj.game_geometry['board']['HerDeadPos'],isVertical=False,spacing=s,childs=herChilds)
            
    #시작 기물을 정한다.
    def makeBoard(self,powerReset=False):
        
        
        if powerReset:
            self.initChessObj()
        else:
            for i in range(8):
                for j in range(8):
                    _obj = self.boardDisplay[j][i].chessObj
                    if _obj != None:
                        _obj.setParent(None)
                        self.chessObjs[_obj.code].append(_obj)
                        self.boardDisplay[j][i].chessObj = None

        #Board Making
        if Obj.config["Board"].is_checkmate():
            Obj.config["Board"] = chess.Board()
            Obj.config["HintCount"] = 0
            Obj.config["Swapped"] = False

        self.boardDisplay = gridObj(Obj.game_geometry['board']['Pos'],(Obj.game_geometry['board']['TileSize'],Obj.game_geometry['board']['TileSize']),(8,8),spacing=(0,0),color=Cs.brown)
        self.deadObjs = []
        self.bongcloudOpened = False # Bongcloud 오프닝이 일어났는지 체크하는 인자
        self.ladyBestMode = False # 이 모드가 활성화되면 제일 좋은 수만 둔다.
        self.ladyIsOnMate = False # 체크메이트 수순에 들어갔음을 알려주는 인자.
        self.undoCounter = 0.0 # Undo 확률과 관련된 인자.
        self.promotionGUI = None # 프로모션될 기물들을 보여줄 gui.
        
        self.aboutHint = {"Hint":None,"Fen":None} # Hint를 확인하는 인자.
        self.showHint = False
        self.hintCounter = 0.0 # 힌트 줄 확률과 관련된 인자.
        self.hintProc = None
        self.hintCoolTime=1

        self.currentColor = ''
        self.evaluation = {'type':'cp','value':0} # Ai의 chess 평가값을 저장하는 인자.
        if hasattr(self,'lastMovedObj'):
            self.lastMovedObj.setParent(None)

        #Board Coloring
        for i in range(8):
            for j in range(8):
                if Obj.config["UserIsWhite"]:
                    if (i+j)%2==0:
                        self.boardDisplay[i][j].color=Cs.dark(Cs.brown)                    
                else:
                    if (i+j)%2==1:
                        self.boardDisplay[i][j].color=Cs.dark(Cs.brown)
                self.boardDisplay[i][j].chessObj = None

        ##Make and place Chess Objects
        self.updateBoard()

        if self.proc != None:
            self.proc.terminate()
            self.proc = None
        makeAIData("") # Reset Ai thinking

        self.makeCoordinate() # Set Coordinate


    def ladySays(self,sentence):
        self.currentSentence = sentence        
        geometry = Obj.game_geometry['talk']['Pos']
        size = Obj.game_geometry['talk']['TextSize']
        width = Obj.game_geometry['talk']['TextWidth']
        self.talkObj = longTextObj(sentence,geometry,size=size,textWidth=width)
        self.talkBgObj = rectObj(Rs.padRect(self.talkObj.boundary,size),color=Cs.black)
        self.talkObj = longTextObj("",geometry,size=size,textWidth=width)
        self.talkObj.alpha=255
        self.talkBgObj.alpha = 0
        self.talkTimer = min(150,len(sentence)*5)
        
        None

    def makeCoordinate(self):
        coordinateX = 'abcdefgh'
        if not Obj.config["UserIsWhite"]:
            coordinateX=coordinateX[::-1]
        temp = []
        for c in coordinateX:
            obj = textButton(c,pygame.Rect(0,0,Obj.game_geometry['board']['TileSize'],Obj.game_geometry['board']['TileSize']//2),hoverMode=False,color=Cs.black)
            temp.append(obj)
        pos = self.boardDisplay.pos+RPoint(0,Obj.game_geometry['board']['TileSize']*8)
        self.coordinateXObj = layoutObj(pos=pos,spacing=0,isVertical=False,childs=temp)
        
        coordinateY = '12345678'
        if Obj.config["UserIsWhite"]:
            coordinateY=coordinateY[::-1]
        temp = []
        for c in coordinateY:
            obj = textButton(c,pygame.Rect(0,0,Obj.game_geometry['board']['TileSize']//2,Obj.game_geometry['board']['TileSize']),hoverMode=False,color=Cs.black)
            temp.append(obj)
        pos = self.boardDisplay.pos+RPoint(-50,0)
        self.coordinateYObj = layoutObj(pos=pos,spacing=0,childs=temp)
        
    def makeTurnButton(self):
        currentColor = Obj.config["Board"].fen().split()[1]
        if self.currentColor != currentColor:
            self.currentColor = currentColor
            number = Obj.config["Board"].fullmove_number
            if currentColor=='w':
                number = 2*number-1
            else:
                number = 2*number
            turnText = "Turn "+str(number)+', '
            if self.isUserTurn():
                t = "Your Turn"
            else:
                t = "Lady's Turn"
            
            if currentColor=='w':
                c = [Cs.white,Cs.black]
            else:
                c = [Cs.black,Cs.white]
            self.turnButton = textButton(turnText+t,Obj.game_geometry['button']['button2'],color=c[0],fontColor=c[1],hoverMode=False)    
            self.turnButton.center = self.boardDisplay[4][4].geometryPos + 5*RPoint(0,Obj.game_geometry['board']['TileSize'])
            self.turnButton.update()


    #display 상에서의 좌표를 체스 좌표로 전환하는 함수
    def posToChessPos(self,i,j):
        x = 'abcdefgh'
        temp = ''
        if Obj.config["UserIsWhite"]:
            temp+=x[i]
        else:
            temp+=x[7-i]
        
        y = '12345678'
        if Obj.config["UserIsWhite"]:
            temp+=y[7-j]
        else:
            temp+=y[j]
        
        return temp
    
    #체스 좌표(ex:'h2')를 display 상의 좌표로 변환
    def chessPosToPos(self,fen):
        x = 'abcdefgh'.index(fen[0])
        y = '12345678'.index(fen[1])
        if Obj.config["UserIsWhite"]:
            return [x,7-y]
        else:
            return [7-x,y]
        
    #현재 가능한 움직임에 대한 Dictionary를 받는다.
    def getLegalMoves(self):
        l = list(Obj.config["Board"].legal_moves)
        l = [str(x) for x in l]
        s = {}
        for x in l:
            start_point = x[:2]
            move_point = x[2:]
            if start_point in list(s):
                s[start_point].append(move_point)
            else:
                s[start_point] = [move_point]
        return s

    #'d2d4'와 같은 string으로 이동하는 함수이다.
    def moveByString(self,s):

        currentColor = Obj.config["Board"].fen().split()[1]
        number = Obj.config["Board"].fullmove_number
        if currentColor=='w':
            number = 2*number-1
        else:
            number = 2*number

        Obj.config["PGN"]+="{0}. {1} ".format(number,s)
        self.moveButton.text = s
        if Obj.config["Board"].piece_at(chess.parse_square(s[2:4])):
            piece = str(Obj.config["Board"].piece_at(chess.parse_square(s[2:4])))
            Rs.playSound('chess-kill.wav',volume=Obj.pieceVolume[piece.upper()])
            
            
        Obj.config["Board"].push_san(s)
        self.updateBoard()
        mainScene.saveConfig()


        startPoint = s[:2]
        endPoint = s[2:]
        

        x,y = self.chessPosToPos(startPoint)
        i,j = self.chessPosToPos(endPoint)
        delta = self.boardDisplay[y][x].geometryPos-self.boardDisplay[j][i].geometryPos
        self.lastMovedObj.setParent(self.boardDisplay[j][i])        
        if not self.isUserTurn():
            self.lastMovedObj.pos = delta
            self.boardDisplay[j][i].chessObj.pos=delta
        self.boardDisplay[j][i].childs = self.boardDisplay[j][i].childs[::-1]

        return [i,j]

    @classmethod
    def saveConfig(cls):
        Rs.saveData(Obj.configPath,Obj.config)

    def isMovable(self,i,j):
        fen = self.posToChessPos(i,j)
        legalMoves = self.getLegalMoves()
        
        return fen in list(legalMoves)

    def updatePossiblePoint(self,i,j,*,alpha=20):
        fen = self.posToChessPos(i,j)
        legalMoves = self.getLegalMoves()
        for obj in self.legalMoveObjects:
            obj.setParent(None)
        self.legalMoveObjects = []
        
        if fen in list(legalMoves):
            for point in legalMoves[fen]:
                hoverObj = rectObj(self.boardDisplay[0][0].rect,color=Cs.yellow)
                hoverObj.alpha = alpha
                x,y = self.chessPosToPos(point)
                hoverObj.setParent(self.boardDisplay[y][x])
                self.legalMoveObjects.append(hoverObj)
                
    ##TODO: AI가 현재 보드에 대한 Hint Data 생성
    def aiMakeHint(self):
        from multiprocessing import Process
        if self.hintProc != None:
            self.hintProc.join(timeout=0)
            if self.hintProc.is_alive():
                return
            else:
                data = pickle.load(open(Obj.hint,'rb'))
                self.aboutHint = data
                makeAIHintData("")
                self.hintProc = None
        else:
            if self.aboutHint["Fen"]!=Obj.config["Board"].fen():
                self.hintProc = Process(target=stockFishHintProcess,args=(Obj.config["Board"].fen(),stockFishPath))
                self.hintProc.start()
        None
                
    def aiMove(self):
        from multiprocessing import Process
        if self.proc != None:
            self.proc.join(timeout=0)
            if self.proc.is_alive():
                return
            else:
                data = pickle.load(open(Obj.think,'rb'))
                #print(data)#DEBUG
                if data['Move']!="" and data['Move']!="Thinking":
                    move = data['Move']['Move']
                    cur_cp = data['Move']['Centipawn']
                    mate = data['Move']['Mate']
                    if not self.ladyIsOnMate and mate!=None:
                        self.ladyIsOnMate = True
                        self.swappedColorTimer=25 ## 컬러스왑 불가
                        Obj.config["Swapped"]=True
                        self.ladySays(random.choice(talkScript['mate']))
                
                    if 'e1' in move or 'e8' in move or Obj.config["Board"].fullmove_number>3:
                        self.bongcloudOpened = True #King Moved or too late to bongcloud


                    ##잦은 버그가 발생하는 코드. 임시방편으로 때워야 겠다....
                    ##임시방편으로 때워도 안됨. TODO: 디버깅 필요
                    try:
                        self.lastChessObj = self.moveByString(move)
                    except:
                        makeAIData("")
                        print("EXCEPTION ERROR")
                        legalMoves = [str(x) for x in list(Obj.config["Board"].legal_moves)]
                        self.lastChessObj = self.moveByString(random.choice(legalMoves))
                        return
                    #self.debugObj.text = str(data['Eval']) ##DEBUG##
                    
                    try:
                        if self.evaluation['type']=='cp':
                            pre_evaluation_cp = self.evaluation['value']
                        else:
                            pre_evaluation_cp = None                            
                    except:
                        pre_evaluation_cp = None
                        
                    self.evaluation = data['Eval']
                    if pre_evaluation_cp != None and self.evaluation['type']=='cp' and cur_cp != None:
                        cp = self.evaluation['value']
                        check_better = cp-pre_evaluation_cp # good for white
                        if not Obj.config["UserIsWhite"]:
                            check_better = -check_better
                        if check_better>10:
                            r = min(1,check_better/150)
                            if random.random()<r:
                                self.ladySays(random.choice(talkScript['praise']))
                        elif check_better<-100:
                            #Lady가 실제로 응징하거나, 일정확률로 블런더 출력
                            if abs(cp-cur_cp)<30 or random.random()<0.2:
                                self.ladySays(random.choice(talkScript['blunder']))
                                self.showSmile=True
                        
                    Rs.playSound('move-chess.wav')
                    self.ladyHandTimer=30
                    makeAIData("")
                    self.proc = None
                else:
                    makeAIData("")
        else:
            c = (Obj.config["Board"].fullmove_number/200.0)
            if random.random()<c:
                self.ladyBestMode = True # 턴이진행될수록 bestMode 진입확률 증가
            self.proc = Process(target=stockFishProcess,args=(1000,Obj.config["Board"].fen(),stockFishPath,self.bongcloudOpened,self.ladyBestMode))
            self.proc.start()
            makeAIData("Thinking")
            
    def updateHintCounter(self):
        c = max(Obj.hintCountMax - Obj.config["HintCount"] + 1,0)
        t = ""
        for _ in range(c):
            t += Obj.heart
        for _ in range(Obj.hintCountMax-c+1):
            t += Obj.emptyHeart
            
        self.hintCounterObj.text = t        
            
  
    def isUserTurn(self):
        if Obj.config["UserIsWhite"]:
            temp = chess.WHITE
        else:
            temp = chess.BLACK
        
        if Obj.config["Board"].turn == temp:
            return True
        return False

    def initOnce(self):
        Rs.setIcon("gameIcon_184.png")
        pygame.mouse.set_visible(False)
        Obj.cursor = imageObj("cursor.png",scale=0.5)

            
        

        self.proc = None
        #Obj.config["UserIsWhite"] = False
        self.legalMoveObjects = []
        self.deadObjs = [] # stores dead chess obj
        self.chessObjs = {}
        self.clickedPos = [] # 현재 클릭된 물체의 위치를 저장하는 변수
        makeAIData("") # Reset Ai thinking
        Obj.renewCondition()
        Rs.setVolume(Obj.config["Volume"])
                
        ##TODO:Buffering##
        self.bufferText = textObj('Now Loading',(400,400),color=Cs.white,size=Obj.game_geometry['sys']['ButtonFontSize'])
        self.bufferText.center = Rs.Point(Rs.screen.get_rect().center)
        self.bufferTimer = 0
        self.bufferBackground = imageObj("loding_background.png",Rs.screen.get_rect())
        self.isBuffering = True
        self.bufferText.draw()
        self.progress = 0
        import threading
        t = threading.Thread(target=self.buffering)
        t.start()
        

        ##잡담을 저장하는 인자 
        self.conversationList = list(talkScript['conversation'])
        random.shuffle(self.conversationList)
        self.raiseRematch = False
        random.shuffle(talkScript['talking'])

        self.talkTimer = 0
        self.undoCoolTime = 0
        self.hintCoolTime = 0
        if Obj.config["Swapped"]:
            self.swappedColorTimer = 0            
        else:
            self.swappedColorTimer = -1
            
        self.currentSentence = ""
        self.currentMousePos = None
        self.talkObj = longTextObj("",(950,200),size=20,textWidth=350)
        mainScene.changedCloth=False #옷을 바꿨음을 체크하는 인자
        
        
        
        self.progress = 25
        self.makeBoard(True)
        #마지막에 움직인 체스 기물을 표시하기 위한 Obj (초록 불빛)
        self.lastMovedObj = imageObj('chess-greenLight.png',pos=(0,0))
        self.lastMovedObj.rect = Rs.padRect(self.boardDisplay[0][0].rect,-5)
        self.lastMovedObj.center = self.boardDisplay[0][0].center
        self.lastMovedObj.alpha = 50

        self.hoverObj = rectObj(self.boardDisplay[0][0].rect,color=Cs.yellow)
        self.hoverObj.alpha = 60
        

        #Init Lady Sprites# 
        ladyGeometry= Obj.game_geometry['lady']
        mainScene.ladyObj = imageObj(costumeSheet[Obj.config["Costume"]],pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        self.ladyThinkingObj = imageObj('lady_bongcloud_thinking.png',pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        self.ladySmileObj = imageObj('lady_bongcloud_happy.png',pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        self.showSmile = False
        self.ladyMouthObj = imageObj('lady_bongcloud_mouth.png',pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        self.ladyClosedEyesObj = imageObj('lady_bongcloud_closedEyes.png',pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        self.ladyCloseEyeTimer = 0 
        self.ladyHandObj = imageObj('lady_bongcloud_hand.png',pos=(0,0),scale=ladyGeometry['Hand'])
        self.ladyHandTimer = 0
        self.ladyBreastsObj = rectObj(ladyGeometry['breasts'],color=Cs.red,alpha=100)
        
        
        
        #Background Objects#
        self.bgPatternObj = imageObj('chess-room.png',pos=(0,0))
        self.bgPatternObj.rect = Rs.screen.get_rect()
        
        backSize = Obj.game_geometry['board']['TileSize']*8+30
        self.chessBackObj = rectObj(pygame.Rect(0,0,backSize,backSize),color=Cs.black)
        self.chessBackObj.scale = 0.9
        self.chessBackObj.center = self.boardDisplay[4][4].geometry.topleft
        
        self.chessTableObj = imageObj('chess-table-2.png',pos=Obj.game_geometry['chessTable']['Pos'],scale=Obj.game_geometry['chessTable']['Scale'])
        
        Scenes.configScene.initOnce()
        Scenes.configScene.initiated=True
        
        #Button Objects#
        self.raiseRematch = False
        self.rematchWhiteButton = textButton("White",Obj.game_geometry['button']['button1'],color=(200,200,200),fontColor=Cs.black)
        self.rematchBlackButton = textButton("Black",Obj.game_geometry['button']['button1'],color=(50,50,50),fontColor=Cs.white)
        
        def rematch(colorIsWhite):
            def f():
                # 보드 초기화
                Obj.config["Board"]=chess.Board()
                Obj.config["PGN"]=""
                self.moveButton.text = ""
                self.raiseRematch = False
                Obj.config["UserIsWhite"] = colorIsWhite
                self.makeBoard(False)
                Rs.playSound('chess-rematch.wav')
                self.swappedColorTimer = -1 ## 컬러스왑한 사실을 없앰
                Obj.config["Swapped"]=False
                Obj.config["HintCount"]=0
                self.updateHintCounter()
                self.hintCoolTime=125
                self.swapButton.fontColor = Cs.white
                self.ladySays(random.choice(talkScript['newgame']))
                Obj.renewCondition()
            return f
        self.rematchBlackButton.connect(rematch(False))
        self.rematchWhiteButton.connect(rematch(True))
        self.rematchButtonLayout = layoutObj(pos=Obj.game_geometry['button']['pos1'],childs=[self.rematchBlackButton,self.rematchWhiteButton],isVertical=False)
        for button in self.rematchButtonLayout.childs:
            button.setAlpha(0)
            
        self.hintButton = textButton("Get Hint",Obj.game_geometry['button']['button1'],color=Cs.hexColor("FB8DA0"))
        self.hintCounterObj = textObj("")
        if Obj.config["HintCount"]>Obj.hintCountMax:
            self.hintButton.fontColor = (160,160,160)
        def getHint():
            if self.hintCoolTime==0 and self.showHint == False and self.isUserTurn():
                if Obj.config["HintCount"]>Obj.hintCountMax:
                    self.ladySays(random.choice(talkScript['hint-disabled']))
                else:
                    if self.aboutHint["Fen"] == Obj.config["Board"].fen() and self.aboutHint["Move"]!=None:
                        words = random.choice(talkScript['hint-ok'])
                        words = words.replace('#',self.aboutHint["Move"])
                        self.showHint = True
                        self.ladySays(words)
                        Obj.config["HintCount"]+=1
                        self.updateHintCounter()

                        mainScene.saveConfig()
                    else:
                        self.ladySays(random.choice(talkScript['hint-reject']))
                self.hintCoolTime=127
        self.hintButton.connect(getHint)
        self.undoButton = textButton("Undo Move",Obj.game_geometry['button']['button1'],color=Cs.hexColor("EFD3B5"))        
        self.rematchButton = textButton("Rematch",Obj.game_geometry['button']['button1'],color=Cs.hexColor("A47551"))
        #게임중에 색을 바꿔서 플레이
        self.swapButton = textButton("Swap Side",Obj.game_geometry['button']['button1'],color=Cs.dark(Cs.grey))
        if Obj.config["Swapped"]:
            self.swapButton.fontColor= Cs.black
        # 재경기 의사를 표현한다.
        def raise_rematch():
            if not self.raiseRematch:
                self.ladySays("Which color do you want to play?")
            else:
                self.raiseRematch = True
                self.ladySays("Oh, Ok.")
            self.raiseRematch = not self.raiseRematch                
        self.rematchButton.connect(raise_rematch)
        
        def swapColor():
            if self.swappedColorTimer == -1:
                Obj.config["UserIsWhite"] = not Obj.config["UserIsWhite"]
                Obj.config["Swapped"]=True
                Obj.config["HintCount"]=Obj.hintCountMax+1 ## 힌트를 더 받을 수 없다.
                self.updateHintCounter()

                self.hintCoolTime=127
                mainScene.saveConfig()
                self.makeBoard(False)
                Rs.playSound('chess-rematch.wav')
                self.ladySays(random.choice(talkScript['swap']))
                self.swappedColorTimer = 25 ##컬러 스왑했음을 알려주는 타이머
                makeAIData("") # Reset Ai thinking
        
        self.swapButton.connect(swapColor)
        
        def undoMove():
            if self.undoCoolTime==0:
                if self.isUserTurn() and random.random()>self.undoCounter:
                    Obj.config["Board"].pop()
                    Obj.config["Board"].pop()
                    self.updateBoard()
                    self.lastMovedObj.setParent(None)
                    self.ladySays(random.choice(talkScript['undo-ok']))
                    self.undoCounter=min(1,self.undoCounter+random.random()*0.5)
                else:
                    self.ladySays(random.choice(talkScript['undo-reject']))
                    self.undoCounter=max(0,self.undoCounter*0.5)
                self.undoCoolTime = 127

        self.undoButton.connect(undoMove)

        self.exitButton = textButton("End Game",Obj.game_geometry['button']['button1'],color=Cs.dark(Cs.red))
        self.exitButton.connect(REMOGame.exit)

        self.conversationButton = imageButton("speech_icon.png",Obj.game_geometry['button']['talkButton'])
        self.conversationButton.alpha = 200
        def conversation():
            if self.talkTimer==0:
                if len(self.conversationList)>0:
                    self.ladySays(self.conversationList.pop())                    
                else:
                    self.conversationList = list(talkScript['conversation'])
                    random.shuffle(self.conversationList)
                    
                    
        self.conversationButton.connect(conversation)

        self.progress = 100

        spacing = Obj.game_geometry['board']['TileSize']//10

        self.buttonLayout = layoutObj(pos=Obj.game_geometry['button']['pos2'],childs=[self.hintButton,self.undoButton,self.rematchButton,self.swapButton],spacing=spacing)
        t = Obj.game_geometry['board']['TileSize']
        self.hintCounterObj.center = self.hintButton.geometryCenter+RPoint(-t//2,-t//3)
        self.updateHintCounter()
        self.configButton = textButton("Config",Obj.game_geometry['button']['button1'],color=Cs.hexColor("9DB6CC"))
        
        self.configButton.connect(configScene.turnToConfig)
        
        self.helpButton = textButton("Help",Obj.game_geometry['button']['button1'],color=Cs.red)
        def showHelp():
            Rs.setCurrentScene(Scenes.helpScene)
        self.helpButton.connect(showHelp)


        self.buttonLayout2 = layoutObj(pos=Obj.game_geometry['button']['pos3'],childs=[textObj("system",color=Cs.black,size=Obj.game_geometry['sys']['ButtonFontSize']),self.configButton,self.helpButton,self.exitButton],spacing=spacing)

        self.debugObj = longTextObj('',pos=(0,0),textWidth=200)
        
        self.makeTurnButton()
        self.moveButton = textButton("",Obj.game_geometry['button']['button3'],color=Cs.black,fontColor=Cs.grey,hoverMode=False)
        self.moveButton.center = self.turnButton.geometryCenter + RPoint(Obj.game_geometry['button']['button3'].width*3,0)

        if Obj.config["PGN"]!="":
            lastMove = Obj.config["PGN"].split()[-1]
            self.moveButton.text = lastMove

        self.moveButton.update()



        self.turnButtonTimer = 0
        
        self.ladySays(random.choice(talkScript['greeting']))


        mainScene.playMusic(Obj.config["Music"])

        makeAIData("")
        
        self.isBuffering=False


        return


    
    def buffering(self):
        while self.isBuffering:
            point = ""
            for _ in range(self.bufferTimer%4):
                point+='.'
            self.bufferText.text='Now Loading'+point + '('+str(int(self.progress))+'%'+')'
            self.bufferTimer+=1
            Rs.fillScreen(Cs.brown)
            self.bufferBackground.draw()
            self.bufferText.draw()
            pygame.display.update()
            time.sleep(0.05)
        
    def init(self):
        return
    

    def update(self):
        if Rs.userJustPressed(pygame.K_ESCAPE):
            configScene.turnToConfig()
        if mainScene.changedCloth:
            mainScene.changedCloth=False
            self.ladySays(random.choice(talkScript['costume']))
        self.isHovering=False
        if self.isUserTurn():
            self.aiMakeHint()                
            if Rs.userJustLeftClicked() and self.promotionGUI:
                for c in self.promotionGUI.childs:
                    if c.collideMouse():
                        s = self.promotionKey+c.code
                        self.moveByString(s)
                        Rs.playSound('move-chess.wav')
                        self.hoverObj.setParent(None)
                        if self.talkTimer==0 and random.random()<0.2:
                            self.ladySays(random.choice(talkScript['thinking']))
                            
                for obj in self.promotionGUI.childs:
                    obj.setParent(None)
                    self.chessObjs[obj.code].append(obj)                                                                                    
                self.promotionGUI = None
                self.clickedPos=[]
            else:
            
                for j in range(8):
                    for i in range(8):
                        curObj = self.boardDisplay[j][i]
                        if curObj.collidepoint(Rs.mousePos()):
                            self.isHovering=True
                            self.hoverObj.setParent(curObj)
                            if Rs.userJustLeftClicked():
                                if self.clickedPos ==[]:
                                    if self.isMovable(i,j):
                                        ##DEBUG##
                                        l = list(Obj.config["Board"].legal_moves)
                                        l = [str(x) for x in l]
                                        
                                        self.raiseRematch = False

                                        self.clickedPos = [i,j]
                                        self.updatePossiblePoint(i,j,alpha=60)
                                else:
                                    x,y = self.clickedPos 
                                    legal = self.getLegalMoves()[self.posToChessPos(x,y)]
                                    def is_promo(x):
                                        if len(x)==3:
                                            return True
                                        return False
                                    promotion_list = list(filter(is_promo,legal))
                                    promotion = {}
                                    for p in promotion_list:
                                        key = p[:2]
                                        if key in promotion:
                                            promotion[key].append(p[2:])
                                        else:
                                            promotion[key]=[p[2:]]
                                    if self.posToChessPos(i,j) in promotion: ##TODO: 프로모션 처리
                                        self.promotionGUI = layoutObj(pos=curObj.geometryPos,spacing=0)
                                        t = Obj.game_geometry['board']['TileSize']
                                        self.promotionBoard = rectObj(Rs.padRect(pygame.Rect(0,0,t,4*t),t//4))
                                        self.promotionBoard.pos = curObj.geometryPos-RPoint(t//4,t//4)                                        
                                        self.promotionKey = self.posToChessPos(x,y)+self.posToChessPos(i,j)
                                        for code in promotion[self.posToChessPos(i,j)]:
                                            if Obj.config["UserIsWhite"]:
                                                code = code.upper()
                                            obj = self.makeChessObj(code)
                                            obj.setParent(self.promotionGUI)
                                    if self.posToChessPos(i,j) in legal:                            
                                        s = self.posToChessPos(x,y)+self.posToChessPos(i,j)
                                        self.moveByString(s)
                                        Rs.playSound('move-chess.wav')
                                        self.hoverObj.setParent(None)
                                        if self.talkTimer==0 and random.random()<0.2:
                                            self.ladySays(random.choice(talkScript['thinking']))
                                    
                                        
                                        
                                        
                                    if self.isMovable(i,j) and not self.clickedPos == [i,j]:
                                        self.clickedPos = [i,j]
                                        self.updatePossiblePoint(i,j,alpha=60)
                                    else:                                
                                        self.clickedPos=[]
                                        self.updatePossiblePoint(i,j)

                                        
                            if self.clickedPos ==[]:
                                if self.currentMousePos != [i,j]:
                                    self.currentMousePos = [i,j]
                                    self.updatePossiblePoint(i,j)
                            break
            if not self.isHovering:
                self.hoverObj.setParent(None)            
                if self.clickedPos == []:
                    for obj in self.legalMoveObjects:
                        obj.setParent(None)
                    self.legalMoveObjects = []
                if Rs.userJustLeftClicked():
                    self.clickedPos=[]
        else:
            if self.showHint:
                self.showHint = False
            self.aiMove()
        
        #체스말 부드럽게 움직이기 위한 코드
        if self.lastMovedObj != None and self.lastMovedObj.pos != RPoint(0,0):
            arrival =RPoint(Obj.game_geometry['board']['TileSize']//2,Obj.game_geometry['board']['TileSize']//2)
            self.lastMovedObj.center = (self.lastMovedObj.center-arrival)*0.7+arrival
            if hasattr(self.lastMovedObj.parent,"chessObj"):
                self.lastMovedObj.parent.chessObj.center = (self.lastMovedObj.center-arrival)*0.7+arrival
                if self.lastMovedObj.parent.chessObj.center.distance(arrival)<5:
                    self.lastMovedObj.parent.chessObj.center = arrival
        
        ##Turn Button Color Change ##
        curColor = Obj.config["Board"].fen().split()[1]
        if self.currentColor !=curColor:
            self.currentColor = curColor
            number = Obj.config["Board"].fullmove_number
            if curColor=='w':
                number = 2*number-1
            else:
                number = 2*number
            turnText = "Turn "+str(number)+', '
            
            if Obj.config["Board"].is_checkmate():
                t = "Checkmate"
            else:
                if self.isUserTurn():
                    t = "Your Turn"
                else:
                    t = "Lady's Turn"
            self.turnButton.text = turnText+t
            self.turnButtonTimer=100
        
        if self.turnButtonTimer>0:
            self.turnButtonTimer-=1
            if self.currentColor=='w':
                c = self.turnButton.color[0]
                c = min(255,c+20)
            else:
                c = self.turnButton.color[0]
                c = max(0,c-20)
            self.turnButton.color = (c,c,c)
            self.turnButton.fontColor = (255-c,255-c,255-c)

        ## Lady Updates ##
        if self.talkTimer==0:
            if random.random()<0.0002:
                if len(talkScript['talking'])>0:
                    self.ladySays(talkScript['talking'].pop())
        if random.random()<0.005:
            self.ladyCloseEyeTimer=5

        ## Undo 안되는 경우
        if Obj.config["Board"].fullmove_number<=1 or Obj.config["Board"].is_checkmate() or Obj.config["Swapped"]:
            self.undoCoolTime=127
            
        if self.swappedColorTimer>0:
            self.swappedColorTimer-=1
            c = self.swappedColorTimer*8
            self.swapButton.fontColor = (c,c,c)
            

        if self.undoCoolTime>0:
            self.undoCoolTime-=1
            c = 255-2*self.undoCoolTime
            self.undoButton.fontColor = (c,c,c)
        if self.hintCoolTime>0:
            self.hintCoolTime-=1
            c = 255-2*self.hintCoolTime
            if Obj.config["HintCount"]>Obj.hintCountMax:
                c = min(160,c)
            self.hintButton.fontColor = (c,c,c)

        ## Button Updates ##
        if self.raiseRematch:
            for button in self.rematchButtonLayout.childs:
                button.setAlpha(min(200,button.alpha+20))
                
            self.rematchButtonLayout.update()
        else:
            for button in self.rematchButtonLayout.childs:
                button.setAlpha(max(0,button.alpha-20))

        self.buttonLayout.update()
        self.buttonLayout2.update()
        if self.talkTimer<25:
            self.conversationButton.update()
        if self.promotionGUI:
            self.promotionGUI.update()

        self.moveButton.update()
            
        ## DEBUG ##
        if Rs.userJustLeftClicked():
            print(Rs.mousePos())
        self.debugObj.pos = Rs.mousePos()+RPoint(20,20)
        self.debugObj.text = str(Rs.mousePos()) ## DEBUG

        return
    def draw(self):
        Rs.fillScreen(Cs.dark(Cs.dustyRose))
        self.bgPatternObj.draw()
        mainScene.ladyObj.draw()
        if not self.isUserTurn():
            self.ladyThinkingObj.draw()
        if self.talkTimer>50:
            self.ladyMouthObj.draw()
        if self.showSmile:
            self.ladySmileObj.draw()
        if self.ladyCloseEyeTimer>0:
            self.ladyCloseEyeTimer-=1
            self.ladyClosedEyesObj.draw()
        self.chessTableObj.draw()
        self.chessBackObj.draw()
        self.boardDisplay.draw()
        self.coordinateXObj.draw()
        self.coordinateYObj.draw()
        
        
        self.myDeadObj.draw()
        self.herDeadObj.draw()
        
        if self.showHint and self.aboutHint["Fen"]==Obj.config["Board"].fen():
            move = self.aboutHint["Move"]
            sx,sy = self.chessPosToPos(move[:2])
            ex,ey = self.chessPosToPos(move[2:4])
            c = self.boardDisplay[0][0].center
            a_s = self.boardDisplay[sy][sx].geometryPos+c
            a_e = self.boardDisplay[ey][ex].geometryPos+c

            arrowSize = int(0.2*Obj.game_geometry['board']['TileSize'])
            Rs.drawArrow(a_s,a_e,alpha=100,trirad=2*arrowSize,thickness=arrowSize)


        if self.lastMovedObj != None and self.lastMovedObj.pos != RPoint(0,0):
            if hasattr(self.lastMovedObj.parent,"chessObj") and self.lastMovedObj.parent.chessObj!=None:
                self.lastMovedObj.parent.chessObj.draw()

        if self.promotionGUI:
            self.promotionBoard.draw()
            self.promotionGUI.draw()

        if self.ladyHandTimer>0:
            x,y = self.lastChessObj
            lastObj = self.boardDisplay[y][x]
            self.ladyHandObj.center = lastObj.geometryPos + RPoint(-20,-70) # 체스말에 맞게 수정해야 함
            self.ladyHandObj.draw()
            self.ladyHandTimer-=1


        self.turnButton.draw()
        self.moveButton.draw()
        self.buttonLayout.draw()
        if self.hintButton.collideMouse():
            self.hintCounterObj.draw()
        self.buttonLayout2.draw()
        if self.talkTimer<25:
            self.conversationButton.draw()
        self.rematchButtonLayout.draw()
        

        if self.talkTimer>0:

            temp = False
            ##미세조정: 스크립트가 위아래로 왔다리 갔다리 하는 것을 막기 위한 조정임.
            i = len(self.talkObj.text)
            if i < len(self.currentSentence):
                fullText = self.currentSentence
                while i < len(fullText) and fullText[i] != " ":
                    i+=1
                parsedText = fullText[:i]
                l1 = self.talkObj.getStringList(self.talkObj.text)[:-1]
                l2 = self.talkObj.getStringList(parsedText)[:-1]
                try:
                    while len(l1[-1]) > len(l2[-1]):
                        self.talkObj.text = fullText[:len(self.talkObj.text)+1]
                        l1 = self.talkObj.getStringList(self.talkObj.text)[:-1]
                        temp = True
                except:
                    pass
                if not temp:
                    self.talkObj.text = self.currentSentence[:len(self.talkObj.text)+1]
            else:
                self.talkTimer -=1
                if self.talkTimer==0:
                    self.showSmile=False

            if self.talkTimer<25:
                self.talkObj.alpha = int(self.talkTimer*8)
                self.talkObj._update()
                self.talkBgObj.alpha = int(self.talkTimer*8)
                self.conversationButton.alpha = int((25-self.talkTimer)*8)
                if self.talkTimer>1:
                    self.conversationButton.hoverMode=False
                else:
                    self.conversationButton.hoverMode=True

            else:
                self.talkBgObj.alpha = min(200,self.talkBgObj.alpha+20)
                self.conversationButton.alpha = 0

            self.talkBgObj.draw()
            self.talkObj.draw()
        ## DEBUG ##
        #self.debugObj.draw() ##DEBUG
        Obj.cursor.pos = Rs.mousePos()
        Obj.cursor.draw()

        return

class configScene(Scene):
    def initOnce(self):
        ##TODO: Make Config Scene Objects ##
        print(Obj.config["PGN"])
                
        t = Obj.game_geometry['board']['TileSize']
        w,h = Rs.screen.get_rect().size
        self.blackBoard = rectObj(Rs.padRect(Rs.screen.get_rect(),-t//2),color=Cs.black,alpha=200)
        self.configLabel = textObj("Config",pos=(t*2,t),size=t//3)
        configScene.configBackButton = textButton("Go Back",pygame.Rect(w-4*t,h-2*t,t*2,t),color=Cs.white,fontColor=Cs.black)
        def configBack():
            #TODO: config 상태 저장
            mainScene.saveConfig()
            Rs.setCurrentScene(Scenes.mainScene)
        configScene.configBackButton.connect(configBack)
        configScene.configBackButton.alpha = 100
        
        self.creditButton = textButton("credit",Obj.game_geometry["credit"]["Button"],color=Cs.black,fontColor=Cs.grey,alpha=100)
        self.showCredit = False
        def show():
            self.showCredit = not self.showCredit
        self.creditButton.connect(show)
        
        configScene.credit = longTextObj(credit,Obj.game_geometry["credit"]["Pos"],textWidth=Obj.game_geometry['board']['TileSize']*6,color=Cs.grey)
        
        ##해상도 조절 버튼##
        self.resolutionLabel = textObj("Resolution")
        temp_l = []
        cur_res = Rs.screen.get_rect().size[0]
        for res in [1080,1440,1920,2560]:
            button = textButton(str(res),Obj.game_geometry['button']['button1'])
            if res == cur_res:
                button.color = Cs.dark(button.color)
                button.hoverMode = False
            def f(r):
                def _():
                    Obj.config["Resolution"]=r
                    Scenes.mainScene.initiated = False
                    updateGeoAndOpenGame()
                    mainScene.saveConfig()
                return _
            button.connect(f(res))

            temp_l.append(button)
            
        self.resolutionLayout = layoutObj(pygame.Rect(0,0,t//2,t//2),isVertical=False,childs=temp_l)
        self.modeLabel = textObj("Game Mode")
        
        
        ##풀스크린 조절 버튼
        l=[]
        for mode in modeSheet:
            button = textButton(mode,Obj.game_geometry['button']['button1'])
            if Rs.isFullScreen() == modeSheet[mode]:
                button.color = Cs.dark(button.color)
                button.hoverMode = False
            def f(m):
                def _():
                    Obj.config["FullScreen"]=m
                    Rs.setFullScreen(modeSheet[m])
                    for button in self.modeLayout.childs:
                        if button.text == m:
                            button.color = Cs.dark(Cs.tiffanyBlue)
                            button.hoverMode = False
                        else:
                            button.color = Cs.tiffanyBlue
                            button.hoverMode = True
                    mainScene.saveConfig()
                return _
            button.connect(f(mode))
            l.append(button)
        self.modeLayout = layoutObj(pygame.Rect(0,0,t//2,t//2),isVertical=False,childs=l)
        
        ##음악 볼륨 조절 기능
        self.musicVolumeLabel = textObj("Music Volume")
        configScene.musicVolumeSlider = sliderObj(RPoint(0,0),length=4*t,isVertical=False,value=Rs.getVolume(),color=Cs.aquamarine)
        def musicVolumeUpdate():
            Rs.setVolume(configScene.musicVolumeSlider.value)
            Obj.config["Volume"] = configScene.musicVolumeSlider.value
        configScene.musicVolumeSlider.connect(musicVolumeUpdate)
        
        
        ##음악 선택 기능
        self.muslcSelectionLabel = textObj("Select Music")
        l2 = []
        for musicLabel in musicSheet:
            button = textButton(musicLabel,Obj.game_geometry['button']['button1'])
            if musicLabel == Obj.config["Music"]:
                button.color = Cs.dark(button.color)
                button.hoverMode = False
            def f(m):
                def _():
                    mainScene.playMusic(m)
                        
                    ##현재 재생중인 음악 버튼 비활성화 처리
                    for musicButton in self.musicSelectionLayout.childs:
                        if musicButton.text == m:
                            musicButton.color = Cs.dark(Cs.tiffanyBlue)
                            musicButton.hoverMode = False
                        else:
                            musicButton.color = Cs.tiffanyBlue
                            musicButton.hoverMode = True
                    Obj.config["Music"]=m
                return _
            button.connect(f(musicLabel))
            l2.append(button)
        self.musicSelectionLayout = layoutObj(pygame.Rect(0,0,t//2,t//2),isVertical=False,childs=l2)
        
        
        ##TODO: 코스튬 선택 기능
        self.costumeLabel = textObj("Costume")
        l3 = []
        for costumeLabel in costumeSheet:
            button = textButton(costumeLabel,Obj.game_geometry['button']['button1'])
            if costumeLabel == Obj.config["Costume"]:
                button.color = Cs.dark(button.color)
                button.hoverMode = False
            def f(m):
                def _():
                    mainScene.ladyObj.setImage(costumeSheet[m])
                        
                    ##현재 재생중인 음악 버튼 비활성화 처리
                    for costumeButton in self.costumeSelectionLayout.childs:
                        if costumeButton.text == m:
                            costumeButton.color = Cs.dark(Cs.tiffanyBlue)
                            costumeButton.hoverMode = False
                        else:
                            costumeButton.color = Cs.tiffanyBlue
                            costumeButton.hoverMode = True
                    Obj.config["Costume"]=m
                    mainScene.changedCloth=True
                return _
            button.connect(f(costumeLabel))
            l3.append(button)
        self.costumeSelectionLayout = layoutObj(pygame.Rect(0,0,t//2,t//2),isVertical=False,childs=l3)
                



        self.leftSettingLayout = layoutObj(pygame.Rect(t,t*2,0,0),isVertical=True,childs=[self.resolutionLabel,self.resolutionLayout,self.modeLabel,self.modeLayout,self.musicVolumeLabel,configScene.musicVolumeSlider,self.muslcSelectionLabel,self.musicSelectionLayout,self.costumeLabel,self.costumeSelectionLayout],spacing=20)
        
        

        return
    def init(self):
        return
    def update(self):
        ##TODO: ConFig Update##
        if Rs.userJustPressed(pygame.K_ESCAPE):
            Rs.setCurrentScene(Scenes.mainScene)
        configScene.configBackButton.update()
        self.leftSettingLayout.update()
        self.creditButton.update()
        return
    def draw(self):
        ##Config Draw##
        Rs.drawScreenShot()
        self.blackBoard.draw()
        self.configLabel.draw()
        configScene.configBackButton.draw()
        self.creditButton.draw()
        self.leftSettingLayout.draw()
        if self.showCredit:
            configScene.credit.draw()
        Obj.cursor.pos = Rs.mousePos()
        Obj.cursor.draw()

        return

    @classmethod
    def turnToConfig(cls):
        Rs.captureScreenShot()
        configScene.musicVolumeSlider.value = Rs.getVolume()
        Rs.setCurrentScene(Scenes.configScene)


class helpScene(Scene):
    def initOnce(self):
        return
    def init(self):
        Rs.captureScreenShot()
        self.backboard = rectObj(Rs.screen.get_rect(),color=Cs.black,alpha=200)
        self.rule = imageObj("chess-help.png",Rs.screen.get_rect())
        t = Obj.game_geometry['board']['TileSize']
        self.ruleLabel = textObj("Rule",pos=(t*2,t),size=t//3)

        return
    def update(self):
        configScene.configBackButton.update()
        return
    def draw(self):
        Rs.drawScreenShot()        
        self.backboard.draw()
        self.rule.draw()
        self.ruleLabel.draw()
        configScene.configBackButton.draw()
        Obj.cursor.pos = Rs.mousePos()
        Obj.cursor.draw()
        return


class Scenes:
    mainScene = mainScene()
    configScene = configScene()
    helpScene = helpScene()


if __name__=="__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    Obj.stockfish.set_depth(20)
    Obj.stockfish.set_skill_level(20)
    print(Obj.stockfish.get_parameters())

    ##TODO: 저장된 config 상태 적용
    if os.path.isfile(Obj.configPath):
        Obj.config = pickle.load(open(Obj.configPath,"rb"))
    else:
        Obj.config = Obj.default_config
        
    ##config 파일 검증
    ##키 손실이 발생할 경우 파일을 디폴트로 조정
    for key in Obj.default_config:
        if key not in Obj.config:
            Obj.config = Obj.default_config
    
    
    updateGeoAndOpenGame() # 게임을 이렇게 시작해도 문제 없음
    '''
    window = REMOGame((1920,1080),True,caption="Bishoujo Chess")
    REMOGame.setCurrentScene(Scenes.mainScene)
    window.run()

    '''
    # Done! Time to quit.


