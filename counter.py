import tkinter as tk
import os.path

#ERROR MESSAGES
ERROR_NO_GAME_NAME = "Please enter a game name"
ERROR_ENTER_SOMETHING = "Please enter something"
ERROR_GAME_NAME_NOT_CHANGED = "Game name not changed"

#STANDARD MESSAGES
GAME_SELECTED = "Game selected"
SCORE_SEPARATOR = "/"
SCORE_RESET = "Score reset"
GAME_WON_VICTORY = "Victory"
GAME_LOST_DEFEAT = "Defeat"
ENTER_GAME_NAME = "Game name "
SET_GAME = "Set game"
ENTER_PREFIX_TEXT = "Prefix text"
SET_PREFIX_TEXT = "Set prefix text"
PREFIX_TEXT_SET = "Prefix text : "
TEXT_SCORE = "Score"
TEXT_RESTART = "Restart"
TEXT_WIN_BUTTON = "Victory"
TEXT_LOSS_BUTTON = "Defeat"
TEXT_DEBUG_MODE = "Debug mod"
TEXT_DEBUG_MODE_ACTIVATED = "Debug mode activated"
TEXT_DEBUG_MODE_DEACTIVATED = "Debug mode deactivated"
FILE_EXTENSION = ".txt"
TEXT_SCORE_RESET = "Score reset"
TEXT_GAME_SCORE = "Game score : "
TEXT_IS_EMPTY_FILE = " is empty"
TEXT_VOID = ""

#Program specific stuff
gameName = TEXT_VOID
gameText = TEXT_VOID
DEBUG_MODE = False
NB_CHAR = 20
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
WINDOW_NAME = "Game Score Counter"

#Colors
WHITE = "white"

WIN = 1
LOSE = 0

WRITE = "w"
READ = "r"

TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"

def debug(text):
	#Shows the message sent in argument if the counter is in debug mode
	if(DEBUG_MODE == True):
		print(text)

def emptyFile(file):
	#Checks if the fils is empty
	lines = file.read()
	return(lines == "\n" or lines == TEXT_VOID)

def isValidFileName(fileName):
	#Checks if the file name is valid (Windows standard)
	valid = True
	i = 0
	while(i < len(fileName) and valid == True):
		valid = (fileName[i] not in ['/', '\\', '?', '%', '*', ':', '|', "\"", "<", ">"])

	return valid

def isNumber(char):
	#Checks if a char is a number
	return char >= '0' and char <= '9'
	
def changeDebugMode():
	#Switches the debug mode
	global DEBUG_MODE
	DEBUG_MODE = (DEBUG_MODE == False)
	if(DEBUG_MODE):
		print(TEXT_DEBUG_MODE_ACTIVATED)
	else:
		print(TEXT_DEBUG_MODE_DEACTIVATED)

def readNumbers(lineRead):
	#Read all the numbers in a string like this NOTNUMBERnumberNOTNUMBERnumberNOTNUMBERnumber..."
	numbers = []
	number = TEXT_VOID
	end = len(lineRead)
	i = 0
	while(i < end):
		number = TEXT_VOID
		if(not isNumber(lineRead[i])): #Get the NOTNUMBER
			i += 1
		else:
			for j in range(i, end):
				if(isNumber(lineRead[j])): #Get the number
					number += lineRead[j]
					i += 1
				else: #We have something not part of the number
					i = j #And we tell the main loop to start from here
					numbers.append(int(number)) #So we put the number we've had so far in the list
					break
	
	if(isNumber(lineRead[end - 1])): #If the line is finished by a number, it's not put at the end of the array, so we do it ourselves
		numbers.append(int(number))
	
	return numbers

class Counter(tk.Frame):
	def isDefinedGameName(self):
		#Checks if the game name is not void
		return(self.getGameName() != TEXT_VOID)

	def getFileName(self):
		#Returns the file name, from the game name and the extension
		gameName = self.getGameName()
		fileName = gameName + FILE_EXTENSION
		return fileName

	def setGameName(self, name):
		#Change the game name
		global gameName
		gameName = name

	def getGameName(self):
		#Return the game name
		return gameName

	def setGameText(self, name):
		#Change the prefix text
		global gameText
		gameText = name
		debug(PREFIX_TEXT_SET + self.getGameText())

	def getGameText(self):
		#Return the prefix text
		return gameText

	def createGame(self):
		#Create the game file, and write the starting score in it
		fileName = self.getFileName()
		file = open(fileName,WRITE)
		file.write(self.getGameText())
		file.write("0" + SCORE_SEPARATOR + "0")
		file.close()
		self.updateGameScore()

	def restart(self):
		#Recreate the game file, erasing the previous score
		if(self.isDefinedGameName()):
			self.createGame()
			self.updateShownMessage(SCORE_RESET)
			debug(TEXT_SCORE_RESET)
		else:
			self.updateShownMessage(ERROR_NO_GAME_NAME)

	def win(self):
		#Adds one to the number of wins
		if(self.isDefinedGameName()):
			self.changeScore(WIN)
		else:
			self.updateShownMessage(ERROR_NO_GAME_NAME)

	def lose(self):
		#Adds one to the number of loses
		if(self.isDefinedGameName()):
			self.changeScore(LOSE)
		else:
			self.updateShownMessage(ERROR_NO_GAME_NAME)

	def getScore(self, scoreLine):
		scoreTab = readNumbers(scoreLine)
		wins = scoreTab[0]
		loses = scoreTab[1]
		
		return wins, loses
	
	def changeScore(self, win):
		#Change the score of the game, saving it in the file, and then update it
		#Positive : win ; Negative or null : loss
		if(self.isDefinedGameName()):
			if win > 1:
				win = 1
			if win < 0 :
				win = 0

			global gameName
			fileName = self.getFileName()
			if os.path.isfile(fileName): #Checks if the file exists
				file = open(fileName,READ)
				if(emptyFile(file)):
					debug(fileName + TEXT_IS_EMPTY_FILE)
					file.close()
					self.createGame()
				wins, loses = self.getScore(self.getGameScore())
				wins += win
				loses += 1 - win
				if(win):
					debug(GAME_WON_VICTORY)
					self.updateShownMessage(GAME_WON_VICTORY)
				else:
					debug(GAME_LOST_DEFEAT)
					self.updateShownMessage(GAME_LOST_DEFEAT)
				file.close()
				file = open(fileName,WRITE)
				file.write(self.getGameText())
				file.write(str(wins) + SCORE_SEPARATOR + str(loses))
				file.close()
			else: #If not, create the file
				self.createGame()

			self.updateGameScore()
			debug(TEXT_GAME_SCORE + self.getGameScore())
		else:
			self.updateShownMessage(ERROR_NO_GAME_NAME)

	def getGameScore(self):
		#Get the game score from the file
		fileName = self.getFileName()
		if os.path.isfile(fileName):
			file = open(fileName,READ)
			wins, loses = self.getScore(file.read())
			score = str(wins) +  SCORE_SEPARATOR + str(loses)
			file.close()
			return score
		else:
			#Create the file
			file = open(fileName,WRITE)
			file.close()
			#Should never get an infinite loop since the file is created right before the call
			self.getGameScore()

	def updateShownMessage(self, message):
		self.gameMiscText.configure(text=message)

	def updateGameScore(self):
		#Updates the game score shown
		self.gameScore.configure(text=self.getGameScore())

	def changeGame(self):
		#Change the game name, and if the file corresponding to that game does not exist, create it
		enteredText = self.gameNameEntry.get()
		if(enteredText == TEXT_VOID):
			shownMessage = ERROR_ENTER_SOMETHING + " - " + ERROR_GAME_NAME_NOT_CHANGED
		else:
			self.setGameName(enteredText)
			gameName = self.getGameName()
			fileName = gameName + FILE_EXTENSION
			if not(os.path.isfile(fileName)):
				self.createGame()
			gameScore = self.getGameScore()
			self.updateGameScore()
			debug(self.getGameName())
			shownMessage = GAME_SELECTED + " : " + enteredText

		self.updateShownMessage(shownMessage)

	def changeText(self):
		#Change the text put before the score
		enteredText = self.gameTextEntry.get()
		if(enteredText != TEXT_VOID):
			self.setGameText(enteredText)

		self.updateShownMessage(enteredText)

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		##Game
		#Name
		self.gameNamePrompt = tk.Label(self, text=ENTER_GAME_NAME)
		self.gameNameEntry = tk.Entry(self, width=NB_CHAR)
		self.gameNameButton = tk.Button(self, text=SET_GAME, command = self.changeGame)
		#Prefix text
		self.gameTextPrompt = tk.Label(self, text=ENTER_PREFIX_TEXT)
		self.gameTextEntry = tk.Entry(self, width=NB_CHAR)
		self.gameTextButton = tk.Button(self, text=SET_PREFIX_TEXT, command = self.changeText)
		#Score
		self.gameScorePrompt = tk.Label(self, text=TEXT_SCORE)
		self.gameScore = tk.Label(self, text=TEXT_VOID, bg=WHITE, width=NB_CHAR)
		#Misc Text
		self.gameMiscText = tk.Label(self, text=TEXT_VOID)
		#Buttons
		self.restart = tk.Button(self, text=TEXT_RESTART, command = self.restart)
		self.win = tk.Button(self, text=TEXT_WIN_BUTTON, command = self.win)
		self.loss = tk.Button(self, text=TEXT_LOSS_BUTTON, command = self.lose)
		#Checkbutton
		self.debugCheck = tk.Checkbutton(self, text=TEXT_DEBUG_MODE, command = changeDebugMode)

		#Sets the widgets
		self.debugCheck.pack(side=BOTTOM)

		self.gameNamePrompt.pack(side=TOP)
		self.gameNameEntry.pack(side=TOP)

		self.gameTextPrompt.pack(side=TOP)
		self.gameTextEntry.pack(side=TOP)

		self.gameScorePrompt.pack(side=TOP)
		self.gameScore.pack(side=TOP)
		
		self.gameMiscText.pack(side=TOP)

		self.win.pack(side=LEFT)
		self.loss.pack(side=LEFT)
		self.restart.pack(side=LEFT)

		self.gameNameButton.pack(side=RIGHT)
		self.gameTextButton.pack(side=RIGHT)

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
	root = tk.Tk()
	root.title(WINDOW_NAME)
	root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
	Counter(root).pack(fill="both")
	root.mainloop()