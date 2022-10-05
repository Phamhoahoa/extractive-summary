from pyrouge import Rouge155
# import settings

r = Rouge155()
# r =pi Rouge155('/absolute/path/to/ROUGE-1.5.5/directory')


path_textrank = "system/"
path_Kmeans = "system_Kmeans/"
class Test_sum(object):
    def validate_sum(self, path_system):
        list_folder = [ 'KHGD', 'KT', 'XH', 'khcn', 'CT', 'VH' ]
        sum_rouge_1_f = 0.
        sum_rouge_2_f = 0.
        sum_rouge_l_f = 0.
        sum_rouge_2_precision = 0.
        for name_folder in list_folder:
            print(name_folder)
            print('-------------------------------------------------------------------')
            r.system_dir = path_system + name_folder
            r.model_dir = 'model/' + name_folder

            # define the patterns
            r.system_filename_pattern = name_folder +'(\d+).txt'

            r.model_filename_pattern = name_folder +'#ID#.txt'  

            # use default parameters to run the evaluation
            output = r.convert_and_evaluate(split_sentences=True)

            output_dict = r.output_to_dict(output)
            print('rouge_1_recall = %s'%output_dict['rouge_1_recall'])
            print('rouge_1_precision = %s'%output_dict['rouge_1_precision'])
            print('rouge_1_f = %s'%output_dict['rouge_1_f_score'])
            sum_rouge_1_f += output_dict['rouge_1_f_score']

            print()
            print('rouge_2_recall = %s'%output_dict['rouge_2_recall'])
            print('rouge_2_precision = %s'%output_dict['rouge_2_precision'])
            print('rouge_2_f = %s'%output_dict['rouge_2_f_score'])
            sum_rouge_2_f += output_dict['rouge_2_f_score']
            sum_rouge_2_precision += output_dict['rouge_2_precision']

            print()
            print('rouge_l_recall = %s'%output_dict['rouge_l_recall'])
            print('rouge_l_precision = %s'%output_dict['rouge_l_precision'])
            print('rouge_l_f = %s'%output_dict['rouge_l_f_score'])
            sum_rouge_l_f += output_dict['rouge_l_f_score']
        sum_rouge_1 = sum_rouge_1_f / len(list_folder)
        sum_rouge_2 = sum_rouge_2_f / len(list_folder)
        sum_rouge_l = sum_rouge_l_f / len(list_folder)
        sum_2_precision = sum_rouge_2_precision / len(list_folder)
        print(sum_rouge_1,sum_rouge_2,sum_rouge_l,sum_2_precision)
        return sum_rouge_1, sum_rouge_2, sum_rouge_l

    def main(self):
        Test_sum().validate_sum(path_textrank)
        # Test_sum().validate_sum(path_Kmeans)
if __name__ == '__main__':
    Test_sum().main()