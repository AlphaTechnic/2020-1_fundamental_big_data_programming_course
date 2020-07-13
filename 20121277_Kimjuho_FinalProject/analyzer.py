
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time 

class Analyzer():
    def __init__(self, DataFrame, begin_month, end_month, column_names):
        self._DataFrame = DataFrame.loc[begin_month : end_month]
        self._DataFrame_begin = begin_month
        self._DataFrame_end = end_month
        if type(column_names) == list:
            self._column_names = column_names
        else:
            self._column_names = []
            self._column_names.append(column_names)
        
        self._mean_list = []
    
    def checktime(func):
        def decorated(self, *args, **kwargs):
            start = time.time()
            func(self, *args, **kwargs)
            end = time.time()
            print("메쏘드의 실행시간은 %f초 입니다." %(end - start))

        return decorated
    
    @classmethod
    def scaling(cls, Series):
        maximum = max(Series)
        minimum = min(Series)
        Series_scaled0to1 = (Series - minimum) / (maximum - minimum)
    
        return Series_scaled0to1
    
    @checktime 
    def show_table(self):
        display(self._DataFrame)     
    
    def get_mean(self):
        self._mean_list = []
        for column_name in self._column_names:
            if column_name == '현금매출비율' or column_name == '평균기온':
                mean = round(sum(self._DataFrame[column_name]) / len(self._DataFrame[column_name]), 1)
                self._mean_list.append(mean)
            else:
                mean = int(sum(self._DataFrame[column_name]) / len(self._DataFrame[column_name]))
                self._mean_list.append(mean)
        return self._mean_list

class BarPlotMean(Analyzer):
    def __init__(self, DataFrame, begin_month, end_month, column_names, labels):
        super(BarPlotMean, self).__init__(DataFrame, begin_month, end_month, column_names)
        self._mean_list = self.get_mean()
        self._labels = labels
    
    def barplot_mean(self):
        return plt.bar(self._labels, self._mean_list)

        
class PiePlotMean(Analyzer):
    def __init__(self, DataFrame, begin_month, end_month, column_names, labels):
        super(PiePlotMean, self).__init__(DataFrame, begin_month, end_month, column_names)
        self._mean_list = self.get_mean()
        self._labels = labels
    
    def pieplot_mean(self):
        return plt.pie(self._mean_list, labels = self._labels, explode = (0, 0.1), autopct = '%1.1f%%', shadow = True)
    
class LinePlot(Analyzer):
    def __init__(self, DataFrame, begin_month, end_month, column_names):
        super(LinePlot, self).__init__(DataFrame, begin_month, end_month, column_names)
   
    def show_one_lineplot(self, title, linestyle):
        self._title = title
        fig = plt.figure(figsize = (25,6))       
        plt.xticks(rotation = 30)
        plt.suptitle(self._title, size = 14)
        plt.plot(self._DataFrame[self._column_names] ,linestyle)
        
        return fig
    
    def show_several_lineplot(self, labels, linestyles):
        fig = plt.figure(figsize = (25,6))
        for ind, column_name in enumerate(self._column_names):
            plt.plot(self._DataFrame[column_name], linestyles[ind])
        plt.legend(labels)
        plt.xticks(rotation = 30)
        
        return fig
    
    def show_lineplot_scaled(self, labels, linestyles):
        fig = plt.figure(figsize = (25,6))
        for ind, column_name in enumerate(self._column_names):
            plt.plot(Analyzer.scaling(self._DataFrame[column_name]), linestyles[ind])
        
        plt.legend(labels)
        plt.xticks(rotation = 30)
        
        return fig

class SpiderPlot():
    def __init__(self, DataFrame, column_name):
        self._DataFrame = DataFrame
        self._column_name = column_name
    
    def spiderplot_per_year(self, year):
        from math import pi
        def spider_chart_plot(values):
            months = ['1', '2','3','4','5','6','7','8','9','10','11','12']

            N = len(months)
            theta = [n / float(N) * 2 * pi for n in range(N)]

            fig = plt.figure(figsize = (5,5))
            ax1 = plt.subplot(polar = True)

            lines, labels = plt.thetagrids(range(0,360, int(360/len(months))), months)

            ax1.set_theta_offset(pi / 2)
            ax1.set_theta_direction(-1)
            
            ax1.plot(theta, values, lw = 0)
            ax1.fill(theta, values, 'b', alpha = 0.2)
            plt.ylim(0, 7000000)
            plt.title(str(year), size = 14)
            
            return fig

       
        if year == 2016:
            values = []
            for j in range(1,13):
                if 1<=j<=5:
                    values.append(0)
                else:
                    a = str(j).zfill(2)
                    index_string = '2016-' + a
                    data = self._DataFrame[self._column_name].loc[index_string]
                    values.append(data)

            return spider_chart_plot(values)

        elif year == 2017:
            values = self._DataFrame[self._column_name].loc['2017-01':'2017-12']
            return spider_chart_plot(values)

        elif year == 2018:
            values = []
            for j in range(1,13):
                if j >= 11:
                    values.append(0)
                else:
                    a = str(j).zfill(2)
                    index_string = '2018-' + a
                    data = self._DataFrame[self._column_name].loc[index_string]
                    values.append(data)

            return spider_chart_plot(values)

        else:
            print("입력 오류입니다. 2016, 2017, 2018 셋 중 하나의 수를 입력해주세요.")
