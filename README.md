# Linear regression

A simple linear regression algorithm. It is only a proof of concept and should
not be used in real applications due to its absurdly low speed. It can be run on
both computers and the CASIO fx-CG50.

## Origin and algorithm

I've always been curious about how linear regressions worked. After some
research, I found what the coefficient of determination was and that what linear
regressions do is try to get the lowest possible squared error.

The algorithm used is the most basic algorithm possible: it loops through slope
and y-intercept values until the best-fitting line is found. The maximum and
minimum slope and y-intercept values are found by looping through all possible
lines created by every two points and finding the lowest and highest values.

## Usage

The script will first ask you for the precision of the calculation. This is the
increment used to process all slope and y-intercept values.

After that, you'll be asked to insert points. Every point should have the
structure `x,y`, x and y being decimal numbers with a period as the decimal
separator. There can be spaces before and after x and y. After you've inserted
all points, just input and empty string.

## Notes

- In most cases, I do not recommend any precision above 0.1 on CASIO calculators
if you want the calculation to take less than a minute.

- Note that different precision calculations won't necessarily output the same
line with more or less decimal places. They can output slightly different lines,
but both will be the best fit for their precision. For example, different
precisions with the same input points can output these two lines:

	- 0.8423x + 0.2
	- 0.8877x + 0.078