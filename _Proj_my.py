import nltk
import unicodedata	#For making unicode table of punctuations for translate function in preprocess
import sys			#Ditto unicodedata

#--Global Vars-------------------------------------------------------------------------------
positive_words=['good' ,'great' ,'nice', 'super', 'fun', 'delightful', 'like','best','awesome']
negative_words=['awful','lame','horrible','bad','worse']
score=0;
#--Functions---------------------------------------------------------------------------------
def printTokentype(str,type,tagged):
	global score							#Required to access global score , else local var is created since score is being modified.
	print(str)
	for i in tagged:
		if(i[1] == type):					#Print by type
			if i[0] in positive_words:
				score=score+1
				print("+ ",end="")
			elif i[0] in negative_words:
				score=score-1
				print("- ",end="")
			print(i[0])
def preprocess(sentence):
	print("Preprocessing...")
	#Change Sentence to lower case
	sentence=sentence.lower()
	
	#Remove punctuations 
	#translation table
	tbl = dict.fromkeys(i for i in range(sys.maxunicode) 
							if unicodedata.category(chr(i)).startswith('P'))
	sentence=sentence.translate(tbl)		#More info on : help(str.translate)
	
	print(sentence)
	return sentence	
def token_tag(sentence):
	#Tokenize
	tokens = nltk.word_tokenize(sentence)
	#Assign pos tags
	print("\nTokenized and tagged: \n")
	tagged = nltk.pos_tag(tokens)
	print(tagged[0:len(tagged)])
	return tagged		
#--MAIN-------------------------------------------------------------------------------------

ORIGINAL = """This is a good movie. This is not bad. This is too great and awesome. Worse. best."""
sentence=ORIGINAL
print("\n Sentence is:\n")
print(sentence)

sentence=preprocess(sentence)
tagged=token_tag(sentence)

printTokentype("\nAbsolute adjective :",'JJ',tagged)
printTokentype("\nComparative adjective :",'JJR',tagged)
printTokentype("\nSuperlative adjective :",'JJS',tagged)

print("\nScore is")
print(score)
if(score > 0):
	print("Positive Review")
elif(score < 0):
	print("Negative Review")
else:
	print("Neutral/Can not be determined")