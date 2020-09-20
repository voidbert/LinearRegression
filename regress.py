#Run this even if the file is being included. This finds the system the script
#is being run on. Because CASIO calculators don't have the os module, importing
#it will fail. Constants are used because enums aren't supported on the CASIO.
SYS_CASIO = 0
SYS_PC = 1

SYSTEM = SYS_PC

try:
	import os
except:
	SYSTEM = SYS_CASIO

#Define infinity and import the needed math functions
INFINITY = float("inf")
from math import tan, atan, log10

#Represents a line in its mathematical form (y = mx + b).
class line:
	m = 0
	b = 0

	#Creates a line. This can be done in many ways:
	#line() -> creates the x axis (y = 0x + 0)
	#line(m, b) -> creates the line y = mx + b. m and b must be convertable to
	#floats through float(). Else, unless they're points, exceptions will be
	#raised.
	#line(point, point) -> creates a line that passes by 2 points. They can't
	#have the same x value because vertical lines aren't supported.
	def __init__(self, *args):
		if len(args) == 0:
			#Create the x axis be leaving m and b as is (0).
			pass
		elif len(args) == 2:
			#If both arguments are points, create a line that passes through
			#them.
			if type(args[0]) == type(args[1]) == point:
				#Because the derivative (slope) of a line is constant, calculate
				#it from the 2 points. An exception will be thrown if the line
				#is vertical because a division by 0 will be performed.
				self.m = (args[0].y - args[1].y) / (args[0].x - args[1].x)
				#Use one of the points to solve the equation y = mx + b
				#(b = y - mx).
				self.b = args[0].y - self.m * args[0].x
			else:
				#They aren't points. They must be m and b values. Make sure they
				#are floats before assigning them.
				self.m = float(args[0])
				self.b = float(args[1])
		else:
			raise Exception("Invalid number of arguments for line()")

#Represents a point in the referential.
class point:
	x = 0
	y = 0

	#Creates a point. Usages:
	#point() -> creates the point (0, 0)
	#point(x, y) -> creates the point(x, y). x and y must be floats or
	#convertable with float(). Or else, exceptions can be raised.
	#point(string) -> Parses a string with the structure "x,y", creating the
	#(x, y) point. In the string, x and y must be in decimal base and spaces are
	#allowed before and after a value. The decimal separator must be a period.
	#An exception will be raised if the string is invalid.
	def __init__(self, *args):
		if len(args) == 0:
			#No arguments. Leave x and y as 0 (default).
			pass
		elif len(args) == 1:
			#Parse the only argument as a string. Split the string by commas and
			#make sure there is only one comma (only 2 coordinates). After that,
			#parse the numbers. float() will raise an exception in case any of
			#them is invalid.
			coords = args[0].split(',')
			if len(coords) != 2:
				raise Exception("Invalid point")
			self.x = float(coords[0])
			self.y = float(coords[1])
		elif len(args) == 2:
			#The 2 arguments are an x and an y. Make sure they are floats before
			#assigning x and y. A conversion may occur.
			self.x = float(args[0])
			self.y = float(args[1])
		else:
			raise Exception("Invalid number of arguments for point()")

#This works exactly like range(), except it's for floating-point values.
def float_range(min : float, max : float, step : float):
	while min < max:
		yield min
		min += step

#Clears the screen on every type of system this script was designed for.
def clear_screen() -> None:
	#On CASIO calculators, print enough lines to fill 2 screens (in case the
	#cursor is in the first line).
	if SYSTEM == SYS_CASIO:
		for i in range(13):
			print("")
	else:
		#Run the console command that clears the screen on PCs. It's a different
		#command depending on the system, clear on POSIX and cls on Windows.
		if os.name == "nt":
			os.system("cls")
		else:
			os.system("clear")

#Clears the screen, prints an error and exits the script.
def error(message: str) -> None:
	clear_screen()
	print(message)
	raise SystemExit()

#Lets the user input one option from a list. This function will only return when
#the user inputs a valid option. There is a limit of 3 options due to the size
#of calculators' screens.
def input_option(message: str, options: list) -> int:
	#Keep printing the options and getting the user input until it is valid.
	while True:
		#Clear the screen, print the message, an empty line and the options.
		#Make sure every option is a string, so that it can be printed. Separate
		#the input from the options with a line break.
		clear_screen()
		print(message + '\n')
		for i in range(len(options)):
			print(str(i + 1) + " - " + str(options[i]))
		print("")

		#Ask for the user input. Make sure it is an integer and inside the range
		#of options. If so, return it. Else, continue the loop.
		value = input("> ")
		try:
			value = int(value)
			if 1 <= value <= len(options):
				return value
		except:
			pass

#Asks the user for the needed data to perform the regression: the points to fit
#the line to and the uncertainty of the calculation. This will return a tuple
#with the precision in the first position and the list of points on the second.
def user_input() -> tuple:
	#Ask for the precision of the regression. The more precise, the longer it
	#will take.
	precisions = [0.1, 0.01, 0.001]
	precision = precisions[input_option("Precision", precisions) - 1]

	#Ask the user for points until the input is empty.
	points = []
	while True:
		#Every message should be on a blank screen.
		clear_screen()
		print("Insert points:\n")

		pt = input("> ")
		if pt == "":
			break
		#Parse the point. It it's invalid (an exception is thrown), don't add it
		#to the list.
		try:
			points.append(point(pt))
		except:
			pass

	return (precision, points)

#Gets the minimum and maximum m and b values. This way, the performance is
#better because less values are processed. This will return the following tuple:
#lowest_m, highest_m, lowest_b, highest_b
def limits(points: list) -> tuple:
	#For every pair of 2 points, create a line that passes through them, always
	#registering the highest and lowest m and b values. This special loop
	#doesn't repeat inverted pairs like (a, b) and (b, a).
	lowest_m, highest_m, lowest_b, highest_b = INFINITY, -INFINITY, INFINITY, \
		-INFINITY
	for i in range(len(points)):
		for j in range(i + 1, len(points)):
			l = line(points[i], points[j])
			lowest_m = min(lowest_m, l.m)
			highest_m = max(highest_m, l.m)
			lowest_b = min(lowest_b, l.b)
			highest_b = max(highest_b, l.b)
	
	return lowest_m, highest_m, lowest_b, highest_b

#Performs the linear regression by testing all the values between the possible m
#an b limits and determining the best line with a certain precision.
def regression(points: list, lim: tuple, precision: list) -> line:
	#Convert the slope to an angle. This is because small changes cause bigger
	#visual differences in smaller slopes, while the same angle change is always
	#the same.
	lowest_angle, highest_angle = atan(lim[0]), atan(lim[1])
	#Keep track of the lowest error registered until now and the line to it
	#correspondent.
	lowest_error = INFINITY
	best_line = None
	for m in float_range(lowest_angle, highest_angle, precision):
		for b in float_range(lim[2], lim[3], precision):
			#Test the line with this m and this b (convert m to a value and not
			#an angle). Calculate the squared error by summing all squared
			#vertical distances to every point.
			l = line(tan(m), b)
			error = 0
			for point in points:
				error += (point.y - (l.m * point.x + l.b)) ** 2
			#If this is the lowest error until now registered, update it and set
			#the line correspondent to it.
			if error < lowest_error:
				lowest_error = error
				best_line = l

	return best_line

#Calculates the r^2 of a regression from the line fit and the points the user
#inputted. This can also return the string "undefined" if a division by 0 is
#performed during the calculation.
def calculate_r2(l: line, points: list) -> float:
	#Calculate the average y value.
	avg_y = 0
	for pt in points:
		avg_y += pt.y
	avg_y /= len(points)

	#Calculate the total sum of squares and the sum of squares of the residuals.
	SStot = 0
	for pt in points:
		SStot += (pt.y - avg_y) ** 2
	SSres = 0
	for pt in points:
		SSres += (l.m * pt.x + l.b - pt.y) ** 2

	#Calculate r^2 and return it. If a division by 0 happens, return "undefined"
	try:
		return 1 - (SSres / SStot)
	except:
		return "undefined"

#Prints a line to the screen with all its characteristics. The user input data
#must be also provided.
def print_line(l: line, data: tuple) -> None:
	clear_screen()
	print("y = mx + b")

	#Round m to 3 decimal places because it for sure won't be more precise than
	#that. 
	print("m = " + str(round(l.m, 4)))
	#Round b to the number of decimal places of the precision.
	print("b = " + str(round(l.b, -int(log10(data[0])))))

	print("r2 = " + str(calculate_r2(l, data[1])))

	#Print 2 lines on calculators to fill the screen
	print("\n")

#The entry point of the script.
def main():
	#Ask the user for the needed information about the line and the regression.
	data = user_input()

	#If no points or only one point was inputted, it's impossible to fit a line.
	if len(data[1]) < 2:
		error("Not enough points for a regression")
	elif len(data[1]) == 2:
		#There are only two points. A line that passes through them (without a
		#full regression) is possible. Make sure they don't have the same x, as
		#a vertical line would cause a division by 0.
		if data[1][0].x == data[1][1].x:
			error("Two points can't have the same X")
		l = line(data[1][0], data[1][1])
		print_line(l, data)
	else:
		#There are more than 2 points. Perform a full regression. First, make
		#sure that there no points with the same x value, forming a vertical
		#line. That can cause exceptions later. This special loop doesn't repeat
		#inverted pairs ((a, b) doesn't show up as (b, a)).
		for i in range(len(data[1])):
			for j in range(i + 1, len(data[1])):
				if data[1][i].x == data[1][j].x:
					clear_screen()
					print("2 points with the same X value")
					raise SystemExit()
		
		#Calculate the minimum and maximum possible m and b values. This reduces
		#the number of values processed for better performance.
		lim = limits(data[1])

		#If there is only one slope possible (account for the given precision),
		#there is only one possible line (the points are collinear).
		if abs(lim[0] - lim[1]) <= data[0]:
			#Print that line (line between any of the 2 points).
			l = line(data[1][0], data[1][1])
			print_line(l, data)
			return

		#Perform the regression and print the resulting line.
		l = regression(data[1], lim, data[0])
		print_line(l, data)

#If this script isn't being included, call the entry point. Because CASIOs don't
#support __name__, always call main on CASIOs.
if __name__ == "__main__" or SYSTEM == SYS_CASIO:
	main()