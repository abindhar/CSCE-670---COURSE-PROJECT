
# Program substituting itself to the scoring program to test python configuration
# Isabelle Guyon, ChaLearn, September 2014
# Updated for queryful searches only - Abindu
import json
from numpy import genfromtxt, log, log2
score_file = open('scores.txt', 'w')
solution_name = 'valid.solution.csv'
#submission_name = 'basicfeaturesonly.txt'
submission_name = 'GraphEmbedding100.txt'
with open(solution_name, 'r') as real_answer, \
    open(submission_name, 'r') as submission:
		answer_lines, sub_lines = iter(real_answer), iter(submission)
		current_ans = next(answer_lines)  # skip column names
		# Setting up NDCG sum variables and counters
		NDCG_search = 0.0
		NDCG_category = 0.0
		counter_search = 0.0
		counter_category = 0.0
		current_search = True
		skipped_lines = 0
        #print('Hello')
		while True:
			try:
				current_ans = next(answer_lines)
				current_sub = next(sub_lines)
				current_ans_split = current_ans.split(';')
				current_sub_split = current_sub.split(' ')

				# print(current_ans_split[1])
				# query id dont match
				while current_ans_split[1] != current_sub_split[0]:

					if int(current_ans_split[1]) < int(current_sub_split[0]):
						#print("Missing query: ", current_sub_split[1])
						#raise Exception()
						current_ans = next(answer_lines)
					else:
						skipped_lines += 1
						# print("Extra query: ", current_ans_split[1])
						#raise Exception()
						current_sub = next(sub_lines)
					# current_ans_split = current_ans.split(';')
					current_sub_split = current_sub.split(' ')
				# Increase counters
                #If is search is true
				current_search = (current_ans_split[3] == "TRUE")
				if current_search:
					counter_search += 1
				else:
					#ignore for now, can use later
					counter_category += 1

			except StopIteration:
				answer = next(answer_lines, None)
				if answer is not None:
					print("Submission file not complete!")
					raise Exception()
				break
			scores_raw_string = current_ans_split[4].replace('""', '"')
			if scores_raw_string[-1] == '\n':
				scores_raw_string = scores_raw_string[:-1]
			scores_raw_string = scores_raw_string[1:-1]  # remove quotes
			ans_json = json.loads(scores_raw_string)
            #sub items = all docs returned per query
			sub_items = current_sub_split[1].replace("\n", "").split(',')
			dcg = 0.
			counted_items = {}
			for i, sub_item in enumerate(sub_items):
				if sub_item not in counted_items:
					counted_items[sub_item] = True # count only first entry of item per query in submission
					dcg += ((2. ** ans_json.get(sub_item, 0)) - 1.) / log2(i + 2.)

			idcg_raw = current_ans_split[5].replace(',', '.')
			idcg = float(idcg_raw)

			if current_search:
                #if is.search=True
				NDCG_search += dcg / idcg
			else:
                #if is.search=False
				#basically ignore the below
				NDCG_category += dcg / idcg
        #Mean of NDCG across
		NDCG_search = NDCG_search / counter_search
		#NDCG_category = NDCG_category / counter_category
			#NDCG_total = NDCG_category * 0.8 + NDCG_search * 0.2
            #NDCG_total = NDCG_search
		score_file.write("Average Search_NDCG: %0.6f\n" % NDCG_search)
			#score_file.write("category_NDCG: %0.6f\n" % NDCG_category)
			#score_file.write("avg_NDCG: %0.6f\n" % NDCG_total)
			   
		score_file.close()
		exit(0)

