
# from bleu.bleu import Bleu
from nltk.translate.bleu_score import sentence_bleu
from nltk import sent_tokenize, word_tokenize, PorterStemmer

import glob




def test_blue(self, text, summary_text):
 
    
    text =  word_tokenize(text)
    reference = [text]
    summary_text = word_tokenize(summary_text)
    candidate = summary_text
    print('Individual 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
    print('Individual 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 1, 0, 0)))
    print('Individual 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 1, 0)))
    print('Individual 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 0, 1)))
    score = sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25))
    print(score)



if __name__ == '__main__':
    # Feed in the directory where the hypothesis summary and true summary is stored
    system_file = glob.glob('system/CT/*.txt')
    model_file = glob.glob('model/CT/*.txt')

    BLEU_1 = 0.
    BLEU_2 = 0.
    BLEU_3 = 0.
    BLEU_4 = 0.
    BLEU = 0.
    num_files = 0
    for reference_file, hypothesis_file in zip(model_file, system_file):
        num_files += 1
        print(reference_file, hypothesis_file)

        with open(reference_file, 'r', errors='ignore') as rf:
            reference = rf.read()

        with open(hypothesis_file,'r', errors='ignore' ) as hf:
            hypothesis = hf.read()

        print(reference)
        print("-------------------------------------------------------------")
        print(hypothesis)

        # ref, hypo = load_textfiles(reference, hypothesis)

        reference =  word_tokenize(reference)
        ref = [reference]
        summary_text = word_tokenize(hypothesis)
        hypo = summary_text
        print('******************************************************************')
        
        print('Individual 1-gram: %f' % sentence_bleu(ref, hypo, weights=(1, 0, 0, 0)))
        print('Individual 2-gram: %f' % sentence_bleu(ref, hypo, weights=(0, 1, 0, 0)))
        print('Individual 3-gram: %f' % sentence_bleu(ref, hypo, weights=(0, 0, 1, 0)))
        print('Individual 4-gram: %f' % sentence_bleu(ref, hypo, weights=(0, 0, 0, 1)))
        score = sentence_bleu(ref, hypo, weights=(0.25, 0.25, 0.25, 0.25))
        BLEU_1 += sentence_bleu(ref, hypo, weights=(1, 0, 0, 0))
        BLEU_2 += sentence_bleu(ref, hypo, weights=(0, 1, 0, 0))
        BLEU_3 += sentence_bleu(ref, hypo, weights=(0, 0, 1, 0))
        BLEU_4 += sentence_bleu(ref, hypo, weights=(0, 0, 0, 1))
        BLEU  += sentence_bleu(ref, hypo, weights=(0.25, 0.25, 0.25, 0.25))
        print(score)
    
    avg_BLEU_1 = BLEU_1 / num_files
    avg_BLEU_2 = BLEU_2 / num_files
    avg_BLEU_3 = BLEU_3 / num_files
    avg_BLEU_4 = BLEU_4 / num_files
    avg_BLEU = BLEU / num_files
    print(avg_BLEU_1, avg_BLEU_2, avg_BLEU_3, avg_BLEU_4,avg_BLEU)


    