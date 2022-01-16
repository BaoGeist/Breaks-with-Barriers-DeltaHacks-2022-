from concurrent.futures.thread import _worker
from importlib.util import set_package
import time, re, random
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import requests
from twilio.rest import Client

#function to message the user given a number and a message
def function_message(number, message):
    account_sid = 'AC034ad1797070215a35dc3578bd033fbb'
    auth_token = '872de64fad709916fb7b44ac962dc32b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to = number,
        from_= '+19402898466',
        body = message
    )

#function to get random quotes
#returns the quote in a list with quote as the first index and the author as the second
#warning, there are cases with no authors
def function_quote():
    f = open('quotes.csv', 'rt')
    lstQuote = []
    for line in f:
        lstQuote.append(line)
    f.close()
    strQuote = lstQuote[random.randint(0, len(lstQuote))]
    splitQuote = strQuote.split('","')
    splitQuote[0] = splitQuote[0].strip('"')
    splitQuote[1] = splitQuote[1].strip('"\n')
    splitQuote[0], splitQuote[1] = splitQuote[1], splitQuote[0]
    return(splitQuote)

#function to create study time analyzation
#creates a plot, and saves it as a png
def function_stats():
    strRaw = ''
    lstStat = []
    f = open('stat.txt', 'rt')
    for line in f:
        strRaw += line
    f.close()

    lstDays, lstHours = [], []
    lstStat = re.findall(r'(\d\d\d\d-\d\d\-\d\d) (\d)', strRaw)
    for item in lstStat:
        lstDays.append(item[0])
        lstHours.append(int(item[1]))

    lstDaysE = []
    lstStor = lstDays[0].split('-')
    dayI = date(int(lstStor[0]), int(lstStor[1]), int(lstStor[2]))
    for days in lstDays:
        lstStor = days.split('-')
        dayF = date(int(lstStor[0]), int(lstStor[1]), int(lstStor[2]))
        deltaTime = dayF - dayI
        lstDaysE.append(deltaTime.days)

    plt.style.use('seaborn-whitegrid')
    plt.scatter(lstDaysE, lstHours)
    plt.ylim(0, max(lstHours)+3)
    plt.ylabel('Number of Hours Studied')
    plt.xlabel('Days Since '+ lstDays[0])
    plt.title('Studied Hours Over Time')
    plt.savefig('figure.png')

#function to access study playlists
#returns type tuple
def spotify_playlists():
    base_url = 'https://api.spotify.com/v1/'
    client_id = 'fcffb0a533f64b7fac50468328ff7b33'
    client_secret = '0a91b5d6ab7c42a59a951a684c299ee0'
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    }
    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    featured_playlists_endpoint = 'browse/featured-playlists/?limit=5'
    featured_playlists_url = ''.join([base_url,featured_playlists_endpoint])
    response = requests.get(featured_playlists_url,headers=headers)
    playlists = response.json().get('playlists').get('items')
    playlist_names = set()
    playlist_descriptions = set()
    playlist_urls=set()
    for pl in playlists:
        playlist_name = pl.get('name')
        playlist_names.add(playlist_name)
    for pl in playlists:
        playlist_description = pl.get('description')
        playlist_descriptions.add(playlist_description)
    for pl in playlists:
        playlist_url = pl.get('external_urls')
        playlist_link=playlist_url["spotify"]
        playlist_urls.add(playlist_link)
    return playlist_names,playlist_descriptions,playlist_urls

#function to get name of user
def function_read(index):
    f = open('info.csv', 'rt')
    line = f.readline()
    f.close()
    lstStor = line.split(',')
    try:
        return float(lstStor[index])
    except:
        return lstStor[index]

#funciton that updates the info.csv
def function_update_info(user,email,time,level):
    row = [user,email,time,level]       
    str_output = ''
    for item in row:
        str_output += str(item) + ','
    f = open('info.csv', 'wt')
    f.write(str_output)
    f.close()

#function updates the info.csv file and returns the level in a float to be updated in the frontend
def function_time(intTime):
    user, email, time, level = function_read(0), function_read(1), function_read(2), function_read(3)
    time += intTime
    level += time/3600
    function_update_info(user,email,time,level)
    return(level)

#function that adds finished study sessions
#addpends to the file stat.txt
def function_add_stats(time):
    now = datetime.now()
    today = datetime.today().strftime('%Y-%m-%d')
    f = open('stat.txt', 'at')
    f.write("\n" + str(today) + " " + str(time))

#function for the long text descriptions in study techniques section of front end
#takes in index from 0 to 8, and returns the string with the description
def function_text_pop(index):
    lstText=[
        '''The SQ3R method is a reading comprehension technique that helps students identify important facts and retain information within their textbook. SQ3R (or SQRRR) is an acronym that stands for the five steps of the reading comprehension process.
Try these steps for a more efficient and effective study session:

Survey: Instead of reading the entire book, start by skimming the first chapter and taking notes on any headings, subheadings, images, or other standout features like charts.
Question: Formulate questions around the chapter’s content, such as, What is this chapter about? What do I already know about this subject?

Read: Begin reading the full chapter and look for answers to the questions you formulated.

Recite: After reading a section, summarize in your own words what you just read. Try recalling and identifying major points and answering any questions from the second step.

Review: Once you have finished the chapter, it’s important to review the material to fully understand it. Quiz yourself on the questions you created and re-read any portions you need to.''',
        '''Retrieval practice is based on the concept of remembering at a later time. Recalling an answer to a question improves learning more than looking for the answer in your textbook.
And, remembering and writing down the answer to a flashcard is a lot more effective than thinking you know the answer and flipping the card over early.

If you practice retrieval, you are more likely to remember the information later on. Below are some ways you can implement the retrieval process into your study routine.

Utilize practice tests: Use practice tests or questions to quiz yourself, without looking at your book or notes.

Make your own questions: Be your own teacher and create questions you think would be on a test. If you’re in a study group, encourage others to do the same, and trade questions.

Use flashcards: Create flashcards, but make sure to practice your retrieval technique. Instead of flipping a card over prematurely, write the answer down and then check.''',
    '''Spaced practice (also known as “distributed practice”) encourages students to study over a longer period of time instead of cramming the night before. When our brains almost forget something,
they work harder to recall that information.
Spacing out your studying allows your mind to make connections between ideas and build upon the knowledge that can be easily recalled later.

To try this technique, review your material in spaced intervals similar to the schedule below:

Day 1: Learn the material in class.
Day 2: Revisit and review.
Day 3: Revisit and review.
After one week: Revisit and review.
After two weeks: Revisit and review.

It’s important to start planning early. At the beginning of each semester, schedule some time each day just for studying and reviewing the material. Even if your exams are months away, this will help you hold yourself accountable.''',
    '''Not only does exercise fight fatigue, but it can also increase energy levels. If you’re struggling to find the motivation to study, consider adding an exercise routine to your day.
It doesn’t have to be a full hour at the gym. It can be a 20-minute workout at home or a brisk walk around your neighborhood. Anything to get your heart rate pumping. Exercising before you study:

Kickstarts brain function and can help improve memory and cognitive performance.
Releases endorphins, which can improve your mood and reduce stress levels.''',
    '''This method takes an active approach to learning that improves memorization and understanding of the topic.
Similar to the SQ3R method above, PQ4R is an acronym that stands for the six steps in the process.

Preview: Preview the information before you start reading to get an idea of the subject. Skim the material and read only the headers, subheadings, and highlighted text.

Question: Ask yourself questions related to the topic, such as, What do I expect to learn? What do I already know about this topic?

Read: Read the information one section at a time and try to identify answers to your questions.

Reflect: Did you answer all of your questions? If not, go back and see if you can find the answer.

Recite: In your own words, either speak or write down a summary of the information you just read.

Review: Look over the material one more time and answer any questions that have not yet been answered.''',
    '''The Feynman Technique is an efficient method of learning a concept quickly by explaining it in plain and simple terms. It’s based on the idea, “If you want to understand something well, try to explain it simply.”
What that means is, by attempting to explain a concept in our own words, we are likely to understand it a lot faster.

How it works:

Write the subject/concept you are studying at the top of a sheet of paper.

Then, explain it in your own words as if you were teaching someone else.

Review what you wrote and identify any areas where you were wrong. Once you have identified them, go back to your notes or reading material and figure out the correct answer.

Lastly, if there are any areas in your writing where you used technical terms or complex language, go back and rewrite these sections in simpler terms for someone who doesn’t have the educational background you have.''',
    '''The Leitner System is a learning technique based on flashcards. Ideally, you keep your cards in several different boxes to track when you need to study each set. Every card starts in Box 1. If you get
a card right, you move it to the next box. If you get a card wrong, you either move it down a box or keep it in Box 1 (if it’s already there).

Each box determines how much you will study each set of cards, similar to the following schedule:

Every day — Box 1
Every two days — Box 2
Every four days — Box 3
Every nine days — Box 4
Every 14 days — Box 5
''',
    '''Messy notes can make it hard to recall the important points of a lecture. Writing in color is a dynamic way to organize the information you’re learning. It also helps you review and prioritize the most
important ideas.

A recent study found that color can improve a person’s memory performance. That same study found that warm colors (red and yellow) “can create a learning environment that is positive and motivating that can help learners
not only to have a positive perception toward the content but also to engage and interact more with the learning materials.” It also reported that warmer colors “increase attention and elicit excitement and information.”

Writing in color may seem like a no-brainer, but keep these tips in mind:

Write down key points in red.
Highlight important information in yellow.
Organize topics by color.
Don’t color everything—just the most important information.''',
    '''If you’re a visual learner, try mind mapping, a technique that allows you to visually organize information in a diagram. First, you write a word in the center of a blank page. From there, you write
major ideas and keywords and connect them directly to the central concept. Other related ideas will continue to branch out.
The structure of a mind map is related to how our brains store and retrieve information. Mind mapping your notes instead of just writing them down can improve your reading comprehension.
It also enables you to see the big picture by communicating the hierarchy and relationships between concepts and ideas.

So, how do you do it?

Grab a blank sheet of paper (or use a tool online) and write your study topic in the center, such as “child development.”
Connect one of your main ideas (i.e., a chapter of your book or notes) to the main topic, such as “developmental stages.”
Connect sub-branches of supporting ideas to your main branch. This is the association of ideas. For example, “Sensorimotor,” “Preoperational,” “Concrete operational,” and “Formal operational.”
TIP: Use different colors for each branch and draw pictures if it helps.'''
    ]
    return lstText[index]
