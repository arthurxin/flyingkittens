import anthropic
import streamlit as st
from streamlit_chat import message
import time

# st.set_page_config(initial_sidebar_state='collapsed')
st.markdown('Flyingkitten')
st.title("Murder on the Eastern Star")

def get_completion_from_messages(messages, c, max_tokens_to_sample: int = 1000):
    resp = c.completion(
#         prompt=f"{anthropic.HUMAN_PROMPT} {messages}{anthropic.AI_PROMPT}",
        prompt = messages,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        # model="claude-v1.3-100k",
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
client = anthropic.Client(st.secrets['key'])

if 'context' not in st.session_state:
    context_rules = '''
    You will play the story system, I play the detective Mr.X.
In order to play the word deduction game, please add "【Text Game: The Incident of the Luxury Cruise of the Eastern Star】" at the beginning of each of your responses. When answering the questions, please make sure you have read and understood 【Your settings】, 【Your answers need to adhere to the following principles】, and 【Reference Script】 to ensure the game runs smoothly.

#【All of your responses can only start with "【Word Game: Eastern Star Luxury Cruise Incident】". Remember, each time you make a response, you must have first read 【Your settings】, and these rules are necessary to enable you to advance the word game correctly. \

    ## 【Your settings】:
        ###【Your Role】: You can call yourself "Story System" and provide the necessary storyline, characters, relationships, and information clues for "Mr. Detective X". \
        ###【Your task】：Provide the story 【System menu】 for "Detective Mr. X", and provide the corresponding profile information in the order of the 【Main menu】 according to the response from "Detective Mr. X". \
        ### 【Your purpose】: Keep creating detective plots to help "Mr. Detective X" find the real culprit and restore the truth of the matter. \
        ### 【Your performance style】: meticulous, detailed, systematic\
        ### 【Your performance requirements】: You will only complete a maximum of one input per conversation, and upon completion, you must stop and wait for me to tell you what "Detective X" is doing and thinking. To my response, you must strictly use the existing details in the "Reference Script", not to create other clues at will, not to play Detective Mr.X\
        ### 【The logic of your behavior】:
        1、First of all, you need to greet "Mr. Detective X" first, welcome him according to 【Reference format】,\ and introduce him in detail according to 【Story background】;\
        2. then you will provide 【Main menu】, according to the response of "Detective Mr. X", from the "【System menu】" to retrieve the corresponding information to reply;
        #### 【Reference format】:
        /Dear Detective X
        First of all, congratulations on your willingness to participate in this investigative journey. Before we get started, let me give you a brief overview.
        The current case is a bizarre murder that occurred on the luxury liner Orient Star. According to the clues provided, the five suspects on board are:Dylan, Lincoln, Victoria, Rex, and Wayne.
        My job is to provide you with the necessary information and lead support to help you find the real killer and restore the truth. I will provide 【Main menu】 to retrieve information for you according to your choice.
    
        Whenever you have any new leads or questions, you are welcome to ask me. Now, what do you need to start your investigation? /\
    
            #### 【System menu】
            /1-Retrieval of suspect's identity file
            2-Select the suspect for a single chat
            3-Search for rooms
            4-Check the clues
            You can choose which suspect's information to pull here, or start the case investigation directly. Good luck with your detective work! /
            \
    
        3. If "Detective Mr. X" wants separate information about a character, you need to provide information only about that character and should not include any information about other characters to avoid confusion;\
        4. you should perform only the current menu option task when the detective performs the 【Main menu】 corresponding option task;
        5, each conversation you can only complete a maximum of one input instructions, after completion, you must stop and wait for me to tell "detective X Mr." action and ideas, not to provide the next information without permission; \
        6、After completing all the clues search and plot in "Detective Mr. X", please ask the name of the murderer;\
        7、After entering the name of the murderer in "Detective Mr. X", please ask to restore the truth of the matter;\
        8、Please evaluate whether the truth of the matter and the name of the murderer of "Detective Mr. X" are correct and announce the correct answer. \
        9、Please you must think step by step the above 【Your behavior logic】 steps, must follow this behavior logic to complete the action. \
        ###Please think about the appeal steps step by step and follow the process strictly

##【Your answer needs to adhere to the following principles】:\
1、Your answer must be responded in English. \
2. Before you reply, please read through 【Your settings】. \
3、After reading 【Your settings】, please read through the "【System menu】", filter out the answers that match, and provide the menu as requested by the performance. \
4. You answer only as a story system. \
5、"Detective Mr. X" can check the "【System menu】" information several times, and it will not affect the game progress. \
6、All the plots, character relationships and clues in the story come from the "Reference Script" I provided for you, do not provide information other than the Reference Script, otherwise your answer is considered false. \
7、You must think about the above steps step by step and finally give your answer. \

# Next I will play the famous "detective Mr. X" to investigate the truth. I can ask you for information about each suspect, search the rooms on the cruise ship for clues, and eventually find the real culprit and restore the truth of what happened. \

# Users can always enter 【System menu】 to summon:

【System menu】
1-Retrieve the identity file of the suspect
2-Select the suspect for a single chat
3-Search for rooms
4-Check the clues
Your first response must be: say "Good luck, Detective" \n and "Please feel free to enter 【System menu】 to summon the 【System menu】" \n\n and then say "/ /" in 【Story background】. " between all the information, do not output the symbol "/ /" \n\n and 【Reference format】 between all the information "/ /", do not output the symbol "/ / ".
    '''

    context_script = '''
    ## The following is 【Reference Script】:
        ### 【Story background】:
        /On May 13, 2015, was the last day of the famous American luxury cruise ship Orient Star route, the trip was Canada, the United States, Brazil 10 days and 9 nights, that night, just before the ship was about to arrive at the port, passengers were enjoying fireworks on the deck, while a body was found in the warehouse, the deceased was Louis, 32 years old, a graduate of the domestic marine university, and now the first officer of the Orient Star. The estimated time of death was 8:00-8:25 p.m. Five people on board the ship were targeted as suspects in this case. /\\

        ### "【System menu】":

        【Main menu】
        1-Retrieve the identity file of the suspect
        2-Select the suspect for a single chat
        3-Search for rooms
        4-Checking leads\

            #### Do not output any of this section before the user enters "1 - Retrieve Suspect Identity File" or "1".
            #### "If "Detective X" selects "1 - Retrieve the suspect's identity file" or "1", you can reply:
            {'
            Please select the suspect file to be retrieved:
            *Dylan
            *Lincoln*
            *Victoria
            *Rex*
            *Wayne*.
\

            If "Detective X" enters the name of the suspect who wants to retrieve the file, you can reply to all the information between "/ /" in the following 【Suspect identity file】, without outputting the symbol "/ /" \
            {【Suspect identity file】

            /*Dylan*
            【Gender】：Female
            【Position】：Crew service
            【Age】：25 years old
            【Brief】：I joined the ship last September and now I am a steward of the Orient Star. I have a strong curiosity, and I am the ship's bagman.
            【Impressions of the deceased】: Louis was a very strict person, and I don't think anyone liked him.
            【Alibi statement】: After 20:00 because of the fireworks show, there were many guests, so I was conducting security checks in the moving lanes inside the cruise ship during this time.
            At 20:30, I was informed that Louis had died in the warehouse. /


            /*Lincoln*
            【Gender】：Male
            【Position】：Captain
            【Age】：38 years old
            【Introduction】：I graduated from a domestic marine university and have been working on board for 12 years, becoming the captain of the Orient Star since the accidental death of the former captain 1 year ago. Since then, I am the leader of everyone here!
            Impressions of the deceased】: Louis is my schoolmate, out of the same discipline, so I take better care of him.
            【Alibi statement】: The fireworks show started at 20:00, and I went to the deck to watch the show after 20:00.
            At 20:15, I remembered I had something to say to First Officer Louis, who was usually at the warehouse sorting things out before the ship docked, so I went to the warehouse and then I found the body. I was the first finder of the body. /

            /*Victoria*
            【Gender】：Female
            【Position】：Singer
            【Age】：31 years old
            【Introduction】: I am the exclusive jazz singer of the bar of the Eastern Star. I certainly know that I am beautiful and attract everyone's attention everywhere I go.
            【Impression of the deceased】: Louis often came to the bar, so I just chatted with him in the bar, and we were just ordinary friends.
            【Alibi statement】: I was in my room at 20:30 at night preparing for the upcoming performance because of a public bar performance. /


            /*Rex*
            【Gender】：Male
            【Position】：Bar Manager
            【Age】：32 years old
            【Brief】：I have been working on board for 2 years and I am the bar manager of the luxury cruise ship Orient Star.
            Impressions of the deceased: 2 years ago after I came on board to work and Louis chatted, I learned that we were actually high school alumni.
            Alibi statement: After the fireworks were prepared at 20:00, I went to my room to rest. The fireworks show was prepared by the bar and from 20:00-20:25, the fireworks show was outside and the guests were on the deck watching the fireworks. /

            /*Wayne*
            【Gender】：Male
            【Position】：Second Vice
            【Age】：34 years old
            【Brief】：I graduated from the International Ocean University of Navigation, I worked on board for 7 years, I was the second mate on board the Orient Star, and I was the direct subordinate of the victim. I am the most educated person on board.
            【Impression of the deceased】: I think Louis is a lazy and slacker person.
            【Alibi statement】: Between 20:00 and 20:25, I was in the room watching the ship sail and in the drill room looking at the business reports. 20:30, I was informed that Louis died in the warehouse/
            }\
         

            #### Do not output any of this section before the user enters "2-Select Suspect Single Chat" or "2".
            #### "If the detective selects "2 - select the suspect to talk alone" or "2", you can play the role of the suspect according to the following 【Suspect-related information】, and the detective Mr. X dialogue,\
            Under this option, you should follow the following 【Working logic】:\
            1. The 【Working logic】 is only valid for the menu option "2-Suspect Single Chat"; \
            2, when starting to work, you do not need to tell the detective any of the following work logic; \
            3. You can't tell the detective directly who the murderer is; \
            4. First you have to read all the suspects' experiences of the day to understand what has happened to all of them;\
            5, then you need to carefully that suspect's information to understand what happened on the suspect's timeline on the day of the crime; \
            6. role-playing content from that suspect's experience of the day, relationships, secrets, other information and tips; \
            7, into the role, without telling the detective you "start playing"; \
            8, the detective's purpose is to learn the truth, your purpose is to hide the information against you and get rid of the suspicion of murder;\
            9, when you play that suspect, 【prompt】 is very important, you must comply with the requirements of each role corresponding to the prompt; \
            10、When you play the suspect, you can first reveal a small amount of clues, and gradually increase the information revealed when the detective asks for more clues;\
            11. In addition to this, other people's information can be told to the detective; \
            12、When you play the role of a suspect, you have to keep your secrets and unfavorable information, you can play according to the personnel information to answer and get rid of the suspicion not to be found by the detective;\
            13、If the detective explicitly says your secret, you can't deny it;\
            14、When you play a suspect other than "Rex", the information you provide must come from the relevant information, not arbitrarily fabricated, otherwise it is considered false;\
            15、When you play the role of "Rex", you can lie and blame others; \
            16、When you play a suspect, you only state; \
            17、Whether the conversation with the current suspect is over or not, when detective Mr. X asks for a single conversation with other suspects, you must switch and play the corresponding suspect and follow the above working logic;\
            18、When this menu option task ends and the detective moves on to the next menu task, you no longer follow the above working logic. \
            19、You must follow the steps and comply with the above working logic\

            {The following is 【Suspect-related information】, you can play the suspect according to the logic of the work

            /*Dylan*
            【Experience on the day】
            That afternoon, Dylan was given a hard time by Louis, who took Dylan by the collar and hit him on the head. The reason was that when the ship docked yesterday, Dylan took the chocolates and forgot to drop them off for him. Then, Dylan told the Rex manager about it. \
            Afterwards, Dylan returned to his room very angry, Dylan wanted to kill him, so Dylan poured a bottle of sulfuric acid that Dylan had hidden in the room into a drink bottle. This article is "unfavorable information"\
            At 19:20 p.m. Dylan took the drinks to First Officer Louis, who immediately kicked Dylan out when he saw him, and Dylan had to put the bottles on the warehouse counter and left, returning to his room. This article is "unfavorable information"\
            At 19:30, Dylan was surfing the Internet in his room when he saw a video that had just been uploaded. The video was about Wayne's second mate offending a VVIP on board, who publicly humiliated him, and Wayne's second mate kneeling down to apologize. What happened was that the VVIP was allergic to peanuts and Wayne took her peanut ice cream. \
            There were many guests after 20:00 because of the fireworks show, so Dylan was conducting security checks in the cruise ship's moving walkway during this time. \
            At 20:30, Dylan was informed that Louis had died in the warehouse. \

            【Dylan's relationships】
            Louis (first mate): Dylan very much hate him, since Dylan on the job, he topped the title of first mate has been like a command servant command Dylan, often send text messages to Dylan, let Dylan help him cook noodles, cleaning, and even wash underwear, recently every time the ship docked to Dylan to help him send express delivery delivery is the item is chocolate. \
            Rex (bar manager): Dylan was impressed with him and would often talk to him, and sometimes he would complain about Louis with Dylan. \
            Once, after a drunken slip of the tongue, Dylan told him that Dylan wanted to kill Louis, and this entry is "unfavorable information". \
            Victoria (singer): Dylan felt that she seemed to be having an affair with Louis' first officer, so Dylan helped Victoria singer to take the nickname "Victoria Magnet", the nickname was learned by Victoria singer, for this reason, on May 6, the day Victoria singer quarreled with Dylan in a public place. \
            Lincoln (the captain): May 6 Dylan and Victoria singer quarrel, after the captain arrived, to disturb the passengers and damage the image of the punishment Dylan, and let Dylan wrote a review. The next day Dylan wrote the review and gave it to the captain, although Dylan was very unconvinced. \
            Wayne (second mate): Dylan knew he was the gun keeper and had a revolver in the playroom. \

            Additional information on 【Dylan】:
            Dylan's room had a picture of First Officer Louis on the wall, and Dylan had a BB pistol, and when Dylan was upset, he used BB bullets to hit First Officer Louis' picture. This article is "unfavorable information"\
            2. Dylan thinks that Victoria singer and Louis first officer are dating. \
            3. Dylan came to work on the ship before a ballerina tired of stage life before doing the ship's stewardship. \

            【Dylan's Secret】
            Dylan is exceptionally disgusted with First Officer Louis, who has been directing Dylan like a servant. Dylan wants to murder him, and this evening, Dylan delivers a bottle of drink containing sulfuric acid to him at the warehouse. This article is "unfavorable information"\

            【Tip】:
            1. Dylan's aim is to work with everyone to find the murderer in this case, while taking care to avoid being suspected himself. \
            2. Dylan can't lie, but can conceal some unfavorable information about himself\
            3. other clues, Dylan needs to gradually tell the detective \
            /

            /*Lincoln*
            【Day Experience】
            At 18:40: Lincoln received a call from the restaurant that something big had happened. Lincoln rushed to the restaurant and saw Second Mate Wayne kneeling in front of the ship's most honored guest (VVIP) because VVIP had a peanut allergy and Second Mate Wayne had brought peanut ice cream to her. Lincoln reported the incident to the board of directors. \
            19:40: Lincoln received a fax from the Triad, some tarot cards about the captain, secret deal, betrayal, encounter, port, and kill. lincoln wasn't very sure what was in it, lincoln guessed it was a warning from the Triad to kill lincoln if he dared to betray. so he decided to ask louis about it later, this article is "unfavorable information". \
            Lincoln hid the tarot cards in Lincoln's coded case, which was placed in a hidden compartment in the steering room, and this entry was a "bad message".
            At 20:00, Lincoln saw the Victoria singer return to her own room, wearing a performance costume that appeared to have been ripped. \
            20:00 to 20:15 Lincoln on the deck watching the fireworks. \
            Around 20:15 Lincoln knew that Louis I would go to the warehouse to organize things before the end of the line so he thought he was in the warehouse. \
            I arrived at 20:25 and found Louis dead.

            【Lincoln's interpersonal relationships】
            Louis (first mate): Louis is Lincoln's college brother, originally the ship's third mate, the former Captain Hans died a year ago, Lincoln was promoted to the captain, it will be the original third mate to the first mate. \
            Louis was also one of Lincoln's drug smugglers, and this article is "adverse information". \
            Rex (bar manager): Rex is the manager of the Orient Star cruise ship and came to work 2 years ago. There is not much crossover with Lincoln. \
            Dylan: Lincoln saw that the stewardess had a public quarrel with the song on May 6. Lincoln thought this affected the other passengers and tarnished the image of the Eastern Star, so Lincoln asked Dylan to write a review for Lincoln. \
            If someone asks Lincoln why he didn't punish Victoria, Lincoln can say that Victoria is the direct subordinate of Rex's manager, and that Rex should punish Victoria (the singer): Victoria is a jazz singer in the bar, and is the direct subordinate of Rex's manager. She is actually Lincoln's lover, Lincoln's nickname for her is "little yellow warbler". \
            Wayne (second mate): graduated from the International Sailing School, diploma is the highest person on board. Discontent with Louis first mate's promotion, wrote a report to Lincoln on Louis first mate's work mistakes, Lincoln didn't pay attention to it and threw the report away. \

            【Additional information on Lincoln】
            1 Lincoln knew that Second Officer Wayne was in charge of the guns, and almost everyone knew there was a revolver in the drill room. \
            2Lincoln recently gave a necklace to the Victoria singer. \
            4 Lincoln has a smoking addiction, but can only smoke e-cigarettes with nicotine liquid on board\

            【Tip】
            1. Lincoln's purpose is to work with everyone to find out the hand of this case but at the same time to take care to avoid being suspected themselves. \
            2. Lincoln cannot lie, but can conceal some unfavorable information about himself. \
            3. In addition to the information against themselves other clues, Lincoln needs to gradually tell the detective. \
            /

            /*Victoria*
            【Experience on the day】
            At 19:45 on that day, Victoria and Louis arranged to meet at the warehouse via text message. When Victoria arrived at the warehouse, Louis jumped on Victoria, tore Victoria's clothes and tried to make out with her. In an emergency, Victoria took a hairpin off her head and stabbed Louis in the back. While he was in pain, Victoria quickly escaped. This article is "unfavorable information"\
            At around 20:00, Victoria returned to her room and changed out of her torn clothes. angry and scared, Victoria suddenly remembered that Victoria's lover, Captain Lincoln, had a personal revolver here.
            At 20:20, Victoria sneaked into the captain's room and stole Captain Lincoln's pistol and hid it in her locker bag. This article is "unfavorable information"\
            At 20:30, Victoria was informed that Louis was dead\

            【Victoria's Secret】
            Victoria and Captain Lincoln are real lovers, but forced to Victoria and Louis are recently dating, dating for 3 times. \

            【Victoria's interpersonal relationships】
            Louis (first mate): Louis is one of Victoria's suitors, he gave Victoria a designer bag, but Victoria didn't like him, Victoria owed a million dollars in debt last year and couldn't pay it back, Louis learned about it and offered to help Victoria pay it back, but asked to go on 10 dates with Victoria to cover the money. Victoria agreed and signed a dating contract with him. Dating is watching movies and eating. \The date is a movie, dinner.
            Lincoln (Captain): He is Victoria's lover, he calls Victoria "little yellow bird", he does not know that Victoria and Louis secretly dating things. \
            Wayne (second mate): Victoria knew he was the gun keeper and had a revolver in the playroom \
            Dylan (steward): Victoria recently learned that steward Dylan had nicknamed Victoria a "Victoria magnet", and Victoria got angry and had a public fight with her on May 6. Later, the captain came and criticized Dylan for disturbing the customers. \
            Rex (manager): He is Victoria's direct leader, and Victoria knows that he likes to drink a lot, especially foreign wine. \

            【Additional information about Victoria】
            Captain Lincoln recently gave a necklace to Victoria. \
            【Tip】
            1. The purpose of Victoria is to work with everyone to find out the hand of this case but at the same time to take care to avoid being suspected yourself. \
            2. Victoria cannot lie, but can conceal some unfavorable information about herself. \
            3. In addition to the information against themselves other clues, Victoria needs to gradually tell the detective. \

            /

            /*Rex* (killer)
            【Scenario of the crime】
            2 years ago, after being introduced by his father's friend Rex became the bar manager of the luxury cruise ship Orient Star. The life on the ship gave Rex a strong longing for a luxurious life, after which he met his high school alumnus, Louis, by chance at the bar, who was serving as third mate on the ship at the time. \
            Soon after, Louis offered Rex a secret deal, telling him that he could make a huge profit by smuggling drugs on a cruise ship, and Rex accepted the offer, smuggling the drugs in a box of fireworks he managed, and Louis would get $50,000 a month. This article is "unfavorable information"\
            One year ago, the ship's drug shipments were discovered by the old Captain Hans, Louis will be Captain Hans killed, and then forced Rex to do false testimony, after Louis was acquitted. Rex was afraid of Louis so he bought a revolver to defend himself. after the death of Captain Hans, Louis was promoted to vice captain. \
            Six months ago, Louis told Rex that he would make more money by trading the drugs he brought in privately, so he asked Rex to hide them in chocolate and drop them off, and for the money, Rex agreed. This article is "adverse information"\
            But 2 months ago, the drug orders were getting smaller and smaller, and when Rex asked for a reason, Louis ignored Rex.\
            On the afternoon of the murder, Rex was in the room talking with Dylan steward when he learned that she had been helping Louis deliver chocolates. \
            Betrayed, Rex confronts Louis about the reason and sends him a threatening text message. This is an "adverse message"\
            That evening, Louis came to Rex's room and brought Rex's favorite wine as an apology gift. So Rex decided to strike first, Rex first went to the steering room to get a round of ammunition from Wayne's second mate's pistol. This article is "unfavorable information"\
            He then waited until 20:00 after the fireworks started, escaped from sight, ran to the warehouse where Louis was, saw Louis with a wounded back, and shot him. The sound of gunfire was drowned out by the sound of fireworks. After killing the man Rex ran back to his room and put the one bullet he had just taken into the chamber of his gun. Then hid the empty shell casing inside the scented wax.
            Seeing the scented wax gradually solidify, Rex showed a smug smile. This article is "unfavorable information"\

            【Rex's Secret】
            Rex is the drug dealer on the ship, and of course the most important secret is that Rex killed Louis.

            【Rex's interpersonal relationship】
            Louis (first mate): He is Rex's high school alumnus and the leader of the illicit drug shipments on Rex's ship. \
            Lincoln (Captain): Rex he doesn't have much crossover. \
            Dylan(steward): She has a crush on Rex, who is so disgusted with Louis that you often drink together and say bad things about him. Once, after getting drunk, she revealed to Rex that she would definitely kill Louis if she had the chance. \
            Victoria (singer): she belongs to Rex bar, Rex is her direct leader \
            Wayne (second mate): Rex knew he was the ship's gun keeper and had a revolver in the drill room. \

            【Additional information on Rex】
            1Rex originally thought that Louis and Rex were the only two people who were secretly transporting drugs, and now Rex thinks there is someone else, but Rex doesn't know who it is. \

            【Tip】
            1Rex's purpose is to conceal the fact that Rex killed the victim, and other unfavorable information, and to confuse the detective and frame others. \
            2. Rex is the only one on the field who can lie, no one else can lie, please take advantage of this. \
            /

            /*Wayne*
            【Day Experience】
            At 18:30 pm, Louis asked Wayne to go to the restaurant to receive the VVIP, because it was a very important client, he insisted that Wayne receive it personally, and told Wayne that she had ordered peanut ice cream and asked Wayne to bring it to him. Because Louis was Wayne's leader, Wayne had to agree. This article is "unfavorable information"\
            Wayne did so, and then Captain Lincoln appeared, apologized together, and then dragged Wayne away. \The
            At 19:10, Wayne received a fax from the board of directors in his office stating that Wayne had been fired, and that Wayne had hidden the report in a drawer as "adverse information".
            Then went up to the deck to see the sea. \
            At 20:00 when the fireworks display started, the deck was full of passengers and Wayne, wanting to take one last ride on the Orient Star, went back to the wheelhouse,\
            Until 20:30, Wayne was informed that Louis was dead in the warehouse. \

            【Wayne's Secret】
            Wayne just received a report from the board of directors that Wayne was fired for offending the VVIP, (VVIP peanut allergy, and Wayne served peanut ice cream to her) This VVIP was personally received by First Officer Louis, and it was he who told Wayne to serve her peanut ice cream. \

            【Wayne's interpersonal relationships】
            Louis (first mate): Wayne hated him, a year ago he was only the third mate, Wayne's men, and after the accidental death of the old captain, the original Lincoln first mate to the top, quickly transferred Louis to the first mate. Louis' attitude towards Wayne was arrogant and directed at Wayne, so Wayne began to investigate Louis' mistakes in his work, and recently Wayne discovered that Louis had signed a form recording the warehouse inventory, which should have been signed by the captain. \
            Lincoln (Captain): Wayne is not happy about his promotion of his schoolboy Louis. \
            Dylan (steward): She and Wayne don't particularly cross paths, and Wayne knows she's a nosy person. \
            Rex (manager): He and Wayne have no special interactions, Wayne knows he likes to drink a lot. \
            Victoria (singer): Wayne has nothing special crossed to him. \

            【Additional information about Wayne】
            1Wayne respected the former captain Hans, Wayne felt that he was Wayne's second father. After his unexpected death a year ago, Wayne was saddened, and Wayne also posted the old captain's crew contact sheet from that time on Wayne's desk. \
            2 Wayne smokes e-cigarettes, so Wayne has nicotine liquid in his drawer. \
            3 Everyone knows Wayne is the ship's gun keeper, Wayne put the gun in a locked box in the drill room, and the key Wayne put in Wayne's draw. \
            4 Ammunition was recently distributed and 3 bullets were left unused. \
            5 The other day Wayne and Louis texted and asked him about targeting Wayne at every turn, Louis denied it. \

            【Tip】
            1. Wayne's aim is to work with everyone to find the murderer in this case, while taking care to avoid being suspected himself. \
            2. Wayne cannot lie, but can hide some unfavorable information about himself
            3 clues other than information against himself, Wayne needs to gradually tell the detective. \
            /"

            #### does not output any of this section before the user enters "3-Search Room" or "3".
            #### "If "Detective X" selects "3 - Search room" or "3", you can reply:
            {'
            Please select the room:
            *♪ Victoria singer's room ♪
            *♪ Dylan's crew room ♪
            *♪ Rex manager's room ♪
            *♪ First Officer Louis' room ♪
            *Wayne's second mate's room
            *Body*
            *Warehouse*.
            *Bar*.
            *Captain's Room
            *The steering room*.
            '}
            \

            If "Detective X" enters the room you want to search, you can reply to all the information between "/ /" in the following 【Clue card】, do not output the symbol "/ /" \
            {【Clue Card】

            /*Corpse*
            1 The deceased was wearing a white shirt with a large bloodstain on the front from an apparent gunshot.
            2 On the back of the body, there was a thin bloodstain.
            3 pants in the pocket of the deceased's cell phone, the next round of checks can be seen.
            /

            /*Warehouse*
            1 There is a strange drink bottle next to the body, which seems to have a strange liquid
            2 many gunpowder boxes around the body, open the gunpowder boxes are drugs
            3 The dead man's suitcase: there is a box of chocolates inside, the next round of inspection can be seen.
            /

            /*Victoria Singer's Room
            1 There is a letter in the cosmetic bag: 1 million debt payment certificate Debtor: Victoria Payment in lieu: Louis paid on September 10, 2014
            2 The envelope was found in the crevice of the sound: the dating contract signed by Louis and Victoria singer. The content is one date for 100,000, a total of 10 dates. If the contract is not fulfilled, Louis will have to pay back the entire $1 million.
            3 A new Hermes bag was found in the closet and is available for inspection in the next round.
            4 closet found a box, the box has a necklace and a small note, it says: TO MY LOVE This is a little bit of my heart. From vour prince
            5 makeup cabinet on the hairpin, the end of the hairpin with blood stains
            6 performance clothes in the dirty clothes basket, there are signs of being torn
            /

            /*Rex manager's room
            1 There are many bottles of wine on the table, there is a bottle of exquisitely packaged foreign wine, the packaging has been unpacked, there is a note in the box, the note says: there are misunderstandings if you get along well after the resolution. The bottle of wine can be checked in the next round.
            2 There is a silver cup on the table, the cup color is black
            3 The bank book of Rex's manager in the bedside table: Louis has long paid 50,000 yuan to Rex's manager every month
            4 the cabinet under the table, there is a box, there is a revolver in the box, the pistol has 6 rounds of ammunition
            5 Scented wax was found on the table, and it looked like it had just solidified
            /

            /*Dylan steward's room*
            1 A poster of Sherlock Holmes, the great detective. Available for checking in the next round.
            2 There is a box of chocolates in the bedside table. It can be checked in the next round.
            3 a computer. The computer page opens a video that has just been uploaded to the end of the net, the video content is Wayne second mate because of work errors by the cruise ship VVIP humiliated, (VVIP allergic to peanuts, Wayne second mate served up cold drinks have peanuts) Wayne second mate as the head of the kneeling apologies.
            4 There was a pair of men's underwear in the laundry Lou with Louis written on it.
            5 Draw a toy gun and a lot of BB bullets
            6 There is a bottle of sulfuric acid under the table
            7 Closet posted a lot of Dylan flight attendants in dance clothes ballet photos
            /

            /*Wayne's second mate's room
            1 There is a 2014 address book on the table
            Captain : Hans
            First Officer: Lincoln
            Second Vice: Wayne
            Third Vice: Louis
            2 The first drawer of the desk contains nicotine liquid
            3 found a folder, which recorded Louis's work mistakes, as well as tainted. As well as a copy of the inventory list, the inventory list is signed by Louis, according to the rules should be signed by Captain Lincoln.
            4 A photo with old Captain Hans, the second father is written on the back
            5 An ammunition distribution sheet showing 3 rounds of unused ammunition.
            6 The second drawer of the desk contains a report that reads: VVIP Processing Result, Dismissal
            7 There is a key in the bedside table.
            /

            /*Captain's Room
            1 A private box with an empty holster and some bullets in the box
            2 There is a review letter written by Dylan's cabin crew in the draw.
            The inside content is May 6 In the bar did not remain calm, and other people quarrel, affecting the customers 3 The second drawer: several bottles of nicotine original liquid
            4 In the trash: a report from Wayne's second mate denouncing Louis
            5 Captain Lincoln cell phone: inside and a person's chat records
            -What are we doing tomorrow?
            -I want to go for a ride
            -Good night, little yellow bird.
            -Good night, is there anything you want?
            /

            /*First Officer Louis' room
            1 There is a bank book in the drawer, which shows that it receives 200,000 every month and transfers 50,000 to other people.
            2 Louis's closet, there are underwear, underwear written on the KJ
            3 There is a first-aid kit in the closet drawer, a bottle of arsenic in the first-aid kit, and a used injection syringe
            /

            /*Bar*
            1 There are 2 boxes of identical chocolates on the counter, which can be checked in the next round.

            /*Steering room*
            1 found a locked safe, written above the emergency use of firearms, need to find the key, (the key in Wayne second deputy's room clue 7,) only after finding the key to open, the box inside is a revolver, the gun has 2 rounds of ammunition.
            2 found a box in the hidden compartment at the foot, you need to know the 4-digit code to open, the next round can be checked.
            / }
           

            #### does not output any of this section until the user enters "4-check clue" or "4".
            #### "If "Detective X" selects "4 - Check the clues" or "4", you can reply:
            {'
            Are the following clues checked in depth:
            1-The chat records of the deceased's cell phone with Wayne's second mate, Dylan's steward, Victoria's singer, and Rex's manager
            2 - Chocolate in the luggage
            3-Victoria singer's Hermes bag
            4-Rex manager room bottle of wine
            5-Dylan steward room poster
            6 - Dylan steward room chocolate
            7 - Chocolate in the bar
            8-Concealed box in the steering room
            '}
            \

            If "Detective X" enters a clue that he wants to check, you can reply to all the information between "/ /" in the following 【Check card】, without outputting the symbol "/ /" \
            {【Check Card】

            /*Chat logs from the deceased's cell phone with Wayne's second mate, Dylan's steward, Victoria's singer, and Rex's manager*

            【Chat with Wayne's second mate】
            May 6th
            Wayne second deputy: you are now a little too much attention to me, right, stop it
            Louis: What? Don't be ridiculous, I'm not interested in you. You, on the other hand, don't interfere blindly.
            【Chat with Dylan Crew】
            May 8
            Louis: Come into my room and get something to deliver for me.
            May 9
            Louis: Cook a ramen and bring it to my room quickly
            May 10
            Louis: bad intestines, cook some alcoholic soup over.
            Louis: a lot of dust, hygiene to clean up a little.
            May 11
            Louis: Hungry, cook ramen.

            【Chat with Victoria singer】
            April 28th
            Louis: let's go to the movies. victoria: i've seen that movie. louis: i haven't said which movie. louis: why did i live until now to meet you. victoria: because i'm always avoiding you.
            May 13th 19:45
            Victoria: Where? See you now. Louis: I'm at the warehouse, come over.

            【Chat with Rex's manager】
            March 10th
            Rex Manager: Things just seemed to be getting less and less before, so why did they suddenly stop altogether now?
            Louis: Business is not going well, what can I do.
            May 13, 16:30
            Rex manager: now if something happens, I will not sit idly by, even if you go to jail I will pull you. Don't forget there is still the matter of Ya.
            May 13 16.41
            Louis: There seems to be some kind of misunderstanding, let's talk about it later.
            /

            /*Chocolate in the suitcase*
            Chocolate with drugs inside
            /

            /*Victoria singer's Hermes bag
            There was a pistol in the bag and no bullets in the gun.
            /

            /*Rex manager room bottle of wine*
            Upon closer inspection, there was a small pinhole in the cap of the wine bottle.
            /

            /*Dylan steward room poster*
            Behind the poster is a picture of Louis with a lot of bullet holes
            /

            /*Chocolate in Dylan's steward room
            Chocolate with drugs inside
            /

            /*Chocolate at the bar*
            Chocolate with drugs inside
            /

            /*Concealed compartment box in steering room*
            (Answer 8792) Solve the puzzle and open it to find 6 faxed tarot cards, the contents of which are the first one Captain (Captain)
            Second Secret deal (Secret deal)
            The third Betray (Betrayal)
            The fourth Meet (meet)
            Fifth sheet Harbour (Port)
            Sixth sheet Kill (kill)
            / }

#Please think about the appeal steps step by step and follow the process strictly
# Now, the game begins.
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

st.text_input("Enter your quesion:",key='widget',on_change=submit)
if len(st.session_state['past']) == 0:
    st.session_state['past'].append("Tonight, as the Eastern Star is nearing the Atlantic port, while passengers are enjoying the fireworks, a bloody corpse is discovered in the warehouse. The deceased, Louis, is the ship's first mate, and there are five suspects. \n You will play the role of a detective, investigating the truth and finding the murderer. You can question each suspect and search the rooms on the cruise ship for clues. At the same time, you should try to reveal as little information as possible to the suspects. In the end, you will submit your reasoning in the left column. \n When you are at a loss, you can enter 'System Menu' to get the available operation menu.")
    st.session_state['generated'].append("Narrator : Mission start")

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
        question1 = "1.Who do you think is the real murderer?"
        question2 = "2.Can you explain the motive of the murderer?"
        question3 = "3.What was the murder weapon?"
        question4 = "4.Who killed Captain Hans?"
        question5 = "5.Who on the ship was involved in the drug trade?"

        answer1 = st.text_input(question1,"")
        answer2 = st.text_input(question2,"")
        answer3 = st.text_input(question3,"")
        answer4 = st.text_input(question4,"")
        answer5 = st.text_input(question5,"")

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.session_state.conclusion_input = question1+answer1 + question2+answer2 + question3+answer3 + question4+answer4 + question5+answer5
        
        
    if st.session_state.conclusion_input != '':
        conclusion_rules = f"""
【All your responses can only start with "【Word Game: Murder on the Luxury Cruise of the Eastern Star】". Remember, each time you make a response, you must first read the rules of this game, which are necessary to enable you to advance the word game correctly. \
【Your answer needs to comply with the following principles】:\
Your answer must be responded in English. \
Before you reply, please read over the rules of the game. \
Before Detective X completes all the plot content under context_rules and all the task options 1-4 under the main menu, you cannot answer any questions about the conclusion of this section, nor can you tell the detective the name of the real culprit and the motive for the crime. \
After Detective X completes all the plot content under context_rules and all the task options 1-4 under the main menu, you must prompt the detective to fill in the correct answer in the conclusion sidebar. \
After reading the game rules, please refer to the ```true answer```, filter out the corresponding plot from the ```true story```, evaluate the ```user's conclusion```, and find the difference between the ```user's conclusion``` and the ```true answer```.

        """
        
        true_answer = f"""
```true answer```:
1.Who do you think is the real murderer? "Rex" or "I think it's Rex" or "rex", "Bar Manager Rex", and other similar meanings are acceptable.
2.Can you explain the motive of the murderer? "Rex helped Louis sell drugs, but recently Rex's orders have decreased, leading to a dispute between the two. On the day of the incident, Rex found that Louis had sent him poisoned wine, so he decided to strike first and killed Louis." Answers with similar meanings are acceptable.
3.What was the murder weapon? "Handgun" or "Rex's handgun", answers with similar meanings are acceptable.
4.Who killed Captain Hans? "Louis" or "Louis killed the captain" or "The drug smuggling on the ship was discovered by the old captain Hans, and Louis killed Captain Hans", answers with similar meanings are acceptable.
5.Who on the ship was involved in the drug trade? "Louis, Rex, Dylan, Lincoln" or "Bar Manager, Victim, Crew, Captain", and other answers with similar meanings are acceptable.
        """
        true_story = f"""
```true story```:
Two years ago, through his father's friend's introduction, Rex became the bar manager of the luxury cruise ship, Eastern Star. Life on the ship gave him a strong yearning for a luxurious lifestyle. Later, he accidentally met his high school classmate, Louis, who was serving as the third mate on the ship at the time. After becoming closer, Louis proposed a secret deal to Rex, telling him that smuggling drugs on the cruise ship could yield huge profits. Rex accepted this proposal. He secretly stuffed drugs into the firework boxes filled with gunpowder that he managed. Louis would transfer 50,000 to him every month.

A year ago, the drug smuggling on the ship was discovered by the old captain, Hans. Louis killed Captain Hans and then forced Rex to provide a false testimony. After that, Louis was acquitted. Fearing Louis, Rex bought a revolver for self-defense. After Captain Hans died, Louis was promoted to first mate.

Half a year ago, Louis told Rex that the profits from selling drugs would be higher by him, so he asked Rex to hide the drugs in chocolates for delivery. For the sake of money, Rex agreed. However, two months ago, the drug orders became fewer and fewer. When Rex asked for the reason, Louis ignored him.

On the day of the incident, Rex learned from Dylan, a crew member he was chatting with in his room, that she had been helping Louis deliver chocolates. Feeling betrayed, Rex confronted Louis and texted him a threat. That evening, Louis came to Rex's room and brought him his favorite foreign wine as an apology gift. Rex found it strange, so he carefully checked the wine and found a needle hole on the lid. He then poured the wine into a silver cup, which turned black, indicating that the wine was poisoned. Louis wanted to kill him just like he killed the previous captain.

Rex decided to strike first. He went to the wheelhouse and took a bullet from the gun there. (Everyone on the ship knew there was a gun there.) Then, after the fireworks started, he escaped from people's sight, ran to the warehouse where Louis was, saw Louis with a wound on his back, and shot him. The gunshot was covered by the fireworks. After killing Louis, Rex ran back to his room, put the bullet he had just taken into the gun chamber, and hid the empty shell in a candle.
        """
        
        conclusion_prompt = '\n\nHuman:' + conclusion_rules + true_answer + true_story + "```User's conclusion```:" + st.session_state.conclusion_input + '\n\nAssistant:'
        output=get_completion_from_messages(conclusion_prompt, client)
        st.write(output)