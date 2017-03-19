# CREDITS TO SHABDA RAJ
# http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
end_chars = ["!", ".", "?", "..."]
end_words = ["SAD!", "Sad!", "sad!", "DISGRACE!", "AGAIN!", "AGAIN", "BAD!", "bad!"]


import random
import json

class Markov:
	def __init__(self, file):
		self.cache = {}
		self.file = open(file)
		self.file.seek(0)
		self.data = self.file.read()
		self.file.seek(0)
		self.data = self.file.read()
		self.words = self.data.split()
		self.genTriplets()

	def genTriplets(self):
		for i in range (len(self.words) - 2):
			w1, w2, w3 = self.words[i], self.words[i+1], self.words[i+2]
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def genTweet(self):
		start_word = " "
		while True:
			start = random.randint(1, (len(self.words) - 3))
			prev_word = self.words[start - 1]
			start_word = self.words[start]
			next_word = self.words[start + 1]
			if (start_word[0].isupper() or start_word[0] == "\"") and (prev_word[-1] in end_chars):
				break
		w1 = start_word
		w2 = next_word
		gen_words = []
		while True:
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1,w2)])
			if (w2[-1] in end_chars and len(gen_words) > 10) or w2 in end_words:
				break
		gen_words.append(w2)
		return ' '.join(gen_words)
