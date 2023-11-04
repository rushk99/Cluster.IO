"""
Last Modified on 7/31
"""

from helpers import BinHelper


class PDFHelper:
    def __init__(self):
        self.bh = BinHelper.BinHelper()

    def calculate_vals(self, input_data, min_val=None, max_val=None, min_lim=0.07, min_lim_large=0.02,
                       max_lim=0.10, max_lim_large=0.30, max_case_multiplier=0.75, min_case_multiplier=1.25,
                       large_corr_mult=3.0, init_bin_inc=1.0):
        """

        :param input_data: The data we will be generating pdf values on
        :param min_val: The min value we want to look at in the input data
        :param max_val: The max value we want to look at in the input data
        :param min_lim: The min value in a single in a bin that isn't acceptable for the max of all bin percentages
        :param min_lim_large: If the max percentage in pdf is above this use more a more extreme correction
        :param max_lim: The max value in a single in a bin that isn't acceptable for the max of all bin percentages
        :param max_lim_large: If the max percentage in pdf is below this use more a more extreme correction
        :param max_case_multiplier: Used in max extreme correction case
        :param min_case_multiplier: Used in min extreme correction case
        :param large_corr_mult: The multiplier for correction compared to the original
        :param init_bin_inc: The initial bin increment to use, really doesn't matter as long as you aren't of by 10e5

        :return: Nothing

        This will find the pdf values associated with the input data set using the BinHelper object. This object will
        also automatically get the bin increment value over time. If the percentage is to large in one bin, it reduces
        bin size. If it is too small in the largest bin, then it increases bin size. Does this process until it gets
        an acceptable value as the max of all pdf bins.

        """

        # This is where we set the correction factor for the extreme cases
        max_case_large_multiplier = max_case_multiplier / large_corr_mult
        min_case_large_multiplier = min_case_multiplier * large_corr_mult

        # Sets up the initial bin increment
        bin_increment = init_bin_inc

        # We need to first generate pdf values in order to get the max of all the pdf values
        pdf_vals = self.bh.generate_values(input_data=input_data, min_val=min_val, max_val=max_val,
                                           bin_increment=bin_increment)
        max_val = max(pdf_vals)

        # While the max of pdf values is outside the acceptable range, change bin size
        while min_lim > max_val or max_val > max_lim:
            # Above max extreme case
            if max_val > max_lim_large:
                bin_increment = bin_increment * max_case_large_multiplier
            # Below min extreme case
            elif max_val < min_lim_large:
                bin_increment = bin_increment * min_case_large_multiplier
            # Above max case
            elif max_val > max_lim:
                bin_increment = bin_increment * max_case_multiplier
            # Below min case
            elif max_val < min_lim:
                bin_increment = bin_increment * min_case_multiplier
            # Generate the pdf values again
            pdf_vals = self.bh.generate_values(input_data=input_data, min_val=None, max_val=None,
                                               bin_increment=bin_increment)
            # Look at the max again
            max_val = max(pdf_vals)
            # Rinse and repeat until it is acceptable...

        return

    def plot_vals(self, label=None):
        """

        :param label: The label of the plot if it has one, such as Hardness or Modulus

        :return: Nothing

        Plots the values in the BinHelper object, you need to run the calculate_vals method before this

        """

        self.bh.plot_values(label=label)
        return
