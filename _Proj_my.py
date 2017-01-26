from __future__ import print_function
import nltk
import unicodedata	#For making unicode table of punctuations for translate function in preprocess
import sys			#Ditto unicodedata

#--Global Vars-------------------------------------------------------------------------------
score=0
pos_words=''
neg_words=''
#--Functions---------------------------------------------------------------------------------
def my_print(x,NewLine=1):
	if(debug == '1'):
		if(NewLine == 1):
			print(x)
		else:
			print(x,end='')	
def init():
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
def prompt():
	#ORIGINAL = """This is a good movie. This is not bad. This is too great and awesome. Worse. best."""
	#print("\nSentence is:")
	#print(sentence)
	print("Enter A review :")
	ORIGINAL=input()
	return ORIGINAL
def getScore():
	global score
	for i in tagged : 
		if i[0] in pos_words:
			score=score+1
			my_print("+ ",0)
		elif i[0] in neg_words:
				score=score-1
				my_print("- ",0)
		my_print(i[0])
def printTokenScore(str,type,tagged):		#also calculates score
	global score							#Required to access global score , else local var is created since score is being modified.
	my_print(str)
	for i in tagged:
		if(i[1] == type):					#my_print by type
			if i[0] in pos_words:
				score=score+1
				my_print("+ ",0)
			elif i[0] in neg_words:
				score=score-1
				my_print("- ",0)
			my_print(i[0])
def preprocess(sentence):
	my_print("Preprocessing...")
	#Change Sentence to lower case
	sentence=sentence.lower()
	
	#Remove punctuations 
	#translation table
	tbl = dict.fromkeys(i for i in range(sys.maxunicode) 
							if unicodedata.category(chr(i)).startswith('P'))
	sentence=sentence.translate(tbl)		#More info on : help(str.translate)
	
	my_print(sentence)
	return sentence	
def token_tag(sentence):
	#Tokenize
	tokens = nltk.word_tokenize(sentence)
	#Assign pos tags
	my_print("\nTokenized and tagged: \n")
	tagged = nltk.pos_tag(tokens)
	my_print(tagged[0:len(tagged)])
	return tagged		

#--MAIN-------------------------------------------------------------------------------------
init()
ORIGINAL=prompt()
sentence=ORIGINAL


sentence=preprocess(sentence)
tagged=token_tag(sentence)
getScore()

#printTokenScore("\nAbsolute adjective :",'JJ',tagged)
#printTokenScore("\nComparative adjective :",'JJR',tagged)
#printTokenScore("\nSuperlative adjective :",'JJS',tagged)

my_print("\nScore is")
my_print(score)
if(score > 0):
	print("Positive Review")
elif(score < 0):
	print("Negative Review")
else:
	print("Neutral/Can not be determined")
