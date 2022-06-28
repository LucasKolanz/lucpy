import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


#default colors and linestyles
defaultcolors = ['red','blue','black','orange']
defaultlinestyles = ['--','-','dashdot','dotted']
defaultmarkerstyles = ['o','s','v','*']

default_plotions = {
	"title": "suptitle",
	"plottitles": ["plottitle"],
		#needs to be a list even if just one title
		#if singleaxis is true then this will be overall title
	"xlabel": "x",
	"ylabel": "y",
	"fontsize": 20,
	"singleaxis": True,
	"plotshape": (1,1),
		#must be (row,column) order
	"xscale": "linear",
	"yscale": "linear",
	"xlim": 'auto',
	"ylim": 'auto',
	"legends": [],
		#should be a list whose first dimension corresponds to plots and 
		#second dimension corresponds to different legend entries within 
		#a single plot
		#if legend shape does not match shape of plots, it will do its
		#best but weird things may happen
	"figsize": (15,10),
	"gridlines": False,
	"gridspacing": 1,
	"colors": defaultcolors,
	"linestyles": defaultlinestyles,
	"markerstyles": defaultmarkerstyles,
	"markevery": "extrapolate",
	#TODO
	#test for different plots different x vals
}		

class plot():
	"""docstring for plot"""

	

	def __init__(self, plotions=default_plotions):
		super(plot, self).__init__()
		plotions = self.parse_arguments(plotions)

		self.title = plotions["title"]
		self.plottitles = plotions["plottitles"]
		self.xlabel = plotions["xlabel"]
		self.ylabel = plotions["ylabel"]
		self.xlim = plotions["xlim"]
		self.ylim = plotions["ylim"]
		self.fontsize = plotions["fontsize"]
		self.plotshape = plotions["plotshape"]
		self.singleaxis = plotions["singleaxis"]
		if self.singleaxis:
			self.plotshape = (1,1)
		self.plotsize = self.plotshape[0]*self.plotshape[1]
		self.yscale = plotions["yscale"]
		self.xscale = plotions["xscale"]
		self.gridlines = plotions["gridlines"]
		self.gridspacing = plotions["gridspacing"]
		self.legends = plotions["legends"]
		self.figsize = plotions["figsize"]
		self.colors = plotions["colors"]
		self.linestyles = plotions["linestyles"]
		self.markerstyles = plotions["markerstyles"]
		self.markevery = plotions["markevery"]


		plt.rcParams.update({'font.size': self.fontsize})
		plt.rcParams['text.usetex'] = True


	def parse_arguments(self,arguments):
		plotions = default_plotions
		for key in arguments.keys():
			if key in plotions.keys():
				plotions[key] = arguments[key]
		return plotions

	#number of possible plots with given data must be same as desired
	#plotshape
	def gen_fig(self,xdata,ydata):

		# #test if the shape of data matches shape of desired plotshape
		if not self.singleaxis and ydata.shape[0] != self.plotsize:
			print("ERROR: shape of data must match shape of desired plotshape.")
			print("Desired shape of plot is {}".format(self.plotshape))
			print("Thus the desired length is {}".format(self.plotsize))
			print("Length of data input is {}".format(ydata.shape[0]))	
			return

		if self.plotsize == 0:
			print("ERROR: shape of plot cannot be zero")

		self.fig,self.axes = plt.subplots(nrows=self.plotshape[0],ncols=self.plotshape[1],figsize=self.figsize)
		
		if self.singleaxis:
			self.axes = [self.axes]
			xdata = np.array([xdata])
		else:
			#check if shape of x and y data given is the same
			#if not then duplicate xdata to be same size as ydata
			if xdata.shape[0] != ydata.shape[0]:
				temp_x = []
				for i in range(ydata.shape[0]):
					temp_x.append(xdata)
				xdata = np.array(temp_x)
			self.axes = self.axes.flatten()

		self.plot_axes(xdata,ydata)
		
		self.fig.tight_layout()
		plt.show()

	def extrapolate(self,xdata,ydata):
		markevery = np.where(np.isnan(xdata),False,True).tolist()
		
		for xindex in range(xdata.shape[0]):
			# print(np.argwhere(~np.isnan(xdata[xindex]))[:,0])
			notnanindex = np.argwhere(~np.isnan(xdata[xindex]))[:,0]

			for ind in range(notnanindex.shape[0]-1):

				if notnanindex[ind+1] != notnanindex[ind]+1:
					x1 = xdata[xindex,notnanindex[ind]]
					x2 = xdata[xindex,notnanindex[ind+1]]

					dx = (xdata[xindex,notnanindex[ind+1]]-xdata[xindex,notnanindex[ind]])/(notnanindex[ind+1] - notnanindex[ind])

					new_slice = np.arange(xdata[xindex,notnanindex[ind]], xdata[xindex,notnanindex[ind+1]], dx)
					old_slice = xdata[xindex,notnanindex[ind]:notnanindex[ind+1]]
					leng = min(len(new_slice),len(old_slice))

					xdata[xindex,notnanindex[ind]:notnanindex[ind+1]][:leng] = new_slice[:leng]
					# if xdata.shape[0] == 1:
					for yindex in range(xindex,ydata.shape[0]):
						# if yindex > xdata.shape[0]-1:
						# 	yindex = xdata.shape[0]-1
						y1 = ydata[yindex,notnanindex[ind]]
						y2 = ydata[yindex,notnanindex[ind+1]]
						if self.yscale == 'log' and self.xscale == 'linear':
							m = (np.log(y2/y1))/(x2-x1)
							ydata[yindex,notnanindex[ind]:notnanindex[ind+1]] = np.exp(m*(xdata[xindex,notnanindex[ind]:notnanindex[ind+1]]-x1)+np.log(y1))

						elif self.xscale == 'linear' and self.xscale == 'log':
							m = (y2-y1)/(np.log(x2/x1))
							ydata[yindex,notnanindex[ind]:notnanindex[ind+1]] = m*(xdata[xindex,notnanindex[ind]:notnanindex[ind+1]]-x1)+y1

						elif self.xscale == 'log' and self.xscale == 'log':
							m = (np.log(y2/y1))/(np.log(x2/x1))
							ydata[yindex,notnanindex[ind]:notnanindex[ind+1]] = np.exp(m*(np.log(xdata[xindex,notnanindex[ind]:notnanindex[ind+1]])-np.log(x1))+np.log(y1))

						else:
							m = (y2-y1)/(x2-x1)
							ydata[yindex,notnanindex[ind]:notnanindex[ind+1]] = m*(xdata[xindex,notnanindex[ind]:notnanindex[ind+1]]-x1)+y1
					# else:
					# 	yindex = xindex
					# 	y1 = ydata[yindex,notnanindex[ind]]
					# 	y2 = ydata[yindex,notnanindex[ind+1]]
					# 	m = (y2-y1)/(x2-x1)
					# 	ydata[yindex,notnanindex[ind]+1:notnanindex[ind+1]+1] = m*(xdata[xindex,notnanindex[ind]:notnanindex[ind+1]]-x1)+y1
		return xdata, ydata, markevery


	def plot_axes(self,xdata,ydata):
		if self.markevery == "extrapolate":
			xdata,ydata,self.markevery = self.extrapolate(xdata,ydata) 

		#make figsize a plotion in future
		self.set_axes_limits(xdata,ydata)
		for index in range(ydata.shape[0]):
			if self.singleaxis:
				xindex = 0
			else:
				xindex = index
			styleindex = index%len(self.colors)
			self.axes[xindex].plot(xdata[xindex],ydata[index], \
				color=self.colors[styleindex], \
				linestyle=self.linestyles[styleindex], \
				marker=self.markerstyles[styleindex], \
				markevery=self.markevery[xindex])

			self.axes[xindex].set_title(self.plottitles[xindex])
			self.axes[xindex].set_xlabel(self.xlabel)
			self.axes[xindex].set_ylabel(self.ylabel)
			self.axes[xindex].set_xscale(self.xscale)
			self.axes[xindex].set_yscale(self.yscale)
			# print([np.nanmin(xdata),np.nanmax(xdata)])

			if len(self.legends) > xindex:
				self.axes[xindex].legend(self.legends[xindex])
			if self.gridlines:
				# loc = plticker.MultipleLocator(base=self.gridspacing)
				# self.axes[xindex].xaxis.set_major_locator(loc)
				# self.axes[xindex].yaxis.set_major_locator(loc)
				self.axes[xindex].grid(b=True, which='major', color='#666666', linestyle='-')

		if not self.singleaxis:
			self.fig.suptitle(self.title)

	def set_axes_limits(self,xdata,ydata):

		max_x = np.nan
		min_x = np.nan
		max_y = np.nan
		min_y = np.nan
		for index in range(ydata.shape[0]):
			if self.singleaxis:
				xindex = 0
			else:
				xindex = index
			styleindex = index%len(self.colors)
			if self.xlim == 'auto':
				step = (np.nanmax(xdata[xindex])-np.nanmin(xdata[xindex]))/25
				maxi = np.nanmax(xdata[xindex])
				mini = np.nanmin(xdata[xindex])

				if self.xscale == "log":
					mincorrection = mini/5
					maxcorrection = maxi/5
				else:
					mincorrection = step
					maxcorrection = step
				
				if self.singleaxis:
					if maxi > max_x or np.isnan(max_x):
						max_x = maxi
					if mini < min_x or np.isnan(min_x):
						min_x = mini

					xlim = [min_x-mincorrection,max_x+maxcorrection]
				else:
					xlim =	[mini-mincorrection,maxi+maxcorrection]
				self.axes[xindex].set_xlim(xlim)
			else:
				self.axes[xindex].set_xlim(self.xlim)
			
			if self.ylim == 'auto':
				print("dkfjhs")
				step = (np.nanmax(ydata[index])-np.nanmin(ydata[index]))/25
				maxi = np.nanmax(ydata[index])
				mini = np.nanmin(ydata[index][ydata[index]>0])
				if self.yscale == "log":
					mincorrection = mini/5
					maxcorrection = maxi/5
				else:
					mincorrection = step
					maxcorrection = step

				if self.singleaxis:
					print(max_y,maxi)
					if maxi > max_y or np.isnan(max_y):
						max_y = maxi
					if mini < min_y or np.isnan(min_y):
						min_y = mini

					ylim = [min_y-mincorrection,max_y+maxcorrection]
					print(ylim[1])
				else:
					ylim =[mini-mincorrection,maxi+maxcorrection]
				for i in range(ydata.shape[0]):
					self.axes[i].set_ylim(ylim)
			else:
				self.axes[xindex].set_ylim(self.ylim)
			
			# print(xlim)
			# print(ylim)