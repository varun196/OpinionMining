from __future__ import print_function
import nltk
import unicodedata	#For making unicode table of punctuations for translate function in preprocess
import sys			#Ditto unicodedata

#--Global------------------------------
score=0
debug=0
enhancers_1 = ['generally','usually']
enhancers_2 = ['never','very','too','always','primarily']
diminishers = ['moderately','averagely']
inverter	= ['not']
#--Functions---------------------------------------------------------
def preprocess(sentence):
	my_print("Preprocessing...")
	#Change Sentence to lower case
	sentence=sentence.lower()
	return sentence	
def my_print(x,NewLine=1,sign=0):
	if(debug == '1'):
		if(sign == 1):
			print('+  ',end='')
		elif(sign==-1):
			print('-  ',end='')
		if(NewLine == 1):
			print(x)
		else:
			print(x,end='')	
def init():						#Bring in lists , Ask for debug
	global pos_words
	global neg_words
	try:
		pos_words=open("positive.txt").read()
	except:
		print("Positive Database not present")
		sys.exit()
	try:
		neg_words=open("negative.txt").read()
	except:
		print("Negative Database not present")
		sys.exit()
	
	global debug
	
	while(True):
		print("Debug? [1/0]:")
		debug=input()
		if(debug=='1' or debug=='0'):
			break
	pos_words=pos_words.split('\n')
	neg_words=neg_words.split('\n')
	
def findSign(x):
	if(x>0):
		return 1
	elif(x<0):
		return -1
	else:
		return 0
	
def prompt():					#Ask Review
	#ORIGINAL = """This is a good movie. This is not bad. This is too great and awesome. Worse. best."""
	#print("\nSentence is:")
	#print(ORIGINAL)
	print("Enter A review :")
	ORIGINAL=input()
	return ORIGINAL
def scoreSent(sent):			#operate Sentence wise
	modifier=0;
	multiplier=1;
	sent=nltk.word_tokenize(sent)
	tagged=nltk.pos_tag(sent)
	
	my_print(tagged,0)
	
	global score
	for i in tagged :
		if i[0] in inverter:
			my_print("*    ",0)
			multiplier=-1;
		elif i[0] in pos_words:
			score=score+((2+modifier)*multiplier)
			my_print(2+modifier,0,findSign((2+modifier)*multiplier))
			my_print(" ",0)
			modifier=0
			multiplier=1
		elif i[0] in neg_words:
			score=(score+(-2-modifier)*multiplier)
			my_print(abs(-2-modifier),0,findSign((-2-modifier)*multiplier))
			my_print(" ",0)
			modifier=0
			multiplier=1
		elif i[0] in enhancers_1:
			modifier=1
			my_print("1    ",0)
		elif i[0] in enhancers_2:
			modifier=2
			my_print("2    ",0)
		else:
			my_print("     ",0)
		my_print(i[0])
def printAnswer():
	my_print("Score :")
	my_print(score)

	if(score > 0):
		print("Positive Review")
	elif(score < 0):
		print("Negative Review")
	else:
		print("Neutral/Can not be determined")

#--Main---------------------------------------------------------------

init()
ORIGINAL=prompt()
review=ORIGINAL

review=preprocess(review)
sentences=review.split('.')
for sent in sentences :		#Score Each sentence.
	scoreSent(sent)
	
printAnswer()