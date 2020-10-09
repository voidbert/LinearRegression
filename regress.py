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

#NOTE - Both points and lines are tuples. Points are (x, y) and lines (m, b), a
#line being y = mx + b

#Asks the user to input a list of points and returns it.
def input_points():
	points = []
	#Keep asking the user for points until they input an empty string
	while True:
		print("\nInsert points:")
		input_string = input(">")

		if input_string == "":
			break
		elif input_string.lower() == "list":
			#The user asked to list the points. Do that.
			for point in points:
				print("({0}, {1})".format(point[0], point[1]))
		else:
			#Parse the point. It should have the structure x,y. Separate the
			#input by commas and parse the x and y values.
			point_strings = input_string.split(",")
			#If there isn't exactly one comma, the point is invalid.
			if len(point_strings) != 2:
				print("INVALID POINT")
				continue
			else:
				try:
					x = float(point_strings[0])
					y = float(point_strings[1])
					point = (x, y)

					#If a point with the same X value was already inserted, warn
					#the user.
					found_repeated = False
					for pt in points:
						if point[0] == pt[0]:
							print("REPEATED POINT")
							found_repeated = True
							break

					if not found_repeated:
						points.append(point)
				except:
					print("INVALID POINT")
					pass

	return points

#Returns the best-fitted line for a list of points.
def regression(points: list):
	#Calculate the averages needed to calculate the slope and the y-intercept.
	x_avg, y_avg = 0, 0
	for point in points:
		x_avg += point[0]
		y_avg += point[1]
	x_avg /= len(points)
	y_avg /= len(points)

	#Calculate the slope.
	upper, lower = 0, 0
	for point in points:
		upper += (point[0] - x_avg) * (point[1] - y_avg)
		lower += (point[0] - x_avg) ** 2
	slope = upper / lower

	#Calculate the y-intercept and return the line.
	y_intercept = y_avg - slope * x_avg
	return slope, y_intercept

#Calculates the coefficient of determination of a line for a list of points.
def r2(points: list, line: tuple):
	#Calculate the average of y values, needed to calculate r^2.
	y_avg = 0
	for point in points:
		y_avg += point[1]
	y_avg /= len(points)

	#Calculate r^2. If a division by 0 is going to be performed, return
	#"undefined".
	SS_tot = 0
	for point in points:
		SS_tot += (point[1] - y_avg) ** 2
	SS_res = 0
	for point in points:
		SS_res += (line[0] * point[0] + line[1] - point[1]) ** 2

	if SS_tot == 0:
		return "undefined"
	else:
		return 1 - (SS_res / SS_tot)

def main():
	#Ask the user for the points and perform the regression.
	points = input_points()

	#If there aren't enough points for a line, throw an error. If there are just
	#2 points, return the line that passes through both of them. Only perform a
	#regression if there are more than 2 points.
	line = None

	if len(points) < 2:
		print("Not enough points")
		exit()
	elif len(points) == 2:
		#The derivative is constant and the slope of the line.
		slope = (points[0][1] - points[1][1]) / (points[0][0] - points[1][0])
		#y = mx + b with data from a point to find b
		y_intercept = points[0][1] - slope * points[0][0]

		line = (slope, y_intercept)
		r_squared = r2(points, line)
	else:
		line = regression(points)
		r_squared = r2(points, line)

	print("\ny = mx + b")
	print("m = " + str(line[0]))
	print("b = " + str(line[1]))
	print("r2 = " + str(r_squared))

#If this script isn't being included, call the entry point. Because CASIOs don't
#support __name__, always call main on CASIOs.
if __name__ == "__main__" or SYSTEM == SYS_CASIO:
	main()