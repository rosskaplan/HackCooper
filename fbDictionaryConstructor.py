import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from fbMessage import fbMessage
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
%matplotlib inline
pdb = {}
tdb = {}


def myDate2object(date):
    if date[date.find(':')-2] == ' ':
        date = date[:date.find(':')-1] + '0' + date[date.find(':')-1:]
    if date[date.find(',',12)-2] == ' ':
        date = date[:date.find(',',12)-1] + '0' + date[date.find(',',12)-1:]
    if date[date.find(':')+3] == 'a':
        date = date[:date.find(':')+3] + 'AM' + date[date.find(':')+5:]
    if date[date.find(':')+3] == 'p':
        date = date[:date.find(':')+3] + 'PM' + date[date.find(':')+5:]        
    date = date[:date.rfind(' ')]
    
    return datetime.strptime(date, '%A, %B %d, %Y at %I:%M%p')
        
def countOccurrences(str,subStr):
    i = 0
    c = -1
    endReached = False
    while not endReached:
        i = str.find(subStr,i)
        if i == -1:
            endReached = True
        i += 1
        c += 1
    return c
    
def getTimeSeries(sender,receiver):
    time = []
    first = pdb[sender][receiver][0].date
    for msg in pdb[sender][receiver]:
        time.append(msg.date)
    return time
    
def getPersonalMsgs(sender,receiver):
    msgs = []
    for msg in pdb[sender][receiver]:
        msgs.append(msg.text)
    return msgs

def wordsPerConversation(thread):
	countVector = []
	dateVector = []
	delta = timedelta(hours = 3)
	lastMessage = tdb[thread][0]
	words = 0
	for msg in tdb[thread]:
		if msg.date - lastMessage.date < delta:
			text = msg.text
			words += len( text.split())
		else:
			countVector.append(words)
			dateVector.append(msg.date)
			words = 0
		lastMessage = msg
	return dateVector,countVector
		
		
		
	

messagesFile = open('messages.txt','r')
text = messagesFile.read()

threadStartStr = '"thread">'
userStartStr = '"user">'
dateStartStr = '"meta">'
mesgStartStr = '</span></div></div><p>'

myUser = 'Cory Nezin'
c = 0
i = 0
N = 0
n = 0
done = False
while i != -1 and not done:
    i = text.find(threadStartStr,i) + len(threadStartStr)
    threadEnd = text.find('<',i)
    thread = text[i : threadEnd]
    if thread.find(myUser):        #If your own username is second
        nameEnd = thread.find(',')
        name = thread[:nameEnd]
    else:
        nameBegin = thread.find(',')
        name = thread[2+nameBegin:]
    i = threadEnd
    n = i
    N = text.find(threadStartStr,n)
    if N == -1:
        done = True
        N = len(text)
    N += len(threadStartStr)
    
    while n != -1:
        n = text.find(userStartStr,n)
        if n == -1:
            break
        n += len(userStartStr)
        
        if n > N:
            break    
        userEnd = text.find('<',n)
        sender = text[n : userEnd]
        #print 'user',user
        n = userEnd
        
        if sender == myUser:
            receiver = name
        else:
            receiver = myUser
        
        n = text.find(dateStartStr,n) + len(dateStartStr)
        dateEnd = text.find('<',n)
        date = text[n : dateEnd]
        dateObject = myDate2object(date)
        n = dateEnd
        #print 'date',date
        
        n = text.find(mesgStartStr,n) + len(mesgStartStr)
        mesgEnd = text.find('<',n)
        mesg = text[n : mesgEnd]
        n = mesgEnd
        
        message = fbMessage(dateObject,sender,receiver,mesg)
        
        if thread not in tdb.keys():
            tdb[thread] = []
            tdb[thread].append(message)
        else:
            tdb[thread].append(message)

        if message.sender in pdb.keys():
            if message.receiver not in pdb[message.sender].keys():
                pdb[message.sender][message.receiver] = []
            (pdb[message.sender][message.receiver]).append(message)
        else:
            pdb[message.sender] = {}
            pdb[message.sender][message.receiver] = []
            (pdb[message.sender][message.receiver]).append(message)
                
        i = n
        
for sender in pdb.keys():
    for receiver in pdb[sender].keys():
        pdb[sender][receiver].sort(key=lambda x: x.date)
        
for thread in tdb.keys():
    tdb[thread].sort(key=lambda x: x.date)

time1 = getTimeSeries('Cory Nezin','Brenda So')
time2 = getTimeSeries('Brenda So','Cory Nezin')

time3 = getTimeSeries('Cory Nezin','Ross Kaplan')
time4 = getTimeSeries('Ross Kaplan','Cory Nezin')
delta = timedelta(hours = 3)
#time = []
#length = []

#start = tdb['Cory Nezin, Ross Kaplan'][0]
#for msg in tdb['Cory Nezin, Ross Kaplan']:
#    if msg.date - start.date > delta:
#        plt.plot( (msg.date, msg.date), (0, 10000), 'k-')
#    start = msg

time5 = getTimeSeries('Cory Nezin','Gordon Macshane')
time6 = getTimeSeries('Gordon Macshane','Cory Nezin')
    
time7 = getTimeSeries('Cory Nezin','Joan Danielle Blanche')
time8 = getTimeSeries('Joan Danielle Blanche','Cory Nezin')

time9 = getTimeSeries('Cory Nezin','Grace T Lofudu')
time10 = getTimeSeries('Grace T Lofudu','Cory Nezin')

plt.figure(1,figsize=(10,10))

a1, = plt.plot(time1,np.arange(len(time1)),'r.',label='Cory->Brenda')
a2, = plt.plot(time2,np.arange(len(time2)),'ro',label='Brenda->Cory')
a3, = plt.plot(time3,np.arange(len(time3)),'b.',label='Cory->Ross')
a4, = plt.plot(time4,np.arange(len(time4)),'bo',label='Ross->Cory')
a5, = plt.plot(time5,np.arange(len(time5)),'g.',label='Cory->Gordon')
a6, = plt.plot(time6,np.arange(len(time6)),'go',label='Gordon->Cory')
a7, = plt.plot(time7,np.arange(len(time7)),'y.',label='Cory->Mom')
a8, = plt.plot(time8,np.arange(len(time8)),'yo',label='Mom->Cory')
a9, = plt.plot(time9,np.arange(len(time9)),'c.',label='Cory->Ex')
a10, = plt.plot(time10,np.arange(len(time10)),'co',label='Ex->Cory')
plt.legend(handles=[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10],loc=2)

time1 = []
time1c = []
time2 = []
time2c = []
time3 = []
time3c = []
time4 = []
time4c = []
time5 = []
time5c = []
time6 = []
time6c = []
words1 = ''
words2 = ''
words3 = ''
words4 = ''
words5 = ''
words6 = ''

for thread in tdb:
    for msg in tdb[thread]:
        time1.append( msg.date.hour + 1.0/60.0*msg.date.minute )
        words1 = "".join([words1 + '\n',msg.text])

for key in pdb['Cory Nezin']:
    for msg in pdb['Cory Nezin'][key]:
        time1c.append( msg.date.hour + 1.0/60.0*msg.date.minute )

for msg in pdb['Joan Danielle Blanche']['Cory Nezin']:
    time2.append( msg.date.hour + 1.0/60.0*msg.date.minute )
for msg in pdb['Cory Nezin']['Joan Danielle Blanche']:
    time2c.append( msg.date.hour + 1.0/60.0*msg.date.minute )
    
for msg in pdb['Ross Kaplan']['Cory Nezin']:
    time3.append( msg.date.hour + 1.0/60.0*msg.date.minute )
for msg in pdb['Cory Nezin']['Ross Kaplan']:
    time3c.append( msg.date.hour + 1.0/60.0*msg.date.minute )
    
for msg in pdb['Brenda So']['Cory Nezin']:
    time4.append( msg.date.hour + 1.0/60.0*msg.date.minute )
for msg in pdb['Cory Nezin']['Brenda So']:
    time4c.append( msg.date.hour + 1.0/60.0*msg.date.minute )

for msg in pdb['Gordon Macshane']['Cory Nezin']:
    time5.append( msg.date.hour + 1.0/60.0*msg.date.minute )
for msg in pdb['Cory Nezin']['Gordon Macshane']:
    time5c.append( msg.date.hour + 1.0/60.0*msg.date.minute )

for msg in pdb['Grace T Lofudu']['Cory Nezin']:
    time6.append( msg.date.hour + 1.0/60.0*msg.date.minute )
for msg in pdb['Cory Nezin']['Grace T Lofudu']:
    time6c.append( msg.date.hour + 1.0/60.0*msg.date.minute )
    
f,(ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True, sharey=False)
f.set_size_inches(10, 10,forward=True)
ax1.hist(time1,150,alpha = 0.5,normed = False,facecolor = 'orange',label='Total')
ax1.hist(time1c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax1.legend(loc=2)
ax1.set_title('Messaging Activity')
plt.ylabel('Frequency' , multialignment='center')
plt.xlabel('Time' , multialignment='center')

ax2.hist(time2,150,alpha = 0.5,normed = False,facecolor = 'yellow',label='Mom')
ax2.hist(time2c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax2.legend(loc=2)
ax3.hist(time3,150,alpha = 0.5,normed = False,facecolor = 'blue',label='Ross')
ax3.hist(time3c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax3.legend(loc=2)
ax4.hist(time4,150,alpha = 0.5,normed = False,facecolor = 'red',label='Brenda')
ax4.hist(time4c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax4.legend(loc=2)
ax5.hist(time5,150,alpha = 0.5,normed = False,facecolor = 'green',label='Gordon')
ax5.hist(time5c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax5.legend(loc=2)
ax6.hist(time6,150,alpha = 0.5,normed = False,facecolor = 'cyan',label='Ex')
ax6.hist(time6c,150,alpha = 0.5,normed = False,facecolor = 'black',label='Cory')
ax6.legend(loc=2)

for msg in tdb['Cory Nezin, Joan Danielle Blanche']:
    words2 = "".join([words2 + '\n',msg.text])

for msg in tdb['Cory Nezin, Ross Kaplan']:
    words3 = "".join([words3 + '\n',msg.text])
    
for msg in tdb['Cory Nezin, Sam Keene']:
    words5 = "".join([words5 + '\n',msg.text])
    
for msg in tdb['Monica Chen, Jocelyn Lai, Helena Zhu, Dennis Burgner, Matt Lee, Max Mogel, Brenda So, Andy Jeong, Ben Park, Anton Luz, Deven Jacobi, Nathan Gozar']:
    words6 = "".join([words6 + '\n',msg.text])


wordcloud1 = WordCloud(font_path='C:\Anaconda2\Lib\site-packages\wordcloud\DroidSansMono.ttf',
                          stopwords=STOPWORDS,
                          background_color='black',
                          width=1200,
                          height=1000
                         ).generate(words2)
                         
wordcloud2 = WordCloud(font_path='C:\Anaconda2\Lib\site-packages\wordcloud\DroidSansMono.ttf',
                          stopwords=STOPWORDS,
                          background_color='black',
                          width=1200,
                          height=1000
                         ).generate(words3)
                         
wordcloud3 = WordCloud(font_path='C:\Anaconda2\Lib\site-packages\wordcloud\DroidSansMono.ttf',
                          stopwords=STOPWORDS,
                          background_color='black',
                          width=1200,
                          height=1000
                         ).generate(words5)
                         
wordcloud4 = WordCloud(font_path='C:\Anaconda2\Lib\site-packages\wordcloud\DroidSansMono.ttf',
                          stopwords=STOPWORDS,
                          background_color='black',
                          width=1200,
                          height=1000
                         ).generate(words6)
      
g,((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, sharex='col', sharey='row')
g.set_size_inches(10, 10,forward=True)
ax1.imshow(wordcloud1)
ax1.axis('off')
ax2.imshow(wordcloud2)
ax2.axis('off')
ax3.imshow(wordcloud3)
ax3.axis('off')
ax4.imshow(wordcloud4)
ax4.axis('off')

h,(ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=False)
h.set_size_inches(10, 10,forward=True)
N = 50
convKernel = np.ones(N)/N
d0,v0 = wordsPerConversation('Cory Nezin, Brenda So')
d1,v1 = wordsPerConversation('Cory Nezin, Ross Kaplan')
d2,v2 = wordsPerConversation('Cory Nezin, Gordon Macshane')
d3,v3 = wordsPerConversation('Grace T Lofudu, Cory Nezin')
ax1.plot(d0,np.convolve(convKernel,v0,'same'),'ro',label='Cory <-> Brenda')
ax1.legend(loc=2)
ax2.plot(d1,np.convolve(convKernel,v1,'same'),'bo',label='Cory <-> Ross')
ax2.legend(loc=2)
ax3.plot(d2,np.convolve(convKernel,v2,'same'),'go',label='Cory <-> Gordon')
ax3.legend(loc=2)
ax4.plot(d3,np.convolve(convKernel,v3,'same'),'co',label='Cory <-> Ex')
ax4.legend(loc=4)

plt.show()
