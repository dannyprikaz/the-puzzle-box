from random import randint
import os
from sys import exit
clear = lambda: os.system('cls')

class WorkTable(object):
	def __init__(self):
		self.my_grid = OffGrid()
		self.target = TargetGrid()
		self.switch_one = False
		self.switch_two = False
		self.switch_states = {False: "Off", True: "On"}
		self.ColorLocks = []
		self.same = False
		for i in range(4):
			self.ColorLocks.append(ColorLock())
	
	def __str__(self):
		print_out = "\nThe box's Grid looks like this:\n"
		print_out += self.my_grid.__str__() + "\n\n"
		
		print_out += "Your Grandfather's key looks like this:\n"
		print_out += self.target.__str__() + "\n\n"
		
		print_out += "Switch 1 is %s.\n" % self.switch_states[self.switch_one]
		print_out += "Switch 2 is %s.\n\n" % self.switch_states[self.switch_two]
		
		print_out += "You can lock the color into four of the squares:\n"
		for i in range(4):
			print_out += ('\t%d: ' % (i + 1)) + self.ColorLocks[i].__str__()
			print_out += "\n"
		
		return print_out
	
	def check_switches(self):
		if not(self.switch_one) and not(self.switch_two):
			return OffGrid()
		elif self.switch_one and not(self.switch_two):
			return RedGrid()
		elif self.switch_one and self.switch_two:
			return GreenGrid()
		elif not(self.switch_one) and self.switch_two:
			return BlueGrid()
		else:
			self.switch_one = False
			self.switch_two = False
			return OffGrid()
			
	
	
	def refresh(self):
		self.my_grid = self.check_switches()
		for lock in self.ColorLocks:
			index, color, is_on = lock.contents()
			if is_on:
				self.my_grid.boxes[index] = color
		if self.my_grid.boxes == self.target.boxes:
			self.same = True
	

class ColorLock(object):
	def __init__(self):
		self.index = 0
		self.color = 'O'
		self.is_on = False
	
	def __str__(self):
		if not(self.is_on):
			return "Unlocked"
		else:
			return self.color + " is locked in box %d" % (self.index + 1)
		
	def activate(self, index, Grid):
		self.index = index
		self.color = Grid.boxes[index]
		self.is_on = True
		
	def deactivate(self):
		self.is_on = False
	
	def contents(self):
		return self.index, self.color, self.is_on
		

class Grid(object):
	def __init__(self):
		self.colors = ['R', 'G', 'B', 'O']
		self.modulus = 3
		self.boxes = list()
		for i in range(9):
			self.boxes.append('')
	
	def __str__(self):
		print_out = ''
		for i in range(3):
			print_out += '\t --- --- --- \n'
			num = i * 3
			print_out += '\t| %s | %s | %s |\n' % (self.boxes[num],
												 self.boxes[num + 1],
												 self.boxes[num + 2])
		print_out += '\t --- --- --- '
		return print_out
		
	def set_color(self):
		if self.modulus == 3:
			for i in range(9):
				self.boxes[i] = self.colors[self.modulus]
		else:
			for i in range(9):
				self.boxes[i] = self.colors[(i + self.modulus) % 3]
				if i % 3 == 2:
					self.modulus += 2

class OffGrid(Grid):
	def __init__(self):
		super(OffGrid, self).__init__()
		self.set_color()

class RedGrid(Grid):
	def __init__(self):
		super(RedGrid, self).__init__()
		self.modulus = 0
		self.set_color()

class GreenGrid(Grid):
	def __init__(self):
		super(GreenGrid, self).__init__()
		self.modulus = 1
		self.set_color()

class BlueGrid(Grid):
	def __init__(self):
		super(BlueGrid, self).__init__()
		self.modulus = 2
		self.set_color()

class TargetGrid(Grid):
	def create_variances(self):
		self.variances = []
		for i in range(4):
			variance = randint(0, 8)
			while variance in self.variances:
				variance = randint(0, 8)
			self.variances.append(variance)
		for variance in self.variances:
			pick_color = randint(0, 3)
			while self.colors[pick_color] == self.boxes[variance]:
				pick_color = randint(0, 3)
			self.boxes[variance] = self.colors[pick_color]

	def __init__(self):
		super(TargetGrid, self).__init__()
		self.modulus = randint(0, 3)
		self.set_color()
		self.create_variances()

class GameEngine(object):
	def __init__(self):
		self.table = WorkTable()
		self.start()
		
	def start(self):
		clear()
		print "\nYou pull the puzzle box down from its shelf."
		print "Your Grandfather gave it to you just before he died."
		print "He handed it to you and said,"
		print "\n\t'Inside this box, there is something I want you to have.'\n"
		print "He passed away later that day."
		print "\n[PRESS ENTER TO CONTINUE]"
		raw_input()
		print "\nYou've fiddled with the box from time to time,"
		print "but you've never solved it."
		print "It has a 3 x 3 Grid on the front of it."
		print "Each square can either be Off, Red, Green, or Blue."
		print "Two switches control the patterns of colors that appear on the Grid."
		print "You've also figured out that you can lock a color in place by pressing down on it,"
		print "but you can only lock four colors in place at a time."
		print "Pressing any of those locked squares again unlocks them."
		print "\n[PRESS ENTER TO CONTINUE]"
		raw_input()
		print "\nEarlier today, you were looking through your grandfather's study."
		print "In a drawer of his desk, you found a piece of paper."
		print "It seems to have a key to the puzzle on it."
		print "You sit on the floor with the box on your lap."
		print "You wonder what it might contain."
		print "\nAre you ready to solve the puzzle?"
		print "\n[PRESS ENTER TO CONTINUE]"
		raw_input()
		
		self.play()
		
	def victory(self):
		clear()
		print '\nInside you find a note.  It reads:\n'
		print '\t"Persistance is the key that opens any lock.'
		print '\t"Love, Grandpa"'
		print '\nYour eyes begin to water.'
		print '\nYou turn the paper over in your hands.'
		print "There's writing on the other side..."
		print "\n[PRESS ENTER TO CONTINUE]"
		raw_input()
		print"P.S. I don't mean that in a rape-culture-y way.\n"
		
		exit(1)
		
		
	
	def play(self):
		try:
			while not(self.table.same):
				self.table.refresh()
				clear()
				print self.table
				if self.table.same:
					print "You hear a loud click as the box comes unlocked."
					print "You open the box..."
				else:
					print "You can flip a switch or toggle a lock."
					print "Switch or Lock?"
					choice = raw_input('> ')
				
					if choice == "Switch":
						self.switch()
					elif choice == "Lock":
						self.lock()
					else:
						self.play()
		except (EOFError, KeyboardInterrupt):
			smooth_exit()

		print "\n[PRESS ENTER TO CONTINUE]"
		raw_input()

		self.victory()
		
	def switch(self):
		print "Flip which switch?"
		print "1 or 2? (0 to go back)"
		choice = raw_input("> ")
		if choice == '1':
			self.table.switch_one = not(self.table.switch_one)
		elif choice == '2':
			self.table.switch_two = not(self.table.switch_two)
		elif choice == '0':
			pass
		else:
			self.switch()
	
	def lock(self):
		print "Toggle which lock?"
		print "1, 2, 3, or 4? (0 to go back)"
		choice = raw_input("> ")
		if choice == '0':
			pass
		elif choice in ['1', '2', '3', '4']:
			if self.table.ColorLocks[int(choice) - 1].is_on:
				self.table.ColorLocks[int(choice) - 1].deactivate()
			else:
				self.the_lock(int(choice))
		else:
			self.lock()
	
	def the_lock(self, index):
		print "Lock which square? (1-9)(0 to go back)"
		print "The squares are ordered left to right then top to bottom."
		choice = raw_input("> ")
		if choice == '0':
			pass
		elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
			self.table.ColorLocks[index - 1].activate(int(choice) - 1, self.table.my_grid)
		else:
			self.the_lock(index)
		
def smooth_exit():
	try:
		print "\nYou decide to come back to the puzzle later.\n\t Sorry, Grandpa."
		exit(0)
	except KeyboardInterrupt:
		exit(0)
		

if __name__ == "__main__":
	clear()
	game = GameEngine()
