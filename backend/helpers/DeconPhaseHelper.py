import sys

sys.path.append("../")


import numpy as np
from helpers import ExcelFileReaderHelper, DeconHelper, ContourPlotHelper
import time
import math
import pandas as pd


class DeconPhaseHelper:
    """
    The purpose of this class is to show off the functionality associated with reading data from an excel document,
    putting it in a contour plot, running the deconvolution method, and then plotting the resulting data in another
    contour plot.
    """

    def __init__(self):
        self.hard_df = pd.DataFrame()
        self.modu_df = pd.DataFrame()
        self.x_df = pd.DataFrame()
        self.y_df = pd.DataFrame()

    def run_process(self, file_name, sheet_name=None, excel_format=2, col="Hardness", max_iter=1500, limit=10 ** -6):
        """

        :param file_name: The name of the file we are using data from
        :param sheet_name: The name of the test data sheet we are reading from, if None then reads the first test sheet
        :param excel_format: The format of the excel file
        :param col: The column we are reading from
        :param max_iter: Max iterations for deconvolution
        :param limit: Limit of precision for deconvolution

        :return: Nothing

        Runs the deconvolution method on the data in an excel sheet. Plots several contour plots, one before and one
        after the method. Also calculates and plots the fraction of data points inside of each phase.

        """

        # Variable used for timing throughout the project
        start_time = time.time()

        # Setting up variables and reading from the excel file
        efrh = ExcelFileReaderHelper.ExcelFileReaderHelper()
        efrh.read_from_excel(file_path=file_name)
        if sheet_name is not None:
            if excel_format == 2:
                hard_df, modu_df, x_df, y_df = efrh.get_sheet(sheet_name=sheet_name, skip_first_row=True,
                                                              use_cols="B:I", hard_col_name="HARDNESS",
                                                              mod_col_name="MODULUS", x_col_name="X Position",
                                                              y_col_name="Y Position")
            else:
                hard_df, modu_df, x_df, y_df = efrh.get_sheet(sheet_name=sheet_name, skip_first_row=True,
                                                              use_cols="B:T", hard_col_name="HARDNESS",
                                                              mod_col_name="MODULUS", x_col_name="X Position",
                                                              y_col_name="Y Position")
        else:
            hard_df, modu_df, x_df, y_df = efrh.read_next_sheet_format2()

        self.hard_df = hard_df
        self.modu_df = modu_df
        self.x_df = x_df
        self.y_df = y_df

        print("Time to read everything is " + str(time.time() - start_time) + " seconds.")
        start_time = time.time()
        if col == "Hardness":
            ContourPlotHelper.plot_base_data(x_df=x_df, y_df=y_df, data_df=hard_df, prop="Hardness")
        elif col == "Modulus":
            ContourPlotHelper.plot_base_data(x_df=x_df, y_df=y_df, data_df=modu_df, prop="Modulus")
        else:
            ContourPlotHelper.plot_base_data(x_df=x_df, y_df=y_df, data_df=hard_df, prop="Hardness")
            ContourPlotHelper.plot_base_data(x_df=x_df, y_df=y_df, data_df=modu_df, prop="Modulus")

        print("Time to plot contour map is " + str(time.time() - start_time) + " seconds.")
        start_time = time.time()

        # The number of phases for the decon method
        m = 3
        # Initializes and runs the decon helper
        dh_hard = DeconHelper.DeconHelper()
        dh_modu = DeconHelper.DeconHelper()
        if col == "Hardness":
            input_data = hard_df["Data"].values
            dh_hard.run_process(input_data=input_data, max_iter=max_iter, limit=limit, label="Hardness")
        elif col == "Modulus":
            input_data = modu_df["Data"].values
            dh_modu.run_process(input_data=input_data, max_iter=max_iter, limit=limit, label="Modulus")
        else:
            input_data = hard_df["Data"].values
            dh_hard.run_process(input_data=input_data, max_iter=max_iter, limit=limit, label="Hardness")
            input_data = modu_df["Data"].values
            dh_modu.run_process(input_data=input_data, max_iter=max_iter, limit=limit, label="Modulus")

        # Prints the details of the normal curves
        # print(dh.minprumer)
        # print(dh.minstddev)
        # print(dh.minf)

        print("Time to run deconvolution method is " + str(time.time() - start_time) + " seconds.")
        start_time = time.time()

        def curve_i_normpdf(x, index_val, col_name="Hardness"):
            """

            :param x: The value being looked at
            :param index_val: The index of the decon phase
            :param col_name: The name of the column we are using

            :return: The normpdf of the value relative to the curve at index index_val

            Function used to determine which curve a point belongs to

            """
            if col_name == "Hardness":
                return math.fabs(
                    DeconHelper.normpdf(x=x, mean=dh_hard.minprumer[index_val], sd=dh_hard.minstddev[index_val]))
            else:
                return math.fabs(
                    DeconHelper.normpdf(x=x, mean=dh_modu.minprumer[index_val], sd=dh_modu.minstddev[index_val]))

        print("Time to get decon results list " + str(time.time() - start_time) + " seconds.")
        start_time = time.time()

        def get_final_results(m_val, data_df, col_name):
            """

            :param m_val: The number of phases used by the decon method
            :param data_df: The DataFrame containing the data we are getting the final results of
            :param col_name: The name of the column we are working with

            :return: A DataFrame containing the bin each raw data point lands in where each bin is a phase

            Bins all raw data values in a way where we can create a contour plot of the results.

            """

            decon_results = []
            # For every data point, determine which bin it falls into
            for i in range(data_df["Data"].values.size):
                temp_decon_list = []
                for j in range(m_val):
                    temp_decon_list.append(curve_i_normpdf(x=data_df["Data"].values[i], index_val=j, col_name=col_name))
                decon_results.append(np.argmax(temp_decon_list))

            # Makes the list into a DataFrame
            decon_results_df = pd.DataFrame(decon_results)
            decon_results_df.columns = ["Data"]

            return decon_results_df

        # Prints the resulting decon DataFrame
        # print(decon_results_df)

        if col == "Hardness":
            hard_res = get_final_results(m_val=m, data_df=hard_df, col_name="Hardness")
        elif col == "Modulus":
            modu_res = get_final_results(m_val=m, data_df=modu_df, col_name="Modulus")
        else:
            hard_res = get_final_results(m_val=m, data_df=hard_df, col_name="Hardness")
            modu_res = get_final_results(m_val=m, data_df=modu_df, col_name="Modulus")

        # Creates the same variable for the next contour plot using the same format and mostly the same data
        if col == "Hardness":
            ContourPlotHelper.plot_final_decon_data(x_df=x_df, y_df=y_df, decon_results_df=hard_res, prop="Hardness",
                                                    curr_m=m)
        elif col == "Modulus":
            ContourPlotHelper.plot_final_decon_data(x_df=x_df, y_df=y_df, decon_results_df=modu_res, prop="Modulus",
                                                    curr_m=m)
        else:
            ContourPlotHelper.plot_final_decon_data(x_df=x_df, y_df=y_df, decon_results_df=hard_res, prop="Hardness",
                                                    curr_m=m)
            ContourPlotHelper.plot_final_decon_data(x_df=x_df, y_df=y_df, decon_results_df=modu_res, prop="Modulus",
                                                    curr_m=m)

        if col == "Hardness":
            ContourPlotHelper.plot_f(dh=dh_hard, prop="Hardness", method="in each Deconvolution Phase")
        elif col == "Modulus":
            ContourPlotHelper.plot_f(dh=dh_modu, prop="Modulus", method="in each Deconvolution Phase")
        else:
            ContourPlotHelper.plot_f(dh=dh_hard, prop="Hardness", method="in each Deconvolution Phase")
            ContourPlotHelper.plot_f(dh=dh_modu, prop="Modulus", method="in each Deconvolution Phase")

        print("Time to plot final contour plot is " + str(time.time() - start_time) + " seconds.")

        return
