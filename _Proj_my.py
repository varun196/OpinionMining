from __future__ import print_function
import nltk

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
	pos_words=pos_words.split('\n')			#split words from new line
	neg_words=neg_words.split('\n')

def prompt():					#Ask Review
	#ORIGINAL = """This is a good movie. This is not bad. This is too great and awesome. Worse. 	best."""
	#print("\nSentence is:")
	#print(ORIGINAL)
	print("Enter A review :")
	ORIGINAL=input()
	return ORIGINAL

#--Class ---------------------------------------------------------------
class ProcessReview:
	#--Variables -------------------------------------------------------
	score=0
	debug=0
	global noun_dict
	noun_dict={"":0}
	enhancers_1 = ['generally','usually']
	enhancers_2 = ['very','too','always','primarily']
	diminishers = ['moderately','averagely']
	inverter	= ['not']
	inverter_2	= ['never']

	useful = ['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ','NN']

	#--Functions --------------------------------------------------------
	
	def preprocess(self,sentence):
		self.my_print("Preprocessing...")
		#Change Sentence to lower case
		sentence=sentence.lower()
		return sentence	

	def removeStops(self,tag):
		
		for i in tag :
			if i[1] not in self.useful:
				tag.remove(i)
		
	def my_print(self,x,NewLine=1,sign=0):
		if(debug == '1'):
			if(sign == 1):
				print('+  ',end='')
			elif(sign==-1):
				print('-  ',end='')
			if(NewLine == 1):
				print(x)
			else:
				print(x,end='')	

	def findSign(self,x):
		if(x>0):
			return 1
		elif(x<0):
			return -1
		else:
			return 0
	
	def scoreSent(self,sent):			#operate Sentence wise
		modifier=0;
		multiplier=1;
		sent=nltk.word_tokenize(sent)
		tagged=nltk.pos_tag(sent)
	
		self.my_print(tagged)
	
		self.my_print("Removed other words")		#Must do after tagging
		self.removeStops(tagged)			#here cause sentences need to be tagged.
		self.my_print(tagged)
	
		global score
		noun_present_flag=0
		init_score=self.score
	
		for i in tagged :
			if i[1] in 'NN':
				noun=i[0]
				noun_present_flag=1
				self.my_print("     ",0)
			elif i[0] in self.inverter:
				self.my_print("*    ",0)
				multiplier=-1;
			elif i[0] in self.inverter_2:
				self.my_print("*    ",0)
				multiplier=-1;
				modifier=2;
			elif i[0] in pos_words:
				self.score=self.score+((2+modifier)*multiplier)
				self.my_print(2+modifier,0,self.findSign((2+modifier)*multiplier))
				self.my_print(" ",0)
				modifier=0
				multiplier=1
			elif i[0] in neg_words:
				self.score=(self.score+(-2-modifier)*multiplier)
				self.my_print(abs(-2-modifier),0,self.findSign((-2-modifier)*multiplier))
				self.my_print(" ",0)
				modifier=0
				multiplier=1
			elif i[0] in self.enhancers_1:
				modifier=1
				self.my_print("1    ",0)
			elif i[0] in self.enhancers_2:
				modifier=2
				self.my_print("2    ",0)
			else:
				self.my_print("     ",0)
			self.my_print(i[0])
		
			global noun_dict
			if(noun_present_flag==1):
				if((noun in noun_dict) == False):
					noun_dict[noun]=(self.score-init_score)	#Add new key-value pair to dict
				else:
					noun_dict[noun]+=(self.score-init_score)	#Modify value of pair to dict
			
	def printAnswer(self,sc):
		self.my_print("Score :",0)
		self.my_print(sc)
	
		if(self.score > 0):
			print("Positive Review")
		elif(self.score < 0):
			print("Negative Review")
		else:
			print("Neutral/Can not be determined")

	def print_dict(self,x):
		for i in x.keys():
			if(i==""):
				continue
			print(i+" : ",end='')
			if(x[i] > 0):
				print("Positive Review")
			elif(x[i] < 0):
				print("Negative Review")
			else:
				print("Neutral/Can not be determined")

	def getSentiment(self,review):
		
		review=self.preprocess(review)
		sentences=review.split('.')			#Split to sentences
		for sent in sentences :				#Score Each sentence.
			self.scoreSent(sent)
		
		#self.printAnswer(self.score)
		self.my_print("\n")

		#self.print_dict(noun_dict)
		#print(noun_dict)
		
		return {"OverallScore":self.score , "NounScore":noun_dict}	#return dictionary
		
#--Main---------------------------------------------------------------

init()
review=prompt()
pro = ProcessReview()							#Create Object
result=pro.getSentiment(review)	

print("\n\n\nInMain")
print(result["OverallScore"])
print(result["NounScore"])
