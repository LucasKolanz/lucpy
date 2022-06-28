import lucpy as lp
import numpy as np
from random import random

test_plotions = {
	"title": "title",
	"plottitles": ["1","2","3","4"],
		#needs to be a list even if just one title
		#if singleaxis is true then this will be overall title
	"xlabel": "x axis",
	"ylabel": "y axis",
	"singleaxis": False,
		#if true then plotshape does nothing
	"plotshape": (2,2),
		#must be (row,column) order
	"xscale": "linear",
	"yscale": "linear",
	"fontsize": 25,
	"legends": [["pooty"],["skaa"],["ba"],["b"]],
		#should be a list whose first dimension corresponds to plots and 
		#second dimension corresponds to different legend entries within 
		#a single plot
	"gridlines": False,
	"gridspacing": 1,
	"figsize": (15,10),
}

test_plotions1 = {
	"title": r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
	"plottitles": ["1","2","3","4"],
		#needs to be a list even if just one title
		#if singleaxis is true then this will be overall title
	# "ylim": [0.0001,1.1],
	"xlabel": "x axis",
	"ylabel": "y axis",
	"singleaxis": True,
		#if true then plotshape does nothing
	"plotshape": (2,2),
		#must be (row,column) order
	"xscale": "linear",
	"yscale": "log",
	"fontsize": 25,
	"legends": [["pooty","skaa","ba","b"]],
	# "legends": [["pooty","skaa","ba","b"]],
		#should be a list whose first dimension corresponds to plots and 
		#second dimension corresponds to different legend entries within 
		#a single plot
		#if legend shape does not match shape of plots, it will do its
		#best but weird things may happen
	"gridlines": True,
	"gridspacing": 1,
	"markevery": "extrapolate"
}



# lpplot = lp.plot(plotions=test_plotions)
lpplot = lp.plot(plotions=test_plotions1)
# lpplot = lp.plot()

start = 0.01
stop = 1
ds = 0.01
test_x_data = np.arange(start,stop+ds,ds)
for i in range(test_x_data.size):
	if random() < 0.8:
		test_x_data[i] = np.nan

#this array gives off by 1 error
# test_x_data = np.array([0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.16,0.17,0.18,np.nan,np.nan,np.nan,0.22,np.nan,np.nan,np.nan,np.nan,0.27,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.4,np.nan,np.nan,np.nan,np.nan,np.nan,0.46,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.54,np.nan,0.56,np.nan,0.58,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.69,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.76,np.nan,np.nan,np.nan,np.nan,0.81,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.88,np.nan,0.9,np.nan,0.92,np.nan,np.nan,np.nan,np.nan,np.nan,0.98,np.nan,np.nan])
#this one does not
# test_x_data = np.array([np.nan, np.nan, 0.03, np.nan, 0.05, np.nan, np.nan, np.nan, 0.09, 0.09999999999999999, np.nan, np.nan, np.nan, np.nan, 0.15000000000000002, np.nan, np.nan, np.nan, np.nan, np.nan, 0.21000000000000002, 0.22, np.nan, np.nan, 0.25, np.nan, np.nan, np.nan, 0.29000000000000004, np.nan, np.nan, np.nan, np.nan, np.nan, 0.35000000000000003, np.nan, 0.37, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.47000000000000003, np.nan, np.nan, 0.5, np.nan, np.nan, np.nan, np.nan, np.nan, 0.56, np.nan, np.nan, 0.59, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.72, np.nan, np.nan, 0.75, np.nan, 0.77, np.nan, np.nan, np.nan, 0.81, np.nan, np.nan, np.nan, np.nan, 0.86, np.nan, np.nan, np.nan, 0.9, np.nan, np.nan, 0.93, np.nan, np.nan, np.nan, np.nan, 0.98, np.nan, np.nan])

test_y_data = []
test_y_data.append(test_x_data**2)
test_y_data.append(test_x_data**3)
test_y_data.append(test_x_data**4)
test_y_data.append(test_x_data**5)


test_y_data = np.array(test_y_data)
# test_x_data = np.array([test_x_data])
lpplot.gen_fig(test_x_data,test_y_data)