__author__ = 'orps'

class Nonterminal:
	def __init__(self, char, startSymbol='', alternate = False):
		self.char = char
		self.start = startSymbol == char
		self.rules = []
		if alternate == False:
			self.alternate = Nonterminal('~' + char, '~'+startSymbol, True)
		else:
			self.alternate = None


	def addRule(self, rule):
		self.rules.append(rule)
		if self.alternate is not None and False == rule.isLambda():
			rule.copy(self.alternate)

	def delRule(self, rule):
		if rule in self.rules:
			self.rules.remove(rule)
		if self.alternate is not None:
			self.alternate.delRule(rule)

	def isTerminal(self):
		return False

	def isNullable(self):
		for rule in self.rules:
			if rule.isLambda():
				return True
		return False

	def nullable(self):
		if self.isNullable():
			return self.alternate
		return self

	def isStart(self):
		return self.start

	def nonnullOperate(self):
		for rule in self.rules:
			rule.nonnullOperate(self)

	def __repr__(self):
		return self.char

	def printRules(self):
		result = []

		#if self.start and self.alternate is not None:
		#	return self.nullable().printRules()

		for rule in self.rules:
			if rule.isLambda() and self.start:
				continue
			result.append("{0}->{1}".format(self, rule))

		if self.isNullable() and self.start == False:
			result.extend(self.nullable().printRules())

		return result

class Terminal:
	def __init__(self, char):
		self.char = char

	def isTerminal(self):
		return True

	def isStart(self):
		return False

	def isNullable(self):
		return self.char == 'e'

	def __repr__(self):
		return self.char


class Grammatic:
	def __init__(self, nonts, ts):
		self.nonts = nonts
		self.ts = nonts

	def getToken(self, char):
		if char in self.nonts:
			return self.nonts[char]
		else:
			return self.ts[char]

	def nonnullOperate(self):
		for key in self.nonts.keys():
			self.nonts[key].nonnullOperate()

	def __repr__(self):
		r = ''
		for key in self.nonts.keys():
			for i in self.nonts[key].printRules():
				r = r + str(i) + "\n"
		return r


class Rule:
	def __init__(self, start, eq):
		self.eq = eq
		start.addRule(self)

	def copy(self, newStart):
		return Rule(newStart, self.eq[:])

	def isLambda(self):
		return len(self.eq) == 1 and self.eq[0].isNullable() and self.eq[0].isTerminal()

	def nonnullOperate(self, start):
		for i in range(0, len(self.eq)):
			if self.eq[i].isNullable() and False == self.eq[i].isTerminal():
				start.delRule(self)
				n = self.eq[i].nullable()
				l = [n]
				l.extend(self.eq[i+1:])
				Rule(start, l)
			else:
				if i == 0:
					return
				Rule(start, self.eq[i:])
				break

	def __eq__(self, other):
		if len(self.eq) != len(other.eq):
			return  False

		for i in range(0, len(self.eq)):
			if self.eq != other.eq:
				return False

		return True

	def __repr__(self):
		return reduce(lambda x, y: '{0} {1}'.format(x, y), self.eq, '')


def readGrammatic():
	start = 'S'

	nts = {
		'S': Nonterminal('S', start),
		'A': Nonterminal('A', start),
		'B': Nonterminal('B', start)
	}

	ts = {
		'a': Terminal('a'),
		'b': Terminal('b'),
		'e': Terminal('e')
	}

	s = nts.copy()
	s.update(ts)

	g = Grammatic(nts, ts)

	rules = [
		Rule(s['S'], [s['A'], s['B']]),
		Rule(s['A'], [s['a'], s['A']]),
		Rule(s['B'], [s['b'], s['A']]),
		Rule(s['A'], [s['e']]),
		Rule(s['B'], [s['e']]),
	]

	return g

g = readGrammatic()
g.nonnullOperate()

print str(g)
