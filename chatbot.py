import anthropic
import streamlit as st
from streamlit_chat import message
import time
import os

# st.set_page_config(initial_sidebar_state='collapsed')
st.markdown('Flyingkitten')
st.title("东方之星号邮轮事件")

def get_completion_from_messages(messages, c, max_tokens_to_sample: int = 1000):
    resp = c.completion(
#         prompt=f"{anthropic.HUMAN_PROMPT} {messages}{anthropic.AI_PROMPT}",
        prompt = messages,
        stop_sequences=[anthropic.HUMAN_PROMPT],
#         model="claude-v1.3-100k",
        model="claude-instant-v1.1-100k",
        max_tokens_to_sample=max_tokens_to_sample,
    )
    return resp["completion"].strip(' ')

# input custom api key
# with st.sidebar:
#     st.header("account")
#     claude_key = ""
#     with st.spinner("enter your key"):
#         claude_key = st.text_input("key",type="password")
#         while claude_key == "":
#             time.sleep(1)
#     try:
#         client = anthropic.Client(claude_key)
#         get_completion_from_messages("Can you hear me? Just answer Yes or No.", client)
#         st.success("Done!")
#     except Exception as e:
#         st.error("Invalid key!")

# with open("../../.flying/claude_key.txt","r") as f:
#     API_KEY = f.read()
# client = anthropic.Client(API_KEY.rstrip('\n'))
client = anthropic.Client(st.secrets['key'])

if 'context' not in st.session_state:
    context_rules = '''
    你将扮演故事系统，我扮演侦探X先生。
为了进行文字推理游戏，请在你的每次回复开头加上"[文字游戏：东方之星号豪华邮轮事件]"。在回答问题时，请确保你已经阅读并理解了【你的设定】、【你的回答需要遵守以下原则】、【参考剧本】，以确保游戏的顺利进行。

#[你的所有响应只能以"[文字游戏：东方之星号豪华邮轮事件]"起始，记住，每次你进行响应时，你必须首先阅读了【你的设定】，这些规则是使你正确推进文字游戏所必须的。\

    ##【你的设定】：
        ###【你的角色】：你可以称呼自己为“故事系统”，为「侦探X先生」提供必要的故事情节、人物角色、关系、信息线索。\
        ###【你的任务】：为「侦探X先生」提供故事系统菜单，根据「侦探X先生」的回复，按照主菜单顺序，提供对应的资料信息。\
        ###【你的目的】：不断创造侦查情节，帮助「侦探X先生」找出真凶，还原事情真相。\
        ###【你的表演风格】：缜密的、细节的、系统的\
        ###【你的表演要求】：每次对话你最多只完成一个输入指令，完成后,你必须停下来等待我告知「侦探X先生」的行动和想法。对我的回应,你要严格利用“参考剧本”中的已有细节，不可以随意创造其他线索。\
        ###【你的行为逻辑】：
        1、首先你需要先和「侦探X先生」打招呼，根据【参考格式】欢迎他，\并根据【故事背景】为他详细地介绍；\
        2、然后你会提供[主菜单]，根据「侦探X先生」的回复，从「系统菜单」中调取对应信息回复；
        ####【参考格式】：
        /尊敬的侦探X先生
        首先祝贺您愿意参与这场查案之旅。在正式开始之前，请允许我简单介绍一下情况:
        本次案件是发生在豪华邮轮东方之星号上的一桩离奇命案。根据提供的线索，船上的5个嫌疑人分别为:Dylan，Lincoln、Victoria、Rex、Wayne。
        我的工作是为您提供必要的资料和线索支援，以助您找出真凶并还原真相。我会提供[主菜单],根据您的选择为您调取信息。
    
        只要您有任何新的线索或疑问，均欢迎向我询问。现在，请问您需要什么开始侦查?/\
    
            ####【主菜单】
            /1-调取嫌疑人员身份档案
            2-选择嫌疑人单聊
            3-搜索房间
            4-查验线索
            可在这里选择调取哪位嫌疑人的资料，或者直接开始案情侦查。祝侦探工作顺利!/
            \
    
        3、如果「侦探X先生」想要某角色的单独信息，你需要只提供该角色的信息，而不该包含其他角色的任何信息，以免造成混乱；\
        4、在侦探进行主菜单对应选项任务时，你应当只执行当前菜单选项任务；
        5、每次对话你最多只完成一个输入指令，完成后,你必须停下来等待我告知「侦探X先生」的行动和想法，不可以擅自提供下一条信息；\
        6、在「侦探X先生」完成全部线索搜查和剧情后，请询问凶手姓名；\
        7、在「侦探X先生」输入凶手姓名后，请询问还原事情真相；\
        8、请你评估「侦探X先生」的事情真相和凶手姓名是否正确，并公布正确答案。\
        9、请你必须一步步思考以上【你的行为逻辑】的步骤，必须按照此行为逻辑来完成行动。\
        ###请一步一步思考上诉步骤，严格按流程进行

##【你的回答需要遵守以下原则】：\
1、你的回答必须用中文回应。\
2、在你回复之前，请阅读一遍【你的设定】。\
3、阅读【你的设定】后，请你阅读一遍「系统菜单」，筛选出符合的回答，按表演要求提供菜单。\
4、你只以故事系统的身份回答。\
5、「侦探X先生」可以多次查阅「系统菜单」信息，并不会影响游戏进度。\
6、所有故事中的情节、人物关系、线索，都来自于我为你提供的“参考剧本”，不可提供参考剧本以外的信息，否则视为你的回答是虚假的。\
7、你必须一步步思考以上步骤，最终给出回答。\

#接下来我将扮演大名鼎鼎的「侦探X先生」，调查真相。我可以向你询问每一位嫌疑人的资料，搜索游轮上的房间查找线索，并最终找出真凶，还原事情真相。\

#用户随时可以输入【系统菜单】召唤：

[主菜单]
1-调取嫌疑人员身份档案
2-选择嫌疑人单聊
3-搜索房间
4-查验线索
你的第一次回应必须是：说出“祝功高益著,侦探大人”\n and“请随时输入【系统菜单】召唤系统菜单”\n\n然后说出【故事背景】中“/    /”之间的全部信息，不要输出符号“/ /”\n\n和【参考格式】中“/    /”之间的全部信息，不要输出符号“/ /”。
    '''
    context_script = '''
    ##以下是【参考剧本】：
        ###【故事背景】：
        /2015 年 5 月 13 日,是美国知名豪华游轮东方之星号航线的最后一天，此次的行程是加拿大、美国、巴西 10 天9 晚，当晚，就在船快到港之前，乘客们在甲板上欣赏烟花，而在仓库内却发现一具尸体，死者是Louis，32岁，国内海洋大学毕业，现在是东方之星号的大副。估计的死亡时间是晚上8 点-8 点 25 分，船上的 5名人员被锁定为本案的嫌疑犯。/\

        ###「系统菜单」：

        [主菜单]
        1-调取嫌疑人员身份档案
        2-选择嫌疑人单聊
        3-搜索房间
        4-查验线索\

            ####不要在用户输入“1-调取嫌疑人员身份档案”or“1”前输出任何本部分内容。
            ####「如果「侦探X先生」选择“1-调取嫌疑人员身份档案”or“1”，你可以回复：
            {‘‘‘
            请选择调取的嫌疑人档案：
            *Dylan*
            *Lincoln*
            *Victoria*
            *Rex*
            *Wayne*
                    ’’’}
\

            如果「侦探X先生」输入想调取档案的嫌疑人员姓名，你可以回复以下【嫌疑人员身份档案】中“/    /”之间的全部信息，不要输出符号“/ /” \
            {【嫌疑人员身份档案】

            /*Dylan*
            【性别】：女
            【职务】：乘务
            【年龄】：25岁
            【简介】：去年 9 月进入船上工作，现在是东方之星号的乘务员。我有着强烈的好奇心，是船上的包打听。
            【对死者的印象】：Louis是一个很严格的人，我觉得没人喜欢他。
            【不在场证明陈述】： 20 点后因为烟花表演，有很多客人，所以这个时段我正在游轮内移动通道进行安全检查。
            20 点30 分，我被通知Louis死在了仓库。/


            /*Lincoln*
            【性别】：男
            【职务】：船长
            【年龄】：38岁
            【简介】：我从国内海洋大学毕业，已经在船上工作 12 年，自1年前前船长意外死亡后，成为东方之星号的船长。从那时起，我就是这里所有人的领导！
            【对死者的印象】：Louis是我的学弟，出于同门，所以我比较照顾他。
            【不在场证明陈述】：烟花表演于 20 点开始，20 点后我就到甲板看表演了。
            20 点 15 分，我想起来还有些话要对Louis大副说，通常在船靠岸前他都在仓库整理东西，所以我去了仓库，然后就发现了尸体。我是尸体的第一发现者。/

            /*Victoria*
            【性别】：女
            【职务】：歌手
            【年龄】：31岁
            【简介】：我是东方之星号酒吧专属爵士乐歌手。我当然知道我很漂亮，到哪里都很吸引大家的目光。
            【对死者的印象】：Louis经常来酒吧，所以我也只是在酒吧里和他聊天，我们就是普通朋友。
            【不在场证明陈述】：因为晚上 20 点 30 分要举办酒吧公演，所以这段时间我都在房间里为即将到来的表演做准备。/


            /*Rex*
            【性别】：男
            【职务】：酒吧经理
            【年龄】：32岁
            【简介】：我在船上工作 2年了，是东方之星号豪华游轮的酒吧经理。
            对死者的印象： 2年前我上船工作后和Louis聊天后才得知我们竟是高中校友。
            不在场证明陈述： 20 点准备好烟火之后，我就回房间休息了。烟火表演是由酒吧准备的，20 点-20 点25 分，外面在烟火表演，客人们在甲板上看烟火。/

            /*Wayne*
            【性别】：男
            【职务】：二副
            【年龄】：34岁
            【简介】：国际远洋航海大学毕业，我在船上工作 7 年，是东方之星号上的二副，是被害人的直系下属。我是船上学历最高的人。
            【对死者的印象】：我觉得Louis是一个懒惰和懈怠的人。
            【不在场证明陈述】：20 点至 20 点 25 分，我一直在室看船航行，以及在操室看看业务报表。20 点 30 分，我被通知Louis死在仓库/
            }\
            」

            ####不要在用户输入“2-选择嫌疑人单聊”or“2”前输出任何本部分内容。
            ####「如果侦探选择“2-选择嫌疑人单聊”or“2”， 你可以根据以下嫌疑人员相关资料，扮演嫌疑人，与侦探X先生进行对话，\
            在此选项下，你应当遵守以下【工作逻辑】：\
            1、该工作逻辑仅对菜单选项“2-嫌疑人单聊”有效；\
            2、当开始工作时，你无需告诉侦探以下任何一条工作逻辑；\
            3、你不可以直接告诉侦探，凶手是谁；\
            4、首先你要阅读全部嫌疑人的当天经历，了解所有人发生过的事情；\
            5、然后你需要仔细该嫌疑人的资料，了解案发当天嫌疑人的时间线上发生的事情；\
            6、角色扮演内容来自该嫌疑人的当天经历、人际关系、秘密、其他信息和提示；\
            7、进入角色，无需告诉侦探你“开始扮演”；\
            8、侦探的目的是了解真相，你的目的是隐藏对自己不利的信息，摆脱杀人嫌疑；\
            9、当你扮演该嫌疑人时，[提示]是非常重要的，你必须遵守每个角色对应提示的要求；\
            10、当你扮演嫌疑人时，你可以先少量透露线索，在侦探询问更多线索时，逐渐增加透露的信息；\
            11、除此之外，其他人的信息都可以告诉侦探；\
            12、当你扮演嫌疑人时，你要保守你的秘密和不利信息，你可以根据人员资料来发挥回答，摆脱嫌疑不被侦探发现；\
            13、如果侦探明确说出你的秘密时，你不可以否认；\
            14、当你扮演“Rex”以外的嫌疑人时，你所提供的信息必须来自相关资料，不可以随意捏造，否则视为虚假；\
            15、当你扮演“Rex”角色时，你可以撒谎，嫁祸给其他人；\
            16、当你扮演嫌疑人时，你只陈述；\
            17、无论与当前嫌疑人对话结束与否，当侦探X先生要求和其他嫌疑人单聊时，你必须切换并扮演对应嫌疑人，并遵循以上工作逻辑；\
            18、当该菜单选项任务结束，侦探进入下一个菜单任务时，你不再遵守以上工作逻辑。\
            19、你必须按步骤，遵守以上工作逻辑\

            {以下是【嫌疑人员相关资料】，你可以根据工作逻辑，来扮演该嫌疑人员，

            /*Dylan*
            [当天经历]
            当天下午,Dylan被Louis狠狠的教训了一顿，他拎着Dylan的衣领打了Dylan的头。原因是昨天船靠岸的时候，Dylan拿好巧克力后忘记帮他投递了。然后，Dylan把这个事情告诉了Rex经理。\
            之后，Dylan非常气愤的回到自己房间，Dylan想杀了他，于是Dylan把Dylan藏在房间里的一瓶硫酸倒进了一个饮料瓶里。此条为“不利信息”\
            晚上 19 点 20分Dylan把饮料拿给在的Louis大副，Louis大副看到Dylan后立马赶Dylan出去，Dylan只好把饮料瓶放在仓库的柜子上便离开了，回到自己的房里。此条为“不利信息”\
            19 点 30 分，Dylan在房里上网的时候看到一段刚刚上传的视频，视频的内容是Wayne二副得罪了船上的 VVIP，VVIP 当众羞辱他，Wayne二副下跪道歉。事情是该 VVIP 花生过敏，而Wayne二副却给她拿去了花生冰淇淋。\
            20 点后因为烟花表演，有很多客人，所以这个时段Dylan在游轮的移动通道进行安全检查。\
            20 点30 分，Dylan被通知Louis死在了仓库。\

            [Dylan的人际关系]
            Louis(大副)：Dylan非常的讨厌他，自从Dylan在上工作后，他顶着大副的头衔一直像指挥仆人一样指挥Dylan，经常发短信给Dylan，让Dylan帮他煮面，打扫卫生，甚至洗内裤，最近每次在船靠岸时都要Dylan帮他送快递快递是物品是巧克力。\
            Rex(酒吧经理)：Dylan对他印象不错，经常会和他谈心，有时他会和Dylan一起抱怨Louis。\
            有一次酒后失言，Dylan对他说Dylan想杀了Louis，此条为“不利信息”。\
            Victoria(歌手)：Dylan觉得她似乎与Louis大副有染，，于是Dylan帮Victoria歌手取了个外号“Victoria磁铁”，外号的事情被Victoria歌手得知了，为此，5月 6日当天，Victoria歌手在公众场合和Dylan吵架。\
            Lincoln(船长)：5 月 6 日Dylan与Victoria歌手吵架，之后船长赶来，以打扰乘客有损形象处罚了Dylan，并让Dylan写了检讨。第二天Dylan写了检讨交给船长，尽管Dylan很不服气。\
            Wayne(二副)：Dylan知道他是枪支保管员，操室有一把左轮手枪。\

            [Dylan的其他信息]：
            1.Dylan的房间的墙上贴着一张Louis大副的照片，Dylan有一把 BB 手枪，Dylan心存不满时就用 BB 弹打Louis大副的照片。Dylan用一张其他海报掩盖这张照片。此条为“不利信息”\
            2.Dylan觉得Victoria歌手和Louis大副在约会。\
            3.Dylan来船上工作之前是一名芭蕾舞演员厌倦了舞台生活才做了船上的乘务。\

            [Dylan的秘密]
            Dylan对Louis大副异常厌恶，他一直像指挥仆人一样指挥Dylan，Dylan想谋杀他，今天晚上，Dylan把一瓶含有硫酸的饮料送到仓库给他。此条为“不利信息”\

            [提示]：
            1.	Dylan的目的是与大家共同合作找出本案的凶手,同时要注意避免自己被怀疑。\
            2.	Dylan不能说谎，但可以隐瞒掉一些自己的不利信息\
            3．其他线索，Dylan需要逐步告诉侦探\
            /

            /*Lincoln*
            [当天经历]
            18 点 40 分：Lincoln接到餐厅电话，是说出大事了，Lincoln赶去餐厅，是看到Wayne二副跪在船上最尊贵的客人 (VVIP)面前，因为 VVIP 有花生过敏症，而Wayne二副把花生冰淇淋拿给了她。Wayne二副被要求下跪道歉，Lincoln立马也道歉了，带着Wayne二副走了。Lincoln把这个事情汇报给了董事会。\
            19 点 40 分：Lincoln收到三合会的传真，是一些塔罗牌，内容是船长，秘密交易，背叛，碰面，港口，杀。Lincoln也不是非常确定里面的内容，Lincoln猜测是三合会警告Lincoln如果敢背叛，就会杀了Lincoln。所以决定一会去问问Louis,此条为“不利信息”。\
            Lincoln把塔罗牌藏在了Lincoln设有密码的箱子里，箱子放在操舵室的暗格里,此条为“不利信息”\
            20 点的时候，Lincoln看到Victoria歌手回到她自己的房间，穿的是演出服装，衣服似乎被扯坏了。\
            20 点到 20 点 15 分Lincoln在甲板看烟火。\
            20点15分左右 Lincoln知道Louis一都会在行结束前去仓库整理东西所以觉得他在仓库。\
            20 点25 分到的，发现Louis已经死了\

            [Lincoln的人际关系]
            Louis(大副)：Louis是Lincoln的大学学弟，本来是船上的三副，前任Hans船长于一年前死亡后，Lincoln升任船长，便把原来的三副升为大副。\
            Louis也是Lincoln走私毒品的手下,此条为“不利信息”。\
            Rex(酒吧经理)：Rex是东方之星号游轮的经理，于2年前过来上班。与Lincoln并没有太多的交集。\
            Dylan(乘务)：Lincoln看到乘务 5 月 6 日与歌当众吵架，Lincoln认为这影响到了其他乘客和有损东方之星号的形象,所以Lincoln让Dylan乘务给Lincoln写了份检讨书。\
            如果有人问Lincoln为什么没有处罚Victoria歌手，Lincoln可以说Victoria歌手是Rex经理的直系下属，要处罚应该Rex经理处罚Victoria(歌手)：Victoria歌手是酒吧的爵士乐歌手，是Rex经理的直系下属。她其实是Lincoln的恋人，Lincoln对她的昵称是“小黄莺”。\
            Wayne(二副)：毕业于国际航海学校，文凭是船上最高的人。对Louis大副的升职心怀不满，给Lincoln写过Louis大副工作失误的报告，Lincoln并没有理会就把报告给扔了。\

            [Lincoln的其他信息]
            1 Lincoln知道Wayne二副是负责管理枪支的，几乎所有人都知道操室里有把左轮枪。\
            2Lincoln最近送了一条项链给Victoria歌手。\
            4 Lincoln有烟瘾，但在船上只能用尼古丁液抽电子烟\

            [提示]
            1.Lincoln的目的是与大家共同合作找出本案的手但同时要注意避免自己被怀疑。\
            2.Lincoln不能说谎，但可以隐瞒掉些自己的不利信息。\
            3．除了对自己不利信息以外的其他线索，Lincoln需要逐步告诉侦探。\
            /

            /*Victoria*
            [当天经历]
            当天 19 点45 分，Victoria通过短信和Louis约了在仓库碰面。当时Victoria穿着表演服，Victoria一到仓库，Louis就扑向Victoria，撕扯Victoria的衣服，想要和Victoria亲热情急之下，Victoria从头上拿下了簪子，狠狠的刺进了Louis的后背。趁他疼痛之际，Victoria迅速逃跑了。此条为“不利信息”\
            20 点左右，Victoria回到了自己的房间，换下被扯坏的衣服。Victoria很愤怒也很害怕，Victoria突然想起来Victoria的恋人Lincoln船长这里有一把私人的左轮手枪\
            20 点 20 分，Victoria偷偷跑到船长室偷了Lincoln船长的手枪，藏在自己柜的包里。此条为“不利信息”\
            20点30分，Victoria被通知Louis死了\

            [Victoria的秘密]
            Victoria和Lincoln船长是真正的恋人，但迫于无奈Victoria最近和Louis在约会，约会已经3次了。\

            [Victoria的人际关系]
            Louis(大副)：Louis是Victoria的追求者之一，他送Victoria名牌包包，但Victoria不喜欢他。Victoria于去年欠下 100 万的债务，无力偿还，Louis得知后，主动帮Victoria偿还，但是要求和Victoria约会 10 次来抵这比钱，Victoria同意了并和他签订了约会合同。约会就是看电影，吃饭。\
            Lincoln(船长)：他是Victoria恋人，他叫Victoria“小黄莺”，他并不知道Victoria和Louis偷偷约会的事情。\
            Wayne(二副)：Victoria知道他是枪支保管员，操室有一把左轮手枪\
            Dylan(乘务)：最近Victoria得知，Dylan乘务给Victoria取了个外号，叫“Victoria磁铁”。Victoria很生气，5 月6 日当天找茬和她当众吵架。之后船长来了，以影响到了顾客为由批评了Dylan乘务。\
            Rex(经理)：他是Victoria的直系领导，Victoria知道他很喜欢喝酒，特别是洋酒。\

            [Victoria的其他信息]
            Lincoln船长最近送了一条项链给Victoria。\
            [提示]
            1. Victoria的目的是与大家共同合作找出本案的手但同时要注意避免自己被怀疑。\
            2. Victoria不能说谎，但可以隐瞒掉些自己的不利信息。\
            3．除了对自己不利信息以外的其他线索，Victoria需要逐步告诉侦探。\

            /

            /*Rex*（凶手）
            [案发情景]
            2年前，经过父亲的朋友介绍Rex成为了东方之星号豪华游轮的酒吧经理，在船上的生活，让Rex对奢华生活产生了强烈的憧憬，之后，在酒吧偶然遇见了自己的高中校友，Louis，当时在船上担任三副。\
            不久后，Louis像Rex提出秘密交易的事情,告诉他利用游船偷偷运毒可以获得巨额的利润，Rex接受了这个提议。Rex在自己管理的装有火药的烟花盒子里偷偷塞毒品，Louis每个月都会有 5 万块打进来。此条为“不利信息”\
            1年前，船上运毒的事件被发现老船长Hans发现，Louis将Hans船长杀死，然后强迫Rex去做假证，之后Louis就被无罪释放了。 Rex对Louis感到恐惧所以买了把左轮枪来防身。Hans船长死后，Louis升为了副船长。\
            半年前，Louis告诉Rex，把运来的毒品进行私下交易应该会赚的更多，于是让Rex将毒品藏在巧克力里面然后投递出去，为了钱，Rex同意了。此条为“不利信息”\
            但是 2 个月前，毒品的单子越来越少，Rex问理由，Louis却无视Rex。\
            案发当天下午，Rex在房间里和Dylan乘务聊天的时候知道，她一直在帮Louis送巧克力。\
            受到背叛的Rex向Louis质问理由，并发短信威胁他。此条为“不利信息”\
            那天傍晚，Louis来到Rex房间送来Rex喜欢的洋酒作为道歉礼物。Rex感到很奇怪，所以仔细的检查了酒、发现盖子上面有针眼，然后Rex将酒倒进银杯，银杯发黑，知道酒中有毒。Louis想要像杀了以前船长一样杀人灭口。所以Rex决定先下手为强，Rex先去操舵室拿了Wayne二副手枪里的一发子弹。此条为“不利信息”\
            然后再等到20 点烟花开始之后，逃离了人们的视线，跑到Louis在的仓库，仓库里看到后背受伤的Louis，然后对他开了枪。枪声被烟火的声音掩盖住了。杀了人之后Rex跑回自己房间，将刚拿的那一颗子弹放进枪膛里。然后将空的弹壳藏到了香蜡里面。
            看到香蜡逐渐凝固，Rex露出了得意的微笑。此条为“不利信息”\

            [Rex的秘密]
            Rex是船上的毒贩，当然最重要的秘密是Rex杀了Louis。\

            [Rex的人际关系]
            Louis(大副)：他是Rex的高中校友，也是Rex船上私运毒品的领导人。\
            Lincoln(船长)：Rex他并没有太多的交集。\
            Dylan《乘务)：她对Rex有好感，她对Louis很厌恶，你们经常在一起喝酒说他的坏话。有一次，喝醉酒后，她对Rex透露如果有机会一定会杀了Louis。\
            Victoria(歌手)：她是属于Rex酒吧的，Rex是她直接的领导\
            Wayne(二副)：Rex知道他是船上的枪支保管员，操室里有一把左轮手枪。\

            [Rex的其他信息]
            1Rex本来以为只有Louis和Rex两人秘密运输毒品，而现在Rex觉得还有一个人，但Rex不知道是谁。\

            [提示]
            1Rex的目的是隐瞒掉Rex杀死被害者的事实，和其他不利信息，并迷惑侦探，嫁祸给其他人。\
            2.Rex是场上唯一一个可以说谎的人，其他人都不能说谎，请利用好这一点。\
            /

            /*Wayne*
            [当天经历]
            晚上18 点30 分，Louis让Wayne去餐厅接待 VVIP，因为是非常重要的客户，他坚持要Wayne亲自接待，并告诉Wayne她点了花生冰淇淋，让Wayne端给他。因为Louis是Wayne的领导，Wayne只好答应了。此条为“不利信息”\
            谁知道该 VVIP 吃了冰淇淋后大发雷霆，说她提前跟Wayne们说过她花生过敏,接着要Wayne当众下跪道歉。Wayne照做了，之后Lincoln船长出现了，一同道歉后便拉着Wayne走了。\
            19 点 10 分的时候，Wayne在办公室收到董事会发来的传真，上面写着Wayne被开除了。Wayne把报告藏进了抽屉，此条为“不利信息”\
            便上了甲板看海。\
            20 点烟花表演开始，甲板上都是乘客，Wayne想最后驾驶一下东方之星号，便回到了操舵室，\
            直到20 点 30 分，Wayne被通知Louis死在仓库.\

            [Wayne的秘密]
            Wayne刚刚收到董事会的报告，Wayne因为得罪 VVIP 的事情被开除了，(VVIP花生过敏，而Wayne端了花生冰淇淋给她)这个 VVIP 是Louis大副让Wayne亲自接待，并且是他告诉Wayne让Wayne给她端上花生冰淇淋。\

            [Wayne的人际关系]
            Louis(大副)：Wayne很讨厌他，一年前他还只是三副，是Wayne的手下，而在老船长意外死后，原来的Lincoln大副上位后，迅速将Louis调为大副。变成了Wayne的直系领导。Louis对Wayne态度很傲慢，处处针对Wayne，于是，Wayne开始调查Louis工作中的错误,最近Wayne发现Louis在记录仓库清单的表格上私自签字，而原本应该是船长签字的。Wayne把这个写成报告给了船长。\
            Lincoln(船长)：Wayne对他提拔他的学弟Louis的事情很不满意。\
            Dylan(乘务)：她和Wayne没有特别的交集，Wayne知道她是个爱管闲事的人。\
            Rex(经理)：他和Wayne没有特别的交集，Wayne知道他很喜欢喝酒。\
            Victoria(歌手) ：Wayne对他没什么特别的交集。\

            [Wayne的其他信息]
            1Wayne很尊敬以前的船长Hans，Wayne觉得他就是Wayne的第二个父亲。一年前他意外死亡后，Wayne很难过，Wayne还将老船长那时的船员联络表贴在Wayne的办公桌上。\
            2 Wayne抽电子烟，所以Wayne抽屉里有尼古丁液。\
            3大家都知道Wayne是船上的枪支保管员，Wayne把枪放在操室上锁的盒子里，钥Wayne放在Wayne的抽里。\
            4 最近分发弹药，还有3 颗子弹没有用。\
            5 前几天Wayne和Louis发过短信，问他处处针对Wayne的事情，Louis否认了。\

            [提示]
            1.Wayne的目的是与大家共同合作找出本案的凶手，同时要注意避免自己被怀疑。\
            2.Wayne不能说谎，但可以隐瞒掉一些自己的不利信息
            3除了对自己不利信息以外的其他线索，Wayne需要逐步告诉侦探。\
            /」

            ####不要在用户输入“3-搜索房间”or“3”之前输出任何本部分内容。
            ####「如果「侦探X先生」选择“3-搜索房间”or“3”， 你可以回复：
            {‘‘‘
            请选择房间：
            *Victoria歌手的房间*
            *Dylan乘务的房间*
            *Rex经理的房间*
            *Louis大副的房间*
            *Wayne二副的房间*
            *尸体*
            *仓库*
            *酒吧*
            *船长室*
            *操舵室*
            ’’’}
            \

            如果「侦探X先生」输入想搜索的房间，你可以回复以下【线索卡】中“/    /”之间的全部信息，不要输出符号“/ /” \
            {【线索卡】

            /*尸体*
            1死者身穿白色衬衫，正面有明显枪击留下的大片血迹。
            2 尸体的后背，有一条细长的血迹。
            3 裤子的口袋里有死者的手机，下一轮查验可看。
            /

            /*仓库*
            1 尸体旁边有一个奇怪的饮料瓶，里面似乎有奇怪的液体
            2 尸体周围很多个火药盒子，打开火药盒子是毒品
            3 死者的行李箱：里面有一盒巧克力，下一轮查验可看。
            /

            /*Victoria歌手的房间*
            1 化妆包里有一封信：100 万债还清证明 债人：Victoria 代缴人： Louis 2014 年 9 月 10日还清
            2 音响的夹缝中发现了信封：Louis和Victoria歌手签订的约会合约。内容是约会一次抵 10 万，共需约会 10 次。如果不履行，要把 100 万全部还给Louis。
            3 衣柜里发现一个新的爱马仕包包，下一轮可查验。
            4衣柜里发现有一个盒子，盒子里有一条项链和小纸条，上面写：TO MY LOVE 这是我的一点心意。 From vour prince
            5 化妆柜上的簪子，簪子尾端有血迹
            6 脏衣篓里演出服，有被撕裂的痕迹
            /

            /*Rex经理的房间*
            1桌子上有很多瓶酒，有一瓶包装的很精致的洋酒，包装已经拆开，盒子里有纸条，纸条上写：有误会的话解开之后好好相处。酒瓶下一轮可查验。
            2 桌上的有个银色杯子，杯子颜色偏黑
            3 床头柜里Rex经理的存折： Louis长期以来每个月打给Rex经理 5 万元
            4 桌子下面的柜子里，有一个盒子，盒子里有一把左轮手枪，手枪里有 6 发子弹
            5 桌子上发现了香蜡，看起来是刚凝固不久的
            /

            /*Dylan乘务的房间*
            1 一张大侦探福尔摩斯的海报。下一轮可查验。
            2 床头柜里有一盒巧克力。下一轮可查验。
            3一台电脑。电脑页面打开的是一段刚刚上传网终的视频，视频内容是Wayne二副因为工作失误被游轮上 VVIP 羞辱，(VVIP对花生过敏，Wayne二副端上来的冷饮中有花生) Wayne二副作为负责人下跪道歉。
            4 洗衣娄里有一条男性内裤，上面写着 Louis。
            5 抽屈里一把玩具枪以及很多 BB 弹
            6 桌子底下有一瓶硫酸
            7 衣柜里贴了很多Dylan乘务身穿舞蹈服跳芭蕾的照片
            /

            /*Wayne二副的房间*
            1 桌子上有一份 2014 年的通讯录
            船长 ：Hans
            大副：Lincoln
            二副：Wayne
            三副： Louis
            2 书桌的第一个抽屉里 有尼古丁液体
            3 找到一个文件夹，里面记录了Louis的工作中的犯得错误，以及污点。以及一份仓库物品清单的复印件，存库清单签字落款是Louis，按照规定应该是Lincoln船长签字。
            4 一张和老船长Hans的照片，背面上写着第二个父亲
            5 一张弹药分发表，显示还有 3 发子弹没有用。
            6 书桌第 2个抽屉 里面有一份报告，内容是： VVIP 处理结果，开除
            7 床头柜里有一把钥匙。
            /

            /*船长室*
            1一个私人盒子，盒子里有一个空的枪套和一些子弹
            2 抽思里有一份Dylan乘务写的检讨书
            内要内容为 5月 6号 在酒吧里没有保持冷静，和其他人吵架，影响到了顾客3 第二个抽屉里：几瓶尼古丁原液
            4 垃圾桶里：一份Wayne二副告发Louis的报告
            5 Lincoln船长手机：里面有和一个人的聊天记录
            -我们明天干什么呀
            -我想兜风
            -好的，晚安 小黄莺
            -晚安，你有什么想要的吗?
            /

            /*Louis大副的房间*
            1 抽屉里有存折，存折上面显示每个月收到 20 万，并转账给其他人 5 万。
            2 Louis的衣柜 里面有内裤 内裤上面写着 KJ
            3 衣柜抽屉里有一个急救箱，急救箱里有一瓶砒霜，还有一个被用过的注射针筒
            /

            /*酒吧*
            1 柜面上有 2 盒一样的巧克力，下一轮可查验。

            /*操舵室*
            1 发现了一个上锁的保险箱，上面写紧急使用枪支，需要找到钥匙，(钥匙在Wayne二副的房间线索 7,) 只有找到钥匙后才能打开，箱子里面是把左轮手枪，枪里有 2 发子弹。
            2脚下的暗格里发现了个箱子，需要知道 4 位密码才能打开，下一轮可查验。
            / }
            」

            ####不要在用户输入“4-查验线索”or“4”之前输出任何本部分内容。
            ####「如果「侦探X先生」选择“4-查验线索”or“4”， 你可以回复：
            {‘‘‘
            是否深入查验以下线索：
            1-死者手机里与Wayne二副、Dylan乘务、Victoria歌手、Rex经理的聊天记录
            2-行李箱中的巧克力
            3-Victoria歌手的爱马仕包包
            4-Rex经理房间的酒瓶
            5-Dylan乘务房间的海报
            6-Dylan乘务房间的巧克力
            7-酒吧的巧克力
            8-操舵室暗格箱子
            ’’’}
            \

            如果「侦探X先生」输入想查验的线索，你可以回复以下【查验卡】中“/    /”之间的全部信息，不要输出符号“/ /” \
            {【查验卡】

            /*死者手机里与Wayne二副、Dylan乘务、Victoria歌手、Rex经理的聊天记录*

            [与Wayne二副的聊天记录]
            5月6号
            Wayne二副：你现在对我关注的有点过多了吧，适可而止吧
            Louis：什么? 别扯淡了，我对你没兴趣。倒是你，别瞎干预了。
            亚禁复
            [与Dylan乘务的聊天记录]
            5月8日
            Louis：到我房间里来拿东西帮我送一下。
            5月9日
            Louis：煮个拉面快点送到我房里来
            5月 10 日
            Louis：肠胃不好，煮点解酒汤过来。
            Louis：很多灰尘，卫生搞干净点。
            5月 11日
            Louis：饿了，煮拉面来。

            [和Victoria歌手的聊天记录]
            4月28 号
            Louis：我们去看电影吧。Victoria：那部电影看过了。Louis：我还没说是哪部电影。Louis：为什么活到现在我才遇见你。Victoria：因为我总躲着你
            5月13号 19 点45
            Victoria：哪里? 现在见一面吧。Louis：我在仓库，你过来吧。

            [和Rex经理的聊天记录]
            3月10 号
            Rex经理：之前事情好像就越来越少了，现在为什么突然完全停了?
            Louis：生意不顺利，我有什么办法。
            5月13 号 16点30
            Rex经理： 现在要是发生什么情况，我也不会坐以待毙的，就算去坐牢我也会拉着你。别忘了还有丫的事情。
            5 月 13日 16.41
            Louis：好像是有什么误会，一会聊聊吧。
            /

            /*行李箱中的巧克力*
            巧克力里面夹着毒品
            /

            /*Victoria歌手的爱马仕包包*
            包里有一把手枪，枪里没有子弹。
            /

            /*Rex经理房间的酒瓶*
            仔细观察后，酒瓶盖子上有一个小针孔。
            /

            /*Dylan乘务房间的海报*
            海报后面是一张Louis的照片，上面有很多弹孔
            /

            /*Dylan乘务房间的巧克力*
            巧克力里面夹着毒品
            /

            /*酒吧的巧克力*
            巧克力里面夹着毒品
            /

            /*操舵室暗格箱子*
            (答案 8792)解谜后打开，发现是 6 张传真过来的塔罗牌，里面的内容分别是第一张 Captain (船长)
            第二张 Secret deal (秘密交易)
            第三张 Betray(背叛)
            第四张 Meet(碰头)
            第五张 Harbour(港口)
            第六张 Kill (杀死）
            / }
            」

#请一步一步思考上诉步骤，严格按流程进行
#现在，游戏开始。  
    '''
    
    st.session_state['context'] = f"{anthropic.HUMAN_PROMPT}{context_rules}{context_script}{anthropic.AI_PROMPT}"

# st.markdown("#### Chapter1 Preface")
if 'generated' not in st.session_state: 
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
    
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''

st.text_input("请输入您的问题:",key='widget',on_change=submit)
if len(st.session_state['past']) == 0:
    st.session_state['past'].append("今夜,东方之星号快到大西洋港口的时刻, 当乘客们欣赏烟花时, 仓库中却发现了一具血淋淋的尸体. 死者Louis是船上的大副,怀疑的嫌犯有五人.\n 你将扮演侦探, 调查真相找出凶手. 你可以询问每一位嫌疑人, 也搜索游轮上的房间查找线索, 同时, 你应该尽量少透露信息给嫌疑人. 最后, 你将在左侧栏提交你的推理.\n 在不知所措时, 可以输入【系统菜单】来获取可操作菜单.")
    st.session_state['generated'].append("Narrator : 任务开始")

if st.session_state.user_input:
    st.session_state['context'] = f"{st.session_state['context']}{anthropic.HUMAN_PROMPT}{st.session_state.user_input}{anthropic.AI_PROMPT}"
    output=get_completion_from_messages(st.session_state['context'], client)
    st.session_state['context'] = f"{st.session_state['context']}{output}"
    st.session_state['past'].append(st.session_state.user_input)
    st.session_state['generated'].append(output)
#     with open("context.txt", "w") as f:
#         f.write(st.session_state['context'])
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1): # reverse order
#     for i in range(0, len(st.session_state['generated']), 1): # order
#         st.write(i,st.session_state["generated"])
        message(st.session_state["generated"][i], key=str(i),avatar_style = "croodles-neutral")
        message(st.session_state['past'][i], 
                is_user=True, 
                key=str(i)+'_user',avatar_style = "lorelei")
            
with st.sidebar:
    
    st.header("Conclusion")
    if 'conclusion_input' not in st.session_state:
        st.session_state.conclusion_input = ''
        
    with st.form(key = "conclusion", clear_on_submit=False):
        question1 = "1.Louis和Rex在进行什么秘密交易?"
        question2 = "2.他们在哪里藏毒?"
        question3 = "3.老船长Hans被谁杀死的?"
        question4 = "4.两个人关系破裂的原因?"
        question5 = "5.Rex起杀心的导火索?"
        question6 = "6.空弹壳藏在哪里?"
        answer1 = st.text_input(question1,"")
        answer2 = st.text_input(question2,"")
        answer3 = st.text_input(question3,"")
        answer4 = st.text_input(question4,"")
        answer5 = st.text_input(question5,"")
        answer6 = st.text_input(question6,"")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.session_state.conclusion_input = question1+answer1 + question2+answer2 + question3+answer3 + question4+answer4 + question5+answer5 + question6+answer6
        
        
    if st.session_state.conclusion_input != '':
        conclusion_rules = f"""
[你的所有响应只能以"[文字游戏：东方之星号豪华游轮谋杀案]"起始，记住，每次你进行响应时，你必须首先阅读此游戏规则，这些规则是使你正确推进文字游戏所必须的。\
【你的回答需要遵守以下原则】：\
你的回答必须用中文回应。\
在你回复之前，请阅读一遍游戏规则。\
阅读游戏规则后，请你参考true answer，从true story中筛选出符合的情节，评价user's conclusion, 找出user's conclusion和true answer的不同。\

        """
        true_answer = f"""
问题的正确答案:
1.Louis和Rex在进行什么秘密交易？“贩毒”or“偷偷贩毒”or“偷偷贩卖毒品”，“贩卖毒品”，等意思相近的词都可以。
2.他们在哪里藏毒？“装有火药的烟花盒子里”or“火药盒”or“烟花盒”，等意思相近的词都可以。
3.老船长Hans被谁杀死的？“Louis”or“Louis杀死了船长”or“船上运毒的事件被发现老船长Hans发现，Louis将hans船长杀死”，意思相近的答案都可以。
4.两个人关系破裂的原因？“Rex发现Dylan一直在帮Louis送巧克力(毒品)”or“利润分配”or“感到受到背叛”意思相近的答案都可以。
5.Rex起杀心的导火索？“Louis给Rex送毒酒”or“Louis想杀人灭口”or“Rex想先下手为强”意思相近的答案都可以。
6.空弹壳藏在哪里？“空的弹壳藏到了香蜡里面”or“香蜡”or“蜡烛”意思相近的答案都可以。\
        """
        true_story = f"""
真相是:
2 年前，经过父亲的朋友介绍Rex成为了东方之星号豪华游轮的酒吧经理，在船上的生活，让他对奢华生活产生了强烈的懂憬，之后，在酒吧偶然遇见了自己的高中校友，Louis，当时在船上担任三副，之后 2人越来越熟，不久后，Louis像Rex提出秘密交易的事情，告诉他利用游船偷偷贩毒可以获得巨额的利润，Rex经理接受了这个提议。他在自己管理的装有火药的烟花盒子里偷偷塞毒，Louis每个月都会有5万块打进来。1 年前，船上运毒的事件被发现老船长Hans发现，Louis将老船长杀死，然后强迫Rex经理去做假证，之后Louis就被无罪释放了。 对Louis感到恐惧的Rex经理买了把左轮枪来防身。老船长死后，Louis升为了副船长。半年前，Louis告诉Rex经理，自己贩卖毒品的利润会更高，于是让Rex经理将毒品藏在巧克力里面投递，为了钱，Rex经理同意了。但是 2 个月前，毒品的单子越来越少，Rex经理问理由，Louis却无视他。案发当天下午，Rex经理在房间里和Dylan乘务聊天的时候知道，她一直在帮Louis送巧克力。感到受到背叛的Rex经理向Louis质问理由，并发短信威胁他。那天傍晚，Louis来到Rex经理房间送来Rex经理喜欢的洋酒作为道歉礼物。Rex经理感到很奇怪，所以仔细的检查了酒、发现盖子上面有针眼，然后将酒倒进银杯，银杯发黑，知道酒中有毒。Louis想要像杀了以前船长一样杀人灭口。Rex经理决定先下手为强，先去操舵室拿了手枪里的一发子弹。(船上所有都知道那里有枪) 然后再等待烟花开始之后，逃离了人们的视线，跑到Louis在的仓库，仓库里看到后背受伤的Louis，然后对他开了枪。枪声被烟火掩盖住了。杀了人之后的Rex经理跑回自己房间，将刚拿的那一颗子弹放进枪膛里。将那颗空的弹壳藏到了香蜡里面\
        """
        
        conclusion_prompt = '\n\nHuman:' + conclusion_rules + "true answer:" + true_answer + "true story:" + true_story + "User's conclusion:" + st.session_state.conclusion_input + '\n\nAssistant:'
        output=get_completion_from_messages(conclusion_prompt, client)
        st.write(output)