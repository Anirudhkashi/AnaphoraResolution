import os
import stanford
from nltk.tree import *
import ast
import nltk
import re

def findPRPs(node):
	l= []

	if(type(node)== nltk.tree.ParentedTree):
		if(re.search("PRP.*", node.label())):
			l.append(node)

		else:
			for j in node:
				l.extend(findPRPs(j))

	return l


def getDominatingNP(node):

	global history
	history.append(node)

	if(node.label() == "NP" or node.label() == "S"):
		return node
	else:
		return getDominatingNP(node.parent())


def getLeaves(node):
	return " ".join(node.leaves())


def findNP(node, nonnode):

	l= []
	if(type(node)== nltk.tree.ParentedTree):
		if(re.search("NP", node.label()) and node not in nonnode):
			l.append(" ".join(node.leaves()))

		elif(node not in nonnode):
			for j in node:
				l.extend(findNP(j, nonnode))

	return l


def bfs(node, nonnode):

	nodes= []

	if(type(node)== nltk.tree.ParentedTree):
		if(re.search("S", node.label()) and node not in nonnode):
			nodes+= findNP(node, nonnode)

		elif(re.search("NP", node.label())):
			nodes+= findNP(node, nonnode)

	return nodes


def getNPProposals(X):
	Xnodes = []
	NPS = []
	for Xnode in X:
		if(Xnode.label() == "NP" or Xnode.label() =="S"):
			Xnodes.append(Xnode)
	for xn in range(len(Xnodes)):
		res= bfs(Xnodes[xn], history)
		if(res):
			NPS.append(res)
	return NPS


os.environ['STANFORD_PARSER'] = '/home/anirudh/jars'
os.environ['STANFORD_MODELS'] = '/home/anirudh/jars'

parser = stanford.StanfordParser(model_path="/home/anirudh/englishPCFG.ser.gz")
fp= open("dataset.txt", "r").read().strip()
sentences= parser.raw_parse_sents(nltk.sent_tokenize(fp))

history= []
for line in sentences:
	count= -1
	for num in line:

		count+= 1
		sentence = num
		sentence= Tree("root", sentence)
		sentence= sentence[0]
		sentence= ParentedTree.convert(sentence)
		l= findPRPs(sentence)
		
		for i in l:

			history= []
			PRPparent =  getDominatingNP(i.parent())
			X = getDominatingNP(PRPparent.parent())
			NPS= getNPProposals(X)
			
			c= count-1
			if(NPS== []):
				while(NPS== [] and c>= 0):
					tmp= Tree("root", num)
					tmp= tmp[0]
					tmp= ParentedTree.convert(tmp)
					NPS= getNPProposals(tmp)
					c-= 1

			print NPS, i