import os
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.summarization import summarize
import summary
from operator import itemgetter
import nltk
import summary2 

#give the path of the input file below
input_file='text.txt'
a=open(input_file,'r')
text=a.read()

#no need to change path for the next code
#delete this file from specified folder if you are not running it for the first time
c=open('singles.txt','a+')

list_of_values1=([n for n in range(len(text)) if text.find(':', n) == n])
list_of_values1.append(len(text)+1)
list_of_values2=([n for n in range(len(text)) if text.find('\n', n) == n])
list_of_values2.append(len(text)+1)


start=0
for i in range(len(list_of_values2)):
    if i==(len(list_of_values2)-4):
        # c.writelines(text[list_of_values2[i-1]:])
        break
    else:
        sentences = nltk.sent_tokenize(text[(list_of_values1[i]):(list_of_values2[i])])
        print(len(sentences))
        if len(sentences) > 4:
            # single_text=summarize(text[(list_of_values1[i]):(list_of_values2[i])],ratio=0.25)
            single_text = summary2.KmeansCluster().kmeanSummary(text[(list_of_values1[i]):(list_of_values2[i])])
            print(single_text)
            c.writelines(text[(start):(list_of_values1[i])]+": "+str(single_text) +"\n")
            start=list_of_values2[i]
        else:
            single_text=(text[(list_of_values1[i]):(list_of_values2[i])])
            c.writelines(text[(start):(list_of_values1[i])]+single_text +"\n")
            start=list_of_values2[i]

c.close()

b=open('singles.txt','r')
modified_text=b.read()
print('********************')
print(modified_text)
ratio=0.5
output_file='summary4.txt'
sum = modified_text
# sum=(summarize(modified_text,ratio=ratio))
# sum = summary.TextRank().summary(modified_text)

b=open(output_file,'w')
b.write(str(sum))

os.remove('singles.txt')