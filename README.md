# Linear regression

A simple linear regression algorithm. It is only a proof of concept. It can be
run on both computers and the CASIO fx-CG50 (it being useless on the latter
system, given that these calculators can perform linear regressions without any
external program).

## Origin and algorithm

I've always been curious about how linear regressions worked. After some
research, I found what the coefficient of determination was and that what linear
regressions do is try to get the lowest possible squared error.

The algorithm used is the one mentioned in the following Wikipedia article:
https://en.wikipedia.org/wiki/Simple_linear_regression

## Usage

The script will ask you to insert the points to which the line will be fitted.
Every point should have the structure `x,y`, x and y being decimal numbers with
a period as the decimal separator. There can be spaces before and after x and y.
After you've inserted all points, just input an empty string (press Enter on
computers and EXE on calculators). Note that you can't have two points with the
same x value and that you need at least two points to form a line.