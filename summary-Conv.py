import os
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.summarization import summarize
import summary
from operator import itemgetter
import nltk
import summary2 
import glob

class Summary(object):
    def SummaryConv(self, input_file ): 
        # input_file='article/text1.txt'
        a=open(input_file,'r')
        text=a.read()

        #no need to change path for the next code
        #delete this file from specified folder if you are not running it for the first time
        c=open('singles.txt','a+')

        list_of_values1=([n for n in range(len(text)) if text.find(':', n) == n])
        list_of_values1.append(len(text)+1)
        list_of_values2=([n for n in range(len(text)) if text.find('\n', n) == n])
        list_of_values2.append(len(text)+1)
        # sentences = nltk.sent_tokenize(text[(list_of_values1[i]):(list_of_values2[i])])
        start=0
        for i in range(len(list_of_values2)):
            if i==(len(list_of_values2)-4):
                c.writelines(text[list_of_values2[i-1]:])
                break
            else:
                if len(text[(list_of_values1[i]):(list_of_values2[i])])>300:
                    # single_text=summarize(text[(list_of_values1[i]):(list_of_values2[i])],ratio=0.4)
                    single_text = summary.TextRank().summary(text[(list_of_values1[i]):(list_of_values2[i])])
                    c.writelines(text[(start):(list_of_values1[i])])
                    c.write('\n'.join('%s' % x for x in single_text))
                    # c.writelines(text[(start):(list_of_values1[i])]+": "+str(single_text)+"\n")
                    start=list_of_values2[i]
                else:
                    single_text=(text[(list_of_values1[i]):(list_of_values2[i])])
                    print(text[(list_of_values1[i]):(list_of_values2[i])])
                    c.writelines(text[(start):(list_of_values1[i])]+single_text +"\n")
                    start=list_of_values2[i]
        c.close()
        b=open('singles.txt','r')
        modified_text=b.read()
        ratio=0.5
        # sum=(summarize(modified_text,ratio=ratio))
        sum = summary.TextRank().summary(modified_text)
        return sum 
    # summary multil files
    def test(self):
        list_folder = ['article']
        result = 'result'
        for folder in list_folder:
            path =  folder+'/*.txt'
            list_of_files = glob.glob(path)

            for file_name in list_of_files:
                print(file_name)
                f = open(file_name, 'r')
                sum = Summary().SummaryConv(file_name)
                # f = open(os.path.join( result+'/',
                # os.path.basename(file_name)) , 'w')
                # f.write(sum)
                with open(os.path.join( result+'/', os.path.basename(file_name)), 'w') as f:
                    f.write('\n'.join('%s' % x for x in sum))
                f.close()
                os.remove('singles.txt')
    # summary 1 file
    def summary3(self):
        file_name = input("Enter the path of your file: ")
        assert os.path.exists(file_name), "I did not find the file at, "+str(file_name)

        f = open(file_name, 'r')
        sum = Summary().SummaryConv(file_name)
        with open("result.txt", 'w')  as f:
            f.write('\n'.join('%s' % x for x in sum))
        f.close()
        os.remove('singles.txt')

if __name__ == '__main__':
    # Summary().test()
    try:
        Summary().summary3()
    except: 
        print('There was a small error, check again')


