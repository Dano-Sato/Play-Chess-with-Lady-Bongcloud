from model import Stockfish
import chess
from REMOLib import *

##TODO: AI의 체스 레이팅을 조절하는 기능을 추가한다.
##TODO: 미소녀를 체크메이트 할 경우 게임이 튕기는 버그 존재


stockFishPath = "stockfish-windows-2022-x86-64-avx2.exe"


##UI에 관련된 단어들을 각국어별로 저장한다.
UI_words = {
    "undo":{"en":"Undo Move","kr":"되돌리기","jp":"元に戻す","cn":"撤销"},
    "rematch":{"en":"Rematch","kr":"다시하기","jp":"リマッチ","cn":"再比赛"},
    "swap":{"en":"Swap Side","kr":"진영 바꾸기","jp":"サイドを交換する","cn":"交换阵营"},
    "config":{"en":"Config","kr":"설정","jp":"設定","cn":"设置"},
    "hint":{"en":"Get Hint","kr":"힌트","jp":"ヒント","cn":"提示"},
    "exit":{"en":"Exit Game","kr":"나가기","jp":"出口","cn":"退出"},
    "help":{"en":"Help","kr":"도움말","jp":"ヘルプ","cn":"帮助"},
    "black":{"en":"Black","kr":"검은색","jp":"黒","cn":"黑色"},
    "white":{"en":"White","kr":"흰색","jp":"白","cn":"白色"},
}


##UI, 그중에서도 턴에 관련된 단어들을 각국어별로 저장한다.
UI_turn = {
    "my-turn":{"en":"Your Turn","kr":"당신의 차례","jp":"あなたの番","cn":"你的回合"},
    "lady-turn":{"en":"Lady's Turn","kr":"아가씨의 차례","jp":"レディの番","cn":"小姐的回合"},
    "checkmate":{"en":"Checkmate","kr":"체크메이트","jp":"チェックメイト","cn":"将死"},
    "turn":{"en":"Turn","kr":"차례","jp":"番","cn":"回合"},
}


###대화 스크립트 모음


##default, en
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
                   "The Bongcloud Attack has been passed down in my family for centuries, sir.",
                   "In my family, the Bongcloud Attack is considered a sacred chess move.",
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
                   "Do you understand the beauty of the Bongcloud Attack?",
                   "The Bongcloud Attack requires boldness and creativity, sir.",
                   "The Bongcloud Attack can add excitement and unpredictability to your game, sir.",
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
               "What do you think about this attire, sir?",
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
            ],
    'winning':["Looks like you don't want to play game now, sir."
    ],
    'end':["It was a great game,sir. Would you like to play another round?",]
}

talkScript_kr = {
    'greeting': [
    "좋은 날이군요, 선생님.",
    "안녕하세요, 선생님. 오늘 기분은 어떠신가요?",
    "좋은 하루 보내시길 바랍니다, 선생님.",
    "안녕하세요, 선생님. 오늘 뵙게 되어 기쁩니다.",
    "오늘 뵙게 되어 반갑습니다, 선생님.",
    "안녕하세요, 선생님. 오늘도 좋은 하루를 보내고 계시길 바랍니다.",
    "오늘 이곳에 와주셔서 기쁩니다, 선생님."
],
    'praise':[
    "잘하셨습니다, 선생님.",
    "훌륭한 움직임이십니다, 선생님!",
    "정말 인상적인 수입니다, 선생님!",
    "좋은 생각이십니다, 선생님!",
    "선생님께는 이 게임에 대한 재능이 있으시군요.",
    "선생님의 플레이에 감명받았습니다.",
    "정말 잘하셨습니다, 선생님.",
    "선생님은 게임에 대한 훌륭한 감각을 지니고 계십니다.",
    "선생님께서는 이 게임에 진정한 재능이 있으십니다.",
    "앞으로 어떻게 전개될지 무척 궁금합니다.",
],
    'blunder':[
    "걱정하지 마세요, 선생님. 누구나 실수를 하는 법이니까요.",
    "괜찮습니다, 선생님. 계속 플레이해보세요.",
    "괜찮습니다, 선생님. 계속해봅시다.",
    "다음번에는 더 잘 이해하실 수 있을 거예요.",
    "그 수는 최선의 선택이 아닐 수도 있어요.",
    "더 나은 선택이 있을지도 모르겠네요.",
    "다른 수를 시도해보는 것도 좋을 것 같습니다.",
    "결국 우리는 즐기러 온 거잖아요.",
    "걱정하지 마세요, 누구에게나 일어날 수 있는 일이니까요.",
    "오늘 체스 말들이 자기만의 생각을 가지고 있는 것 같네요.",
    "흥미로운... 선택이군요!",
    "전혀 예상하지 못한 수네요.",
    "의심할 여지 없이 게임의 판도를 바꿀 수 있겠어요.",
    "선생님의 기술에 경외심을 느낍니다...",
    "당신의 뛰어난 수에 경외심을 느낍니다... 그 창의력에...",
    "체스의 마법사라고 불러도 될까요, 선생님?"
],
    'talking':[
    "항상 선생님을 뵙는 것이 기다려져요.",
    "몸조심하세요, 선생님. 선생님의 건강과 안녕이 가장 중요합니다.",
    "체스는 집중력과 주의력을 향상시킬 수 있습니다, 선생님.",
    "선생님과 함께할 수 있어 기쁩니다.",
    "오늘 날씨가 정말 아름답네요, 선생님.",
    "정말 멋진 날입니다, 선생님.",
    "태양이 너무 아름답게 빛나고 있네요.",
    "경기를 하기 좋은 날입니다.",
    "오늘 날씨가 게임하기에 아주 좋아요, 선생님.",
    "오늘 같이 좋은 날에는 체스 게임이 제격입니다, 선생님.",
],
    'newgame':["함께 게임을 즐겨봅시다, 선생님.",
               "게임을 시작하죠, 선생님.",
               "게임을 시작할까요, 선생님?"
               ],
    'mate':["죄송합니다만, 선생님, 제가 이긴 것 같습니다."],
    'shy':['...어디서 보십니까, 선생님?',
           "... 당신이 내 여성스러운 부분에 관심이 있는지 몰랐습니다...",
           "... 나는 당신의 열망하는 얼굴을 봅니다...",
           "... 무슨 생각인지 알 수 있을까요, 선생님...?",
           "... 이야기하고 싶은 것이 있습니까, 선생님?",
           "... 흥분하신 것 같네요, 선생님.",
           "...당신은 이것에 대해 열정적으로 보입니다, 선생님."],
    'thinking':['흠흠.........',
                '음음........',
                "흠, 알겠어요...",
                "흠, 알겠습니다...",
                "생각 좀...",
                "흠, 흥미롭군요...",
                "음, 아마도..."
                ],
    'undo-ok':['음... 알겠습니다, 선생님, 이번 한 번만.',
               "이번에는 허락하겠습니다, 선생님.",
               "알겠습니다, 선생님, 하지만 이번 한 번만.",
               "음, 이번 한 번만요, 선생님.",
               "음, 특별한 경우입니다, 선생님.",],
    'undo-reject':["아니요, 선생님, 그렇게 하시면 안 됩니다.",
                   "그건 적절하지 않을 것 같습니다, 선생님.",
                   "죄송합니다만, 그건 규칙에 어긋납니다.",
                   "그렇게 할 수 없습니다, 선생님.",
                   "죄송하지만 동의할 수 없습니다.", 
                   "죄송합니다, 선생님.",
                   ],
    'hint-ok':["#이 좋은 선택이 될 것 같습니다.",
               "#을 고려해 보셨나요?",
               "아마도 #이 좋은 생각일 것 같습니다.",
               "#을 고려해보시는 게 좋을 것 같습니다."],
    'hint-reject':[
    "체스에서는 독립적으로 사고하는 것이 중요합니다, 선생님.",
    "체스에서는 스스로 생각하는 법을 익히셔야 합니다, 선생님.",
    "체스에서는 자신의 직관을 따르는 것이 가장 좋은 방법입니다, 선생님.",
    "혼자서 생각하는 것은 체스 실력을 높이는 데 필수적입니다.",
    "잠시만요, 선생님. 생각을 정리할 시간을 주세요.",
    "잠시만요, 선생님. 생각 중입니다.",
    "생각할 시간이 조금 필요합니다, 선생님. 잠시만 기다려주세요.",
    "잠시 생각 중입니다, 선생님."
],

    'hint-disabled':[
    "이건 이제 선생님께서 직접 해결하셔야 합니다.",
    "유감스럽게도 더 이상 힌트를 드릴 수 없네요.",
    "다음 수는 선생님 스스로 알아내셔야 합니다.",
    "이제 힌트 없이도 충분히 해내실 수 있을 것 같습니다, 선생님."
],
    'conversation':["제 이름은 봉클라우드입니다, 선생님. 하지만 샬롯이라고 부르셔도 괜찮아요.",
                    "봉클라우드 공격은 저희 가문에서 수 세기 동안 전해 내려온 전통이랍니다.",
                    "선생님, 오늘도 즐거운 하루 되시길 바랍니다.",
                    "선생님을 받들 수 있어 기쁩니다.",
                    "이 아름다운 날, 선생님과 함께할 수 있어 정말 운이 좋다고 생각합니다.",
                    "선생님, 이보다 더 완벽한 날은 없을 거예요.",
                    "오늘 하루의 아름다움도 선생님께서 저에게 주시는 기쁨에 비하면 희미하게 느껴집니다.",
                    "도움을 드리는 건 기쁘지만, 너무 많은 도움은 드리고 싶지 않아요.",
                    "힌트는 조금 드리겠지만, 너무 많지는 않을 거예요.",
                    "선생님은 제 삶에 빛을 가져다주시는 분이세요.",
                    "선생님과 함께하는 모든 순간이 저에게는 소중합니다.",
                    "선생님이 저와 함께라서 정말로 행복합니다.", 
                   "당신은 제 세상을 더 나은 곳으로 만들어주십니다, 선생님.",
                   "봉클라우드 어택의 아름다움을 이해하고 계신가요?",
                   "봉클라우드 어택에는 대담함과 창의력이 필요합니다.",
                   "저와 함께 플레이해주셔서 감사합니다, 선생님. 좋은 경기가 되길 바랍니다.",
                   "선생님과 대결하게 되어 정말 기쁩니다. 최고의 선수가 되시길 바랍니다!",
                   "즐거운 경기가 되시길, 선생님. 서로 최선을 다합시다.",
                   "이 경기가 기쁨을 가져다주길 바랍니다, 선생님. 우리 둘 다 최선을 다합시다.",
                   "자신을 믿으세요, 선생님, 당신은 위대한 일을 해내실 수 있습니다.",
                   "더 밝은 날이 기다리고 있으니 힘내세요, 선생님.",
                   "이 게임에서뿐만 아니라, 그 너머에서도, 선생님은 위대해질 운명을 지니고 계십니다.",
                   "잠재력이 있으십니다, 선생님. 게임을 당신의 것으로 만드세요!",
                   "당신의 능력을 믿으세요, 선생님.",
                   "자신을 믿으세요, 선생님.",
                   "선생님, 체스판은 당신의 캔버스입니다. 당신의 재능으로 그림을 그려보세요!",
                   "턱을 높이 드세요, 선생님.",
                   "희망을 잃지 마세요, 선생님.",
                   "한 수 한 수를 둘 때마다, 선생님은 기술과 결단력을 보여주고 계십니다.",
                   "당신과 함께 시간을 보내는 것이 제가 원하는 전부입니다.",
                   "제 행복은 선생님과 함께 있는 것입니다.",
                   "저는 선생님과 함께 있을 때 충만함을 느낍니다.",
                   "선생님은 제가 가장 소중히 여기는 분이십니다.",
                   "선생님은 회색 세상 속 제 햇살이십니다.",
                   "당신 가까이에 있는 것만으로도 순수한 행복을 느낍니다.",
                   "선생님과 함께라면, 저는 있어야 할 곳을 찾은 것 같습니다."

                   ],
    'costume':["선생님, 이 옷이 더 마음에 드시나요?",
            "옷을 갈아입었습니다, 선생님. 당신의 세련된 취향에 맞기를 바랍니다.",
            "이 새로운 복장을 어떻게 보시는지 궁금합니다, 선생님.",
            "이 복장이 마음에 드시나요, 선생님?",
            "이 복장이 만족스러우신가요, 선생님?",
            "이 복장에 대해 어떻게 생각하십니까, 선생님?",
            "이 복장을 염두에 두셨나요, 선생님?",
            "선생님의 취향에 맞으신가요?",
            "이 옷이 마음에 드시나요?",
            "이 복장은 만족스러우신가요?",
            "이 새 옷이 마음에 드시기를 바랍니다, 선생님.",
            "이 옷이 선생님의 마음에 들기를 바랍니다."],
    'swap':[
    "선생님, 제가 당신 자리에 가고, 당신은 제 자리에 오시면 어떨까요?",
    "선생님, 제가 선생님을 대신해서 새로운 진행을 보여드리겠습니다.",
    "게임에 흥미로운 반전을 더해드리겠습니다.",
    "흥미를 더해주지 않나요, 선생님?",
    "조금 더 흥미롭게 느껴지지 않으시나요, 선생님?"
],
    'winning':["지금 게임을 하고 싶지 않으신 것 같네요, 선생님."
    ],
    'end':["즐거운 경기였습니다. 선생님. 한 판 더 하시겠어요?",]

}



##대화 스크립트 JP

talkScript_jp = {
    'greeting': [
    "こんにちは、ご機嫌いかがでしょうか？",
    "ごきげんよう、今日お会いできて嬉しいです。",
    "こんにちは。今日はお元気でいらっしゃいますか。",
    "今日お目にかかれて光栄です。",
    "お会いできて嬉しく思います。",
    "本日お会いできて光栄に存じます。"
],
    'praise':[
    "素晴らしい手ですね。",
    "感動的な一手です。",
    "良いアイデアですね、先生！",
    "あなたには才能がありますね、サー。",
    "あなたのプレーに感銘を受けました。",
    "見事なプレーでした、サー。",
    "試合勘が鋭いですね、サー。",
    "あなたの勇気に感動しました。",
    "困難に直面しても、よくプレーされました。",
    "この試合はさらにエキサイティングになりましたね。",
    "あなたにはこのゲームの才能があります。",
    "これからの展開が楽しみです。",
    "あなたの一手一手に目が釘付けです。",
    "あなたはゲームを本当に魅力的にしていますね。",
    "いつもゲームに面白いひねりを加えてくださいますね、先生。",
    "あなたのユニークな試合アプローチに感謝しています。"
],
    'blunder':[
    "ミスは誰にでもありますよ。",
    "問題ありません、どうぞプレーを続けてください。",
    "大丈夫です、続けましょう。",
    "次はきっとうまくいきますよ。",
    "その手は最善の選択ではないかもしれません、サー。",
    "もっと良い手があるかもしれませんね……。",
    "もっと良い手があるかもしれません。",
    "私たちは楽しむためにここにいるんですから。",
    "あなたは私を楽しませてくれていますよ。",
    "心配しないでください、誰にでもあることです。",
    "今日はチェスの駒が自分の意思を持っているようですね。",
    "面白い…選択ですね！",
    "まったく予想外の手でした。",
    "間違いなくゲームチェンジャーです。",
    "私はあなたの技量に畏敬の念を抱いています、サー。",
    "あなたの戦略的な素晴らしさには限りがありませんね！",
    "あなたの創造性に畏敬の念を抱きます。",
    "チェスの魔術師とお呼びしてもよろしいでしょうか？"
],
    'talking':[
    "あなたと過ごす時間はいつも楽しいものです。",
    "いつもお会いするのを楽しみにしています。",
    "あなたの友情に感謝しています。",
    "どうぞお体を大切に。あなたの健康と幸福が何よりも大切です。",
    "チェスは相手の動きを予測する力を養ってくれますよ。",
    "チェスは集中力を高めてくれます。",
    "あなたと過ごす時間はいつも楽しいです、先生。",
    "あなたの存在に感謝しています。",
    "あなたと一緒にいると本当に楽しいです、先生。",
    "あなたと過ごす時間はいつも楽しみです、サー。",
    "今日は本当に良いお天気ですね。",
    "とても素敵な日ですね、サー。",
    "太陽が眩しく輝いていますね。",
    "お互いに切磋琢磨するのに最高の日です。",
    "ゲームにはこれ以上ない天気ですね。",
    "本当にチェス日和ですね。",
    "対局するには絶好の日です。",
    "私の心は、あなたの存在を待ち望んでいます。"
],
    'newgame':[
    "対局を始めるのが待ちきれません。",
    "ゲームを始めましょうか？"
],
    'mate':[
    "申し訳ありませんが、この勝負は私の勝ちのようですね。"
],
    'shy':["...どこで見ているのですか,サー？"
           "...私の女性的な部分にご興味がおありとは...",
           "...あなたの熱心な顔が見えます...",
           "...何をお考えか,お聞かせ願えますか？",
           "何か話したいことはありますか？",
           "...興奮されているようですね,お客様",
           "...熱心なご様子ですね,サー"],
    'thinking':[
    "さてさて、先生……",
    "うーん……",
    "なるほど……わかりました。",
    "そうですね……そういうことですね。",
    "少し考えさせてください……",
    "うーん、興味深いですね……",
    "まあ、おそらく……"
],
    'undo-ok':[
    "わかりました、今回だけ特別に。",
    "今回は許可しましょう。",
    "わかりましたが、今回だけですよ。",
    "今回だけ特別です。",
    "まあ、特別なケースとして今回は認めます。",
    "今回は特別に許可します。"
],
    'undo-reject':[
    "恐れ入りますが、それは適切ではございません。",
    "それは許可できません。",
    "申し訳ありませんが、規則に反します。",
    "それはさせていただくわけには参りません。",
    "申し訳ありませんが、同意しかねます。",
    "残念ですが、ノーと言わざるを得ません。",
    "それはどうしても許可できません。"
],
    'hint-ok':["#は良い選択だと思います。",
    "サー、#を考慮されましたか？",
    "おそらく、#は良いアイデアかもしれませんね。",
    "#を検討されることをお勧めします。"
],
    'hint-reject':[
    "チェスでは自分で考えることを学ばなければなりません。",
    "チェスでは、自分の直感に従うことが最善の方法であることが多いですよ。",
    "自分で考えることは、チェスの上達に欠かせません。",
    "少々お待ちください。考えをまとめますね。",
    "少々お待ちください。ただいま検討中です。",
    "少し考える時間が必要です。少々お待ちください。",
    "少し考えさせてください。"
],
    'hint-disabled':[
    "これ以上ヒントをお出しすることはできません。",
    "次の手を考えるのは、あなた次第です。",
    "これ以上ヒントがなくても、あなたならきっとできると思います。"
],
    'conversation':[
    "シャーロットと呼んでください。",
    "ボンクラウド・アタックは私の家系に何世紀にも わたって受け継がれてきました。",
    "私の家では、ボンクラウド・アタックは 神聖なチェスの一手とされています。",
    "楽しい一日をお過ごしでしょうか？",
    "お役に立てて光栄です。",
    "この美しい一日をあなたと過ごせることを幸運に思います。",
    "サー、あなたとご一緒できるこれ以上完璧な日はありません。",
    "サー、この日の美しさも、あなたが私にもたらす喜びに比べれば、 些細なものです。",
    "ご指導は喜んでいたしますが、あまりお力添えはできません。",
    "ヒントは良いですが、あまり多すぎるのは困りますね。",
    "あなたは私の人生に光を与えてくださいます。",
    "あなたとの一瞬一瞬が私にとっては貴重です。",
    "私の人生にあなたがいてくださって、とても幸せです。",
    "あなたは私の世界をより良い場所にしてくれます。",
    "ボンクラウド・アタックの素晴らしさを理解されていますか？",
    "ボンクラウド・アタックには、大胆さと創造性が必要です、サー。",
    "ボンクラウド・アタックは、 ゲームに興奮と予測不可能性を加えることができますよ。",
    "対戦してくださってありがとうございます、サー。良い試合しましょう。",
    "あなたと対戦するのが楽しみです。最高の選手が勝ちますように！",
    "試合を楽しんでください。ベストを尽くしましょう。",
    "この試合があなたにとって喜びとなりますように。 お互いに全力を尽くしましょう。",
    "自分を信じてください。 あなたは偉大なことができるのですから。",
    "胸を張ってください。 明るい日々が待っていますよ。",
    "この試合でも、その先でも、サー、 あなたは偉大な運命を持っています。",
    "あなたには無限の可能性があります。 このゲームを有利に進めていきましょう！",
    "自分の力を信じてください。",
    "自分を信じてください。",
    "チェス盤はあなたのキャンバスです。 あなたの輝きで描きましょう！",
    "あごを上げてください、サー。",
    "希望を忘れないでください。",
    "一手一手が、あなたの技量と決意を示しています。",
    "あなたと過ごす時間が私の何よりの願いです、サー。",
    "私の幸せは、あなたと一緒にいることです、サー。",
    "あなたと一緒にいると、私は完全になる感じます、サー。",
    "あなたは私にとって最も大切な人です。",
    "あなたは灰色の世界における私の太陽です、先生。",
    "あなたの近くにいることが、私にとって純粋な幸せです。",
],
    'costume':[
    "お直しいたしました。お気に召していただければ幸いです。",
    "この新しい服装をご覧ください。",
    "この服装、お気に召しますか？",
    "この服装でよろしいでしょうか？",
    "この服装について、どう思われますか？",
    "これがあなたのお考えになっていたものですか、サー？",
    "この変更をお認めになりますか、お客様？",
    "お気に召しましたか？",
    "この服装でよろしいでしょうか？",
    "この新しい服装、お気に召しますか、お客様？",
    "お気に召しますでしょうか？"
],
    'swap':[
    "私はあなたの側に立ち、斬新なチェス体験をお届けします。",
    "それは私たちに新たな視点を与え、異なる考え方を促します。",
    "ゲームに面白いひねりを加えてくれますね。",
    "それは少し興奮を追加してくれるでしょう？"
],
    'winning':["今はゲームをしたくないようですね、サー"],
    'end':["楽しい試合でした。もう一局いかがですか？"]
}

talkScript_cn = {
    'greeting': [
    "您好，先生，今天过得怎么样？",
    "您好，先生。",
    "您好，亲爱的先生，很高兴今天见到您。",
    "下午好，先生，希望您今天一切顺利。",
    "今天见到您真是太好了，先生。",
    "您好，先生。",
    "见到您总是让人高兴，先生。",
    "今天您能来真是太好了，先生。"
],
    'praise':[
    "干得好，先生。",
    "真是漂亮的一手，先生！",
    "令人印象深刻的动作，先生！",
    "这是个好主意，先生！",
    "您在这方面很有天赋，先生。",
    "您的表现让我印象深刻，先生。",
    "打得好，先生。",
    "您对比赛很有感觉，先生。",
    "您的勇气让我感动，先生。",
    "比赛变得更加刺激了。",
    "您确实很有比赛天赋。",
    "我很好奇接下来会如何展开。",
    "我很欣赏您独特的比赛方式，先生。"
],
    'blunder':[
    "没问题，先生。继续比赛吧。",
    "没关系，先生。我们继续吧。",
    "下次你一定会成功的，先生。",
    "这一步可能不是最好的选择，先生。",
    "我想可能有更好的选择，先生。",
    "或许你可以考虑换个招数，先生。",
    "毕竟我们是来享受乐趣的。",
    "你真的让我乐在其中。",
    "别担心，这种事我们都会遇到。",
    "看来今天的棋子都有自己的想法呢。",
    "有趣的选择......先生！",
    "真是出乎意料。",
    "我对您的技巧肃然起敬，先生。",
    "您的妙招让我敬佩......您的创造力真是惊人。",
    "我可以称您为象棋奇才吗，先生？"
],
    'talking':[
    "和您在一起总是很愉快，先生。",
    "我总是期待着见到您，先生。",
    "我非常感激您的友谊，先生。",
    "请保重身体，先生。您的健康和幸福对我来说很重要。",
    "国际象棋可以教会您如何预测对手的行动，先生。",
    "国际象棋可以提高您的注意力和专注力，先生。",
    "我总是喜欢和您在一起，先生。",
    "非常感谢您的光临，先生。",
    "和您在一起总是让我感到愉快，先生。",
    "今天天气真好，先生。",
    "今天真是个好天气，先生。",
    "阳光明媚，先生。",
    "今天是进行友谊赛的绝佳日子，先生。",
    "今天的天气非常适合下棋，先生。",
    "我一直在渴望您的到来，先生。"
],
    'newgame':[
    "我已经迫不及待地想开始下棋了，先生。",
    "我们开始游戏吧，先生？"
],
    'mate':[
    "很抱歉，先生，看起来这场比赛是我赢了。"
],
    'shy':['......你在看哪里，先生？',
           "......我不知道您对我的女性部位感兴趣......",
           "......我看到你渴望的脸......",
           "......我能知道你在想什么吗，先生？",
           "......您有什么想说的吗，先生？",
           "......您看起来很兴奋，先生",
           "......您看起来很兴奋，先生。"],
    'thinking':[
    "让我看看，先生……",
    "嗯，好的……",
    "嗯，我明白了……",
    "让我想一想……",
    "嗯，有意思……",
    "嗯，或许有可能……"
],
    'undo-ok':[
    "嗯……好吧，先生，就这一次。",
    "这次我允许，先生。",
    "好吧，先生，就这一次。",
    "好吧，就这一次，先生。",
    "好吧，作为特例，先生。",
    "这一次我就破例允许了，先生。"
],
    'undo-reject':[
    "恐怕这样不合适，先生。",
    "我不能允许，先生。",
    "对不起，先生，这违反规定。",
    "我不能让您这么做，先生。",
    "抱歉，先生，我不能同意。",
    "恐怕我不得不拒绝，先生。",
    "这不是我能允许的，先生。"
],
    'hint-ok':[
    "先生，您考虑过 # 吗？",
    "也许 # 是个不错的主意，先生。",
    "我建议您考虑 #，先生。"
],
    'hint-reject':[
    "下棋时要学会独立思考，先生。",
    "在国际象棋中，遵循自己的直觉往往是最好的选择，先生。",
    "独立思考是提高棋艺的关键，先生。",
    "请稍等，先生。让我整理一下思路。",
    "请给我一点时间，先生，我正在思考。",
    "我需要一点时间来考虑，先生，请稍等。",
    "我需要一点时间来思考，先生。"
],
    'hint-disabled':    ["恐怕我不能再给您任何提示了，先生。",
    "接下来的步骤就靠您自己了，先生。",
    "我相信您无需更多提示也可以做到，先生。"
],
    'conversation':[
    "奉云攻击在我的家族中已经传承了几个世纪，先生。",
    "在我们家族，奉云攻击被视为神圣的棋步。",
    "希望您今天过得愉快，先生。",
    "我相信您今天一定过得很愉快，先生。",
    "为您服务是我的荣幸，先生。",
    "先生，我想象不出还有比这更完美的一天了。",
    "先生，与您带给我的快乐相比，今天的美丽显得微不足道。",
    "先生，我很乐意为您提供指导，但不想给您太多帮助。",
    "提示是好的，但不要太多，先生。",
    "您为我的生活带来了光明，先生。",
    "和您在一起的每一刻都弥足珍贵，先生。",
    "有您在我的生命中，我感到很幸运，先生。",
    "您让我的世界更加美好，先生。",
    "您了解奉云攻击的魅力吗？",
    "奉云攻击需要勇气和创造力，先生。",
    "奉云攻击可以为您的游戏增添刺激和不可预测性，先生。",
    "感谢您与我对弈，先生。希望我们能有一场精彩的比赛。",
    "请尽情享受比赛吧，先生。让我们全力以赴。",
    "愿这场比赛给您带来快乐，先生。让我们全力以赴。",
    "相信自己，先生，您有能力成就伟大的事情。",
    "振作起来，先生，光明的日子在等着您。",
    "无论在比赛中还是之后，先生，您注定会成就伟大。",
    "您有无限的潜力，先生。让比赛为您所掌控。",
    "相信自己的能力，先生。",
    "相信自己，先生。",
    "先生，棋盘就是您的画布。",
    "先生，棋盘就是您的画布，用您的才华去描绘它吧！",
    "抬起头来，先生。",
    "怀抱希望，先生。",
    "先生，您的每一步都展现了您的技巧和决心。",
    "和您在一起是我唯一的愿望，先生。",
    "我的幸福就是和您在一起，先生。",
    "您是我灰暗世界里的阳光，先生。",
    "在您身边就是纯粹的幸福，先生。",
    "和您在一起，我找到了归属，先生。"
],
    'costume':[
    "先生，您觉得这身衣服合适吗？",
    "我已经修改过了，先生。希望能符合您的品味。",
    "先生，请您评价一下这身新装。",
    "您喜欢这身打扮吗，先生？",
    "您对这套服装满意吗，先生？",
    "您觉得这套服装怎么样，先生？",
    "这是您想要的吗，先生？",
    "这符合您的品味吗，先生？",
    "这套服装您满意吗，先生？",
    "这身新装让您满意吗，先生？",
    "希望这能让您满意，先生。"
],
    'swap':[
    "先生，我站在您这边，您也站在我这边。",
    "这让我们学会适应和换位思考。",
    "这为比赛增添了有趣的转折。",
    "这是不是增添了一丝刺激呢？"
],
    'winning':[
    "看起来您现在不太想下棋了，先生。"
],
'end':[
"这是一场愉快的比赛。您想再来一局吗？"]
}

### 대화 스크립트 끝






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
    "Jazz.mp3":"""George Street Shuffle by Kevin MacLeod | https://incompetech.com/
Creative Commons Creative Commons: By Attribution 3.0 License
http://creativecommons.org/licenses/by/3.0/
    """,
    "Sakuya.mp3":""" Sakuya by PeriTune | https://peritune.com/
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/4.0/
"""    
}

musicSheet = {"Calm":'peaceful.mp3',"Jazz":"Jazz.mp3","Japan":"Sakuya.mp3"}
costumeSheet = {"Normal":"lady_bongcloud.png","Bunny":"lady_bongcloud_bunny.png","Beast":"lady_bongcloud_beast.png"}
languageSheet = {"English":"en","日本語":"jp","中文":"cn","한국어":"kr"}
modeSheet = {"FullScreen":True,"Window":False}
musicVolumeSheet = {"Jazz.mp3":0.6,"Sakuya.mp3":0.1} #음량 조절용 시트
ratingSheet = {"Beginner":600,"Intermediate":1200,"Advanced":1800,"Expert":2400}

default_screen_size = (1920,1080)
window =Rs.new(REMOGame)

class Obj():
    stockfish_hint = Stockfish(path=stockFishPath,parameters={"Threads":2}) ## Stockfish로 힌트를 주는 AI
    stockfish_play = Stockfish(path=stockFishPath,parameters={"Threads":2}) ## Stockfish로 게임을 하는 AI
    game_geometry = copy.deepcopy(game_geometry_n)
    board = chess.Board()
    thinkOfAI = ""
    think = 'chessgame-ai.think'
    hint = 'chessgame-ai.hint'
    configPath = 'chessgame.config'
    default_config = {"Resolution":1080,"FullScreen":False,"Music":"peaceful.mp3","Costume":"lady_bongcloud.png",
                      "Rating":ratingSheet["Intermediate"],"UserIsWhite":False,"Swapped":False,"Volume":1.0,
                      "HintCount":0,"Board":chess.Board(),"PGN":""} # config 정보를 저장
    config = {}
    AIcondition = 0.3
    hintCountMax = 4
    pieceVolume={"P":0.2,"N":0.5,"B":0.5,"R":0.7,"Q":1} ## 피스가 죽을 때 내는 볼륨
    heart = "♥"
    emptyHeart = "♡"
    cursor = Rs.new(imageObj)
    talkscripts = {"en":talkScript,"kr":talkScript_kr,"jp":talkScript_jp,"cn":talkScript_cn} ## 대화 스크립트 모음
    
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
    

    ##체스 레이팅을 가져오는 함수
    @classmethod
    def getChessRating(cls):
        try:
            return Obj.config["rating"]
        except:
            Obj.config["rating"] = ratingSheet["Intermediate"]
            return Obj.config["rating"]

##힌트를 생성하는 프로세스    
def stockFishHintProcess(fen,path,rating):
    stockfish = Obj.stockfish_hint
    print("params",stockfish.get_parameters())
    stockfish.set_fen_position(fen)
    l = stockfish.get_top_moves(3)
    if len(l)>0:
        bestMove = l[0]
        makeAIHintData(bestMove["Move"],fen,path=Obj.hint)


##스톡피쉬를 이용한 AI 체스 프로세스
def stockFishProcess(time,fen,path,bongcloudOpened,isBestMode,rating):
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
    stockfish = Obj.stockfish_play
    if random.random()>Obj.AIcondition:
        stockfish.set_elo_rating(rating)
    else: # Dojitko Move
        stockfish.set_elo_rating(1000)
    stockfish.set_fen_position(fen)
    
    eval = stockfish.get_evaluation()
    tMoves = stockfish.get_top_moves(5)
    tMoves = tMoves[::-1]
    move = ""



    b = chess.Board(fen)
    ##봉클라우드를 위해 킹이 되돌아가는 무브를 제거한다.
    _topMoves=[]
    for move in tMoves:
        m = move["Move"]
        if Obj.checkKingBack(b,m):
            continue
        else:
            _topMoves.append(move)


    if _topMoves==[]: #왕이 튀는거 말곤 답이 없는 상황일때
        if len(tMoves)>0:
            move = tMoves[-1] # Make Best Move
            makeAIData(move,eval=eval,topMoves=_topMoves)
            return
        else: ## Ai 움직일 수 없음 (체크메이트 상태)
            move = "resign" # Make Best Move
            makeAIData(move,eval=eval,topMoves=_topMoves)
            return


    if bongcloudOpened:
        move = tMoves[-1]
        b_move = stockfish.get_best_move()
        move["Move"] = b_move
        if not Obj.checkKingBack(chess.Board(fen),b_move):
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
    cur_lang = "en"
    fenToSprite = 'KQBNRPkqbnrp' # fen과 sprite index를 대응하는 표    
    tileSize = 100
    @classmethod
    def playMusic(cls,m):
        try:
            if m in musicVolumeSheet:
                volume = musicVolumeSheet[m]
            else:
                volume = 1
            Rs.playMusic(m,volume=volume)
            configScene.credit.text = credit + musicCredits[Rs.currentMusic()]
        except:
            mainScene.playMusic("Jazz.mp3")
        
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

    def initUI(self):

        font = self.getFont()


        self.rematchButton.text = UI_words["rematch"][mainScene.cur_lang]
        self.helpButton.text = UI_words["help"][mainScene.cur_lang]
        self.configButton.text = UI_words["config"][mainScene.cur_lang]
        self.exitButton.text = UI_words["exit"][mainScene.cur_lang]
        self.swapButton.text = UI_words["swap"][mainScene.cur_lang]
        self.undoButton.text = UI_words["undo"][mainScene.cur_lang]
        self.hintButton.text = UI_words["hint"][mainScene.cur_lang]
        self.rematchBlackButton.text = UI_words["black"][mainScene.cur_lang]
        self.rematchWhiteButton.text = UI_words["white"][mainScene.cur_lang]

        ##메인 UI 관련 버튼 폰트 초기화
        for button in [self.rematchButton,self.helpButton,self.configButton,self.exitButton,self.swapButton,self.undoButton,self.hintButton,self.rematchBlackButton,self.rematchWhiteButton]:
            button.textObj.font = font
            button.textObj.center = button.geometryCenter-button.geometryPos
            button.update()

        #기타 버튼 폰트 초기화
        for button in [self.turnButton]:
            button.textObj.font = font
            button.textObj.center = button.geometryCenter-button.geometryPos
            button.update()

        self.conversationList = list(self.getTalkScript()['conversation']) ## 대화 리스트를 초기화한다.
        random.shuffle(self.conversationList)

        self.updateTurnText()

    
    def initChessObj(self):
        self.chessObjs={}
        for code in mainScene.fenToSprite:
            for _ in range(20):
                self.makeChessObj(code)
                self.progress+=0.3
            
    
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
        if mainScene.cur_lang=='cn':
            size += 5 ## 중국어는 한자가 작아서 크기를 더 키워준다.
        width = Obj.game_geometry['talk']['TextWidth']
        self.talkObj = longTextObj(sentence,geometry,size=size,textWidth=width,font=self.getFont())
        self.talkBgObj = rectObj(self.talkObj.boundary.inflate(size*2,size*2),color=Cs.black)
        self.talkObj = longTextObj("",geometry,size=size,textWidth=width,font=self.getFont())
        self.talkObj.alpha=255
        self.talkBgObj.alpha = 0


        ##언어에 따라 대화창의 지속 시간을 조절한다.
        if mainScene.cur_lang=='en':
            l = 3
        elif mainScene.cur_lang=='jp':
            l = 17
        elif mainScene.cur_lang=='cn':
            l = 17
        else:
            l = 4
        self.talkTimer = min(100,len(sentence)*l)
        
        None

    def makeCoordinate(self):
        coordinateX = 'abcdefgh'
        if not Obj.config["UserIsWhite"]:
            coordinateX=coordinateX[::-1]
        temp = []
        for c in coordinateX:
            obj = textButton(c,pygame.Rect(0,0,Obj.game_geometry['board']['TileSize'],Obj.game_geometry['board']['TileSize']//2),hoverMode=False,color=Cs.black,alpha=255)
            temp.append(obj)
        pos = self.boardDisplay.pos+RPoint(0,Obj.game_geometry['board']['TileSize']*8)
        self.coordinateXObj = layoutObj(pos=pos,spacing=0,isVertical=False,childs=temp)
        
        coordinateY = '12345678'
        if Obj.config["UserIsWhite"]:
            coordinateY=coordinateY[::-1]
        temp = []
        for c in coordinateY:
            obj = textButton(c,pygame.Rect(0,0,Obj.game_geometry['board']['TileSize']//2,Obj.game_geometry['board']['TileSize']),hoverMode=False,color=Cs.black,alpha=255)
            temp.append(obj)
        pos = self.boardDisplay.pos+RPoint(-50,0)
        self.coordinateYObj = layoutObj(pos=pos,spacing=0,childs=temp)

    ##현재 필요한 폰트를 반환하는 함수
    def getFont(self):
        if mainScene.cur_lang=='cn':
            return 'chinese_button.ttf'
        elif mainScene.cur_lang=='jp':
            return 'japanese_button.ttf'
        else:
            return 'korean_button.ttf'
        
    ##현재 필요한 대화 스크립트를 반환하는 함수
    def getTalkScript(self):
        return Obj.talkscripts[mainScene.cur_lang]

        
    def makeTurnButton(self):
        currentColor = Obj.config["Board"].fen().split()[1]
        if self.currentColor != currentColor:
            self.currentColor = currentColor
            number = Obj.config["Board"].fullmove_number
            if currentColor=='w':
                number = 2*number-1
            else:
                number = 2*number
            turnText = UI_turn["turn"][mainScene.cur_lang] +" "+str(number)+', '
            if self.isUserTurn():
                t = UI_turn["my-turn"][mainScene.cur_lang]
            else:
                t = UI_turn["lady-turn"][mainScene.cur_lang]
            
            if currentColor=='w':
                c = [Cs.white,Cs.black]
            else:
                c = [Cs.black,Cs.white]
            self.turnButton = textButton(turnText+t,Obj.game_geometry['button']['button2'],color=c[0],fontColor=c[1],hoverMode=False,font=self.getFont())    
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
        REMODatabase.saveData(Obj.configPath,Obj.config)

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
                self.hintProc = Process(target=stockFishHintProcess,args=(Obj.config["Board"].fen(),stockFishPath,Obj.getChessRating()))
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
                    try:
                        move = data['Move']['Move']
                        cur_cp = data['Move']['Centipawn']
                        mate = data['Move']['Mate']
                        winning = False
                    except:
                        return
                    if move == 'resign': ## AI 패배
                        return

                    if cur_cp != None and abs(cur_cp)>800 and not Obj.config["Swapped"]:
                        self.swappedColorTimer=25 ## 컬러스왑 불가
                        Obj.config["Swapped"]=True
                        if not self.ladyBestMode:
                            self.ladySays(random.choice(self.getTalkScript()['winning']))
                        winning = True

                    if not self.ladyIsOnMate and mate!=None:
                        if self.currentColor=='w':
                            ladyWinning = 1
                        else:
                            ladyWinning = -1
                        if mate==ladyWinning:
                            self.ladyIsOnMate = True
                            self.swappedColorTimer=25 ## 컬러스왑 불가
                            Obj.config["Swapped"]=True
                            self.ladySays(random.choice(self.getTalkScript()['mate']))
                            self.playVoice("talk-checkmate.wav",0.5)
                
                    if 'e1' in move or 'e8' in move or Obj.config["Board"].fullmove_number>3:
                        self.bongcloudOpened = True #King Moved or too late to bongcloud


                    ##잦은 버그가 발생하는 코드. 임시방편으로 때워야 겠다....
                    ##임시방편으로 때워도 안됨. TODO: 디버깅 필요
                    try:
                        self.lastChessObj = self.moveByString(move)
                    except:
                        makeAIData("")
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
                            if random.random()<r and not winning:
                                if random.random()<0.7:
                                    self.ladySays(random.choice(self.getTalkScript()['praise']))
                                    praiseVoice = random.choice(['talk-praise1.wav','talk-praise2.wav','talk-praise3.wav'])
                                    self.playVoice(praiseVoice,0.5)
                        elif check_better<-100:
                            #Lady가 실제로 응징하거나, 일정확률로 블런더 출력
                            if not winning:
                                if abs(cp-cur_cp)<30 or random.random()<0.2:
                                    if random.random()<0.7:
                                        self.ladySays(random.choice(self.getTalkScript()['blunder']))
                                        self.playVoice('talk-blunder1.wav',0.5)
                                    self.showSmile=True
                        
                    Rs.playSound('move-chess.wav',volume=0.3)
                    self.ladyHandTimer=30
                    makeAIData("")
                    self.proc = None
                else:
                    makeAIData("")
        else:
            c = (Obj.config["Board"].fullmove_number/200.0)
            if random.random()<c:
                self.ladyBestMode = True # 턴이진행될수록 bestMode 진입확률 증가
            self.proc = Process(target=stockFishProcess,args=(1000,Obj.config["Board"].fen(),stockFishPath,self.bongcloudOpened,self.ladyBestMode,Obj.getChessRating()))
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
    
    def playVoice(self,fileName,volume):
        if self.voice:
            self.voice.stop()
        self.voice = Rs.playSound(fileName,volume=volume*0.5)


    def initOnce(self):
        self.voice = None # Lady Voice
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
        try:
            mainScene.cur_lang = Obj.config["language"]
        except:
            mainScene.cur_lang = "en"
                
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
        self.conversationList = list(self.getTalkScript()['conversation'])
        random.shuffle(self.conversationList)
        self.raiseRematch = False
        random.shuffle(self.getTalkScript()['talking'])

        self.talkTimer = 0
        self.aiWait = 0 # AI가 기다리는 시간
        self.talkTicker = time.time() # TalkTimer 조절용 인수
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
        self.lastMovedObj.rect = self.boardDisplay[0][0].rect.inflate(-10,-10)
        self.lastMovedObj.center = self.boardDisplay[0][0].center
        self.lastMovedObj.alpha = 50

        self.hoverObj = rectObj(self.boardDisplay[0][0].rect,color=Cs.yellow)
        self.hoverObj.alpha = 60
        

        #Init Lady Sprites# 
        ladyGeometry= Obj.game_geometry['lady']
        try:
            mainScene.ladyObj = imageObj(Obj.config["Costume"],pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])
        except:
            mainScene.ladyObj = imageObj("lady_bongcloud.png",pos=ladyGeometry['Pos'],scale=ladyGeometry['Scale'])

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
        self.bgPatternObj = imageObj('chess-room-3.jpg',pos=(0,0))
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
                self.raiseRematch = False
                Obj.config["UserIsWhite"] = colorIsWhite
                self.makeBoard(False)
                Rs.playSound('chess-rematch.wav',volume=0.6)
                self.swappedColorTimer = -1 ## 컬러스왑한 사실을 없앰
                Obj.config["Swapped"]=False
                Obj.config["HintCount"]=0
                self.updateHintCounter()
                self.hintCoolTime=125
                self.swapButton.fontColor = Cs.white
                self.ladySays(random.choice(self.getTalkScript()['newgame']))
                self.playVoice("talk-newgame.wav",volume=0.5)
                Obj.renewCondition()
                self.ladyBestMode = False
            return f
        self.rematchBlackButton.connect(rematch(False))
        self.rematchWhiteButton.connect(rematch(True))
        self.rematchButtonLayout = layoutObj(pos=Obj.game_geometry['button']['pos1'],childs=[self.rematchBlackButton,self.rematchWhiteButton],isVertical=False)
        for button in self.rematchButtonLayout.childs:
            button.alpha =0
            
        self.hintButton = textButton(UI_words["hint"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.hexColor("FB8DA0"))
        self.hintCounterObj = textObj("")
        if Obj.config["HintCount"]>Obj.hintCountMax:
            self.hintButton.fontColor = (160,160,160)
        def getHint():
            if self.hintCoolTime==0 and self.showHint == False and self.isUserTurn():
                if Obj.config["HintCount"]>Obj.hintCountMax:
                    self.ladySays(random.choice(self.getTalkScript()['hint-disabled']))
                else:
                    if self.aboutHint["Fen"] == Obj.config["Board"].fen() and self.aboutHint["Move"]!=None:
                        words = random.choice(self.getTalkScript()['hint-ok'])
                        words = words.replace('#',self.aboutHint["Move"])
                        self.showHint = True
                        self.ladySays(words)
                        hintVoice = random.choice(['talk-hintOk.wav','talk-hintOk2.wav'])
                        self.playVoice(hintVoice,volume=0.5)
                        Obj.config["HintCount"]+=1
                        self.updateHintCounter()

                        mainScene.saveConfig()
                    else:
                        self.ladySays(random.choice(self.getTalkScript()['hint-reject']))
                self.hintCoolTime=127
        self.hintButton.connect(getHint)
        self.undoButton = textButton(UI_words["undo"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.hexColor("EFD3B5"))        
        self.rematchButton = textButton(UI_words["rematch"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.hexColor("A47551"))
        #게임중에 색을 바꿔서 플레이
        self.swapButton = textButton(UI_words["swap"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.dark(Cs.grey))
        if Obj.config["Swapped"]:
            self.swapButton.fontColor= Cs.black
        # 재경기 의사를 표현한다.
        def raise_rematch():
            if not self.raiseRematch:
                scripts = {'en':"Which color do you want to play?","kr":"어떤 색으로 게임을 하시겠습니까?","jp":"どの色でプレイしますか？","cn":"您想玩什么颜色？"}
                self.ladySays(scripts[mainScene.cur_lang])
                self.playVoice("talk-colorChange.wav",volume=0.5)
            else:
                self.raiseRematch = True
                scripts = {'en':"Oh, Ok.","kr":"알겠어요.","jp":"わかりました。","cn":"好的。"}
                self.ladySays(scripts[mainScene.cur_lang])
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
                self.ladyBestMode = True
                Rs.playSound('chess-rematch.wav')
                self.ladySays(random.choice(self.getTalkScript()['swap']))
                self.playVoice("talk-swap.wav",volume=0.55)
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
                    self.ladySays(random.choice(self.getTalkScript()['undo-ok']))
                    self.undoCounter=min(1,self.undoCounter+random.random()*0.5)
                else:
                    self.ladySays(random.choice(self.getTalkScript()['undo-reject']))
                    self.undoCounter=max(0,self.undoCounter*0.5)
                self.undoCoolTime = 127

        self.undoButton.connect(undoMove)

        self.exitButton = textButton(UI_words["exit"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.dark(Cs.red))
        self.exitButton.connect(REMOGame.exit)

        self.conversationButton = imageButton("speech_icon.png",Obj.game_geometry['button']['talkButton'])
        self.conversationButton.alpha = 200
        self.lastTalkedIndex = -1 # 마지막으로 말한 대사의 인덱스
        def conversation():
            if self.talkTimer==0:
                if len(self.conversationList)>0:
                    self.ladySays(self.conversationList.pop())
                    wavList = ['talk-talking1.wav','talk-talking2.wav','talk-talking3.wav']
                    talking = random.randint(0,len(wavList)-1)
                    while self.lastTalkedIndex == talking:
                        talking = random.randint(0,len(wavList)-1)
                    self.playVoice(wavList[talking],volume=0.5)            
                    self.lastTalkedIndex = talking        
                else:
                    self.conversationList = list(self.getTalkScript()['conversation'])
                    random.shuffle(self.conversationList)
                    
                    
        self.conversationButton.connect(conversation)

        self.progress = 100

        spacing = Obj.game_geometry['board']['TileSize']//10

        self.buttonLayout = layoutObj(pos=Obj.game_geometry['button']['pos2'],childs=[self.hintButton,self.undoButton,self.rematchButton,self.swapButton],spacing=spacing)
        t = Obj.game_geometry['board']['TileSize']
        self.hintCounterObj.center = self.hintButton.geometryCenter+RPoint(-t//2,-t//3)
        self.updateHintCounter()
        self.configButton = textButton(UI_words["config"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.hexColor("9DB6CC"))

        self.configIcon = imageObj("setting_icon.png",pos=(30,30),scale=0.07) ## 설정 아이콘
        self.configIcon.setParent(self.configButton)
        self.configIcon.center = RPoint(30,23)
        
        self.configButton.connect(configScene.turnToConfig)
        
        self.helpButton = textButton(UI_words["help"][mainScene.cur_lang],Obj.game_geometry['button']['button1'],color=Cs.red)
        def showHelp():
            Rs.setCurrentScene(Scenes.helpScene)
        self.helpButton.connect(showHelp)


        self.buttonLayout2 = layoutObj(pos=Obj.game_geometry['button']['pos3'],childs=[textObj("system",color=Cs.black,size=Obj.game_geometry['sys']['ButtonFontSize']),self.configButton,self.helpButton,self.exitButton],spacing=spacing)

        self.debugObj = longTextObj('',pos=(0,0),textWidth=200)
        
        self.makeTurnButton()

        if Obj.config["PGN"]!="":
            lastMove = Obj.config["PGN"].split()[-1]



        self.turnButtonTimer = 0
        
        self.ladySays(random.choice(self.getTalkScript()['greeting']))
        self.playVoice('talk-greeting1.wav',volume=0.5)


        mainScene.playMusic(Obj.config["Music"])

        makeAIData("")
        
        self.isBuffering=False

        self.ladyRect = rectObj(pygame.Rect(1410,100,240,630)) # Lady가 있는 위치. 클릭시 대화 재생

        self.initUI()

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
    
    ## 턴에 관련된 텍스트를 초기화한다.
    def updateTurnText(self):
        number = Obj.config["Board"].fullmove_number
        if self.currentColor=='w':
            number = 2*number-1
        else:
            number = 2*number

        turnText = UI_turn["turn"][mainScene.cur_lang]+" "+str(number)+', '
        
        if Obj.config["Board"].is_checkmate():
            t = UI_turn["checkmate"][mainScene.cur_lang]
            self.ladySays(random.choice(self.getTalkScript()['end']))
        elif Obj.config["Board"].is_stalemate():
            t = "Stalemate"
            self.ladySays(random.choice(self.getTalkScript()['end']))
        elif Obj.config["Board"].is_variant_draw():
            t = "Draw"
            self.ladySays(random.choice(self.getTalkScript()['end']))
        else:
            if self.isUserTurn():
                t = UI_turn["my-turn"][mainScene.cur_lang]
            else:
                t = UI_turn["lady-turn"][mainScene.cur_lang]

        if Obj.config["Board"].is_check() and number>1:
            ##체크인 경우 소리를 나게 한다.
            Rs.playSound('check-sound.wav',volume=0.3)

            ##체크인 경우 빨갛게 체크 당한 왕에게 애니메이션을 준다.
            obj = Rs.copy(self.chessObjs['k'][0])
            obj.colorize(Cs.red)

            if self.currentColor == 'w':
                c = chess.WHITE
            else:
                c = chess.BLACK

            k_pos =Obj.config["Board"].king(c)
            x,y = self.chessPosToPos(chess.square_name(k_pos))
            obj.pos= self.boardDisplay[y][x].geometryPos
            Rs.fadeAnimation(obj,time=250,alpha=150)
            

        self.turnButton.text = turnText+t

    

    def update(self):
        if Rs.userJustPressed(pygame.K_ESCAPE):
            configScene.turnToConfig()
        if mainScene.changedCloth:
            mainScene.changedCloth=False
            self.ladySays(random.choice(self.getTalkScript()['costume']))
            self.playVoice("talk-costume.wav",volume=0.6)
        self.isHovering=False
        if self.isUserTurn():
            self.aiMakeHint()                
            if Rs.userJustLeftClicked() and self.promotionGUI:
                for c in self.promotionGUI.childs:
                    if c.collideMouse():
                        s = self.promotionKey+c.code
                        self.moveByString(s)
                        Rs.playSound('move-chess.wav',volume=0.4)
                        self.hoverObj.setParent(None)
                        if self.talkTimer==0 and random.random()<0.2:
                            self.ladySays(random.choice(self.getTalkScript()['thinking']))
                            self.playVoice('talk-thinking1.wav',0.5)
                            
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
                                        self.promotionBoard = rectObj(pygame.Rect(0,0,t,4*t).inflate(t//2,t//2))
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
                                        Rs.playSound('move-chess.wav',volume=0.5)
                                        self.hoverObj.setParent(None)
                                        if self.talkTimer==0 and random.random()<0.2:
                                            self.ladySays(random.choice(self.getTalkScript()['thinking']))
                                            self.playVoice('talk-thinking1.wav',0.5)

                                        self.aiWait=random.randint(50,150)
                                    
                                        
                                        
                                        
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
            if self.aiWait>0:
                self.aiWait-=1
            else:
                self.aiMove()
        
        #체스말 부드럽게 움직이기 위한 코드
        if self.lastMovedObj != None and self.lastMovedObj.pos != RPoint(0,0):
            arrival =RPoint(Obj.game_geometry['board']['TileSize']//2,Obj.game_geometry['board']['TileSize']//2)
            self.lastMovedObj.center = (self.lastMovedObj.center-arrival)*0.8+arrival
            if hasattr(self.lastMovedObj.parent,"chessObj"):
                self.lastMovedObj.parent.chessObj.center = (self.lastMovedObj.center-arrival)*0.7+arrival
                if self.lastMovedObj.parent.chessObj.center.distance(arrival)<5:
                    self.lastMovedObj.parent.chessObj.center = arrival
        
        ##Turn Button Color Change ##
        curColor = Obj.config["Board"].fen().split()[1]
        if self.currentColor !=curColor:
            self.currentColor = curColor
            self.updateTurnText()
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
            if random.random()<0.0001:
                if len(self.getTalkScript()['talking'])>0:
                    self.ladySays(self.getTalkScript()['talking'].pop())
        if random.random()<0.001:
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
                button.alpha = min(200,button.alpha+20)
                
            self.rematchButtonLayout.update()
        else:
            for button in self.rematchButtonLayout.childs:
                button.alpha = max(0,button.alpha-20)

        self.buttonLayout.update()
        self.buttonLayout2.update()
        if self.talkTimer<25:
            self.conversationButton.update()
        if self.promotionGUI:
            self.promotionGUI.update()

            
        ## DEBUG ##

        if self.ladyRect.isJustClicked():
            self.conversationButton.func()

        if Rs.userJustLeftClicked():
            print(Rs.mousePos())
        self.debugObj.pos = Rs.mousePos()+RPoint(20,20)
        self.debugObj.text = str(Rs.mousePos()) ## DEBUG
        Obj.cursor.pos = Rs.mousePos()

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
        Rs.acquireDrawLock()

        self.chessTableObj.draw()
        self.chessBackObj.draw()
        self.coordinateXObj.draw()
        self.coordinateYObj.draw()
        self.boardDisplay.draw()
        
        Rs.releaseDrawLock()        
        
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
        self.buttonLayout.draw()
        if self.hintButton.collideMouse():
            self.hintCounterObj.draw()
        self.buttonLayout2.draw()
        if self.talkTimer<25:
            self.conversationButton.draw()
        self.rematchButtonLayout.draw()
        

        if self.talkTimer>0:

            if time.time()-self.talkTicker>1/30:
                self.talkTicker=time.time()

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
        Obj.cursor.draw()


        return

class configScene(Scene):

    ##리팩토링 필요성에 의해 새로 짠 버튼레이아웃 함수
    def makeButtonLayout(self,sheet,curState,settingFunc):
        '''
        sheet: 버튼에 연결될 옵션 {'옵션명':옵션값}
        curState: 현재 옵션 설정 상태
        settingFunc: 버튼을 눌렀을 때 실행할 함수. 인자로 선택된 옵션을 받는다.
        settingFunc(sheet,option)
        '''

        t = Obj.game_geometry['board']['TileSize']

        ##버튼 레이아웃 생성##
        layout = layoutObj(pygame.Rect(0,0,t//2,t//2),isVertical=False)
            

        ##버튼 생성##
        for option in sheet:

            ##선택된 옵션은 색을 진하게, 선택되지 않은 옵션은 밝게
            if sheet[option] == curState:
                _color = Cs.dark(Cs.tiffanyBlue)
                _hoverMode = False
            else:
                _color = Cs.tiffanyBlue
                _hoverMode = True


            button = textButton(str(option),Obj.game_geometry['button']['button1'],color=_color,hoverMode=_hoverMode)
                
            ##함수 제너레이터
            def f(_sheet,_option):
                def _():
                    Rs.acquireDrawLock()
                    settingFunc(_sheet,_option) ##옵션 설정 함수 실행
                    for button in layout.childs:
                        ##선택된 버튼은 색을 진하게, 선택되지 않은 버튼은 밝게
                        if button.text == str(_option):
                            button.color = Cs.dark(Cs.tiffanyBlue)
                            button.hoverMode = False
                        else:
                            button.color = Cs.tiffanyBlue
                            button.hoverMode = True
                    Rs.releaseDrawLock()
                    mainScene.saveConfig() ##설정 저장
                return _
            button.connect(f(sheet,option))
            button.setParent(layout)

        return layout
    def initOnce(self):
        ##TODO: Make Config Scene Objects ##
                
        t = Obj.game_geometry['board']['TileSize']
        w,h = Rs.screen.get_rect().size
        self.blackBoard = rectObj(Rs.screen.get_rect().inflate(-t,-t),color=Cs.black,alpha=200)
        self.configLabel = textObj("Config",pos=(t*2,t),size=t//3)
        configScene.configBackButton = textButton("Go Back",pygame.Rect(w-4*t,h-2*t,t*2,t),color=Cs.grey,fontColor=Cs.black)
        def configBack():
            #TODO: config 상태 저장
            mainScene.saveConfig()
            mainScene.freezeTimer=10
            Rs.setCurrentScene(Scenes.mainScene)
        configScene.configBackButton.connect(configBack)
        configScene.configBackButton.alpha = 225
        

        ##게임 크레딧
        self.creditButton = textButton("credit",Obj.game_geometry["credit"]["Button"],color=Cs.black,fontColor=Cs.grey,alpha=100)
        self.showCredit = False
        def show():
            self.showCredit = not self.showCredit
        self.creditButton.connect(show)
        
        configScene.credit = longTextObj(credit,Obj.game_geometry["credit"]["Pos"],textWidth=Obj.game_geometry['board']['TileSize']*6,color=Cs.grey)
        ###


        ###
        ##해상도 조절 관련 오브젝트
        self.resolutionLabel = textObj("Resolution",size=20)
        resolutionSheet = {x:int(x*1080/1920) for x in [1080,1440,1920,2560]}
        def setResolution(sheet,option):
            Obj.config["Resolution"]=sheet[option]
            Rs.setWindowRes((option,sheet[option]))
        try:
            cur_res = Obj.config["Resolution"]
        except:
            cur_res = 1920
        #해상도 버튼 레이아웃 생성#
        self.resolutionLayout = self.makeButtonLayout(resolutionSheet,cur_res,setResolution)

        ###


        
        ###        
        ##풀스크린 조절 오브젝트
        self.modeLabel = textObj("Game Mode",size=20)
        def setScreenMode(sheet,option):
            Obj.config["FullScreen"]=sheet[option]
            Rs.setFullScreen(sheet[option])
        self.modeLayout = self.makeButtonLayout(modeSheet,Rs.isFullScreen(),setScreenMode)
        ###
        
        ##음악 볼륨 조절 기능
        self.musicVolumeLabel = textObj("Music Volume",size=20)
        configScene.musicVolumeSlider = sliderObj(RPoint(0,0),length=4*t,isVertical=False,value=Rs.getVolume(),color=Cs.aquamarine)
        def musicVolumeUpdate():
            Rs.setVolume(configScene.musicVolumeSlider.value)
            Obj.config["Volume"] = configScene.musicVolumeSlider.value
        configScene.musicVolumeSlider.connect(musicVolumeUpdate)

        self.SEVolumeLabel = textObj("SE Volume",size=20)
        configScene.SEVolumeSlider = Rs.SEVolumeSlider(RPoint(0,0),length=4*t,thickness=10,isVertical=False,color=Cs.orange)
        
        
        ###
        ##음악 선택 기능
        self.muslcSelectionLabel = textObj("Select Music",size=20)
        def setMusic(sheet,option):
            mainScene.playMusic(sheet[option])
            Obj.config["Music"]=sheet[option]
        self.musicSelectionLayout = self.makeButtonLayout(musicSheet,Obj.config["Music"],setMusic)
        ###


        
        ##코스튬 선택 기능
        self.costumeLabel = textObj("Costume",size=20)
        def setCostume(sheet,option):
            mainScene.ladyObj.setImage(sheet[option])
            Obj.config["Costume"]=sheet[option]
            mainScene.changedCloth=True
        self.costumeSelectionLayout = self.makeButtonLayout(costumeSheet,Obj.config["Costume"],setCostume)



        ##언어 선택 기능
        self.languageLabel = textObj("Language",size=20)
        def setLanguage(sheet,option):
            mainScene.cur_lang = sheet[option]
            Obj.config["language"]=sheet[option]
            Scenes.mainScene.initUI()

        self.languageSelectionLayout = self.makeButtonLayout(languageSheet,mainScene.cur_lang,setLanguage)
        for button in self.languageSelectionLayout.childs:
            ##언어에 따라 버튼 폰트 변경
            value = languageSheet[button.text]
            if value=='cn':
                font = 'chinese_button.ttf'
            elif value=='jp':
                font = 'japanese_button.ttf'
            else:
                font = 'korean_button.ttf'
            button.textObj.font = font
            button.textObj.center = button.geometryCenter-button.geometryPos


        ##왼쪽 설정 레이아웃 생성
        self.leftSettingLayout = layoutObj(pygame.Rect(t,t*2,0,0),isVertical=True,childs=[self.resolutionLabel,self.resolutionLayout,self.modeLabel,self.modeLayout,self.musicVolumeLabel,configScene.musicVolumeSlider,
                                                                                          self.SEVolumeLabel,self.SEVolumeSlider,
                                                                                          self.muslcSelectionLabel,self.musicSelectionLayout,self.costumeLabel,
                                                                                          self.costumeSelectionLayout,self.languageLabel,self.languageSelectionLayout],spacing=20)
        
        

        ##체스 레이팅 설정 기능
        self.ratingLabel = textObj("Chess Level",size=20)
        def setRating(sheet,option):
            Obj.config["rating"]=sheet[option]
        try:
            cur_rating = Obj.config["rating"]
        except:
            Obj.config["rating"] = ratingSheet["Intermediate"]
            cur_rating = Obj.config["rating"]
        self.ratingSelectionLayout = self.makeButtonLayout(ratingSheet,cur_rating,setRating)

        self.rightSettingLayout = layoutObj(pygame.Rect(w-t*9,t*2,0,0),isVertical=True,childs=[self.ratingLabel,self.ratingSelectionLayout],spacing=20)

        return
    def init(self):
        return
    def update(self):
        ##TODO: ConFig Update##
        if Rs.userJustPressed(pygame.K_ESCAPE):
            Rs.setCurrentScene(Scenes.mainScene)
        configScene.configBackButton.update()
        self.leftSettingLayout.update()
        self.rightSettingLayout.update()
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
        self.rightSettingLayout.draw()
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
    Rs.target_fps = 60
    Obj.stockfish_hint.set_depth(20)
    Obj.stockfish_hint.set_skill_level(20)

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
    

    ##게임 해상도 설정
    try:
        res = Obj.config["Resolution"]
        win_res = (int(res*1920/1080),res)
    except:
        win_res = (1920,1080)

    window = REMOGame(window_resolution=win_res,screen_size=(1920,1080),fullscreen=False,caption="Play Chess with Lady Bongcloud")
    window.setCurrentScene(Scenes.mainScene)
    window.run()

    '''
    window = REMOGame((1920,1080),True,caption="Bishoujo Chess")
    REMOGame.setCurrentScene(Scenes.mainScene)
    window.run()

    '''
    # Done! Time to quit.


