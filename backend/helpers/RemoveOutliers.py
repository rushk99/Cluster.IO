import sys

sys.path.append("../")

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from helpers import PDFHelper
import pandas as pd


def remove_data_from_outliers(data_df, x_df, y_df, show_plots=False, show_extra_plots=False, method="Z-Score"):
    """

    :param data_df: A DataFrame which holds all of the data we will be detecting outliers in
    :param x_df: A DataFrame of the x coordinates of the grid
    :param y_df: A DataFrame of the y coordinates of the grid
    :param show_plots: Whether or not to show the pdf and contour plots
    :param show_extra_plots: Whether or not to show the extra interpolation step plots
    :param method: The method to remove outliers by, must be "Z-Score" or "IQR" as of right now

    :return: A DataFrame without outliers

    Removes the outliers inside of the data_df DataFrame and corrects them according to the data around them in
    their grid.

    """

    pdfh = PDFHelper.PDFHelper()

    pdfh.calculate_vals(input_data=data_df["Data"].values)

    if show_plots:
        pdfh.plot_vals()

        # Setting up variables to use for contour plot
        x_values = np.unique(x_df["Data"].values)
        y_values = np.unique(y_df["Data"].values)
        z_values = np.rot90(data_df["Data"].values.reshape(len(np.unique(x_df)), len(np.unique(y_df))))

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.set_aspect('equal')
        # Plots contour plot
        cf = ax.contourf(x_values, y_values, z_values)
        # Plots color bar
        cb = fig.colorbar(cf, ax=ax)
        # Plot labels
        cb.set_label("Raw Values")
        plt.title("Raw Data VS Coordinate")
        plt.xlabel("X Values (um)")
        plt.ylabel("Y Values (um)")

        plt.show()

    # Store values in an data_array_1d
    data_array_1d = data_df["Data"].values

    if method == "Z-Score":
        # Remove outliers z_score many standard deviations away from the mean
        mean_val = np.mean(data_array_1d)
        stddev_val = np.std(data_array_1d)
        z_scores = 3
        data_array_1d[abs(data_array_1d - mean_val) > stddev_val * z_scores] = np.nan

    elif method == "IQR":
        # Remove outliers
        med_val = np.median(data_array_1d)

        # First quartile (Q1)
        q1 = np.median(data_array_1d[data_array_1d < med_val])

        # Third quartile (Q3)
        q3 = np.median(data_array_1d[data_array_1d > med_val])

        # Interquartile range (IQR)
        iqr = q3 - q1

        data_array_1d[data_array_1d < (q1 - 1.5 * iqr)] = np.nan
        data_array_1d[data_array_1d > (q3 + 1.5 * iqr)] = np.nan

    return correct_nulls(data_df=pd.DataFrame(data_array_1d, columns=["Data"]), x_df=x_df, y_df=y_df,
                         show_plots=show_plots, show_extra_plots=show_extra_plots)


def correct_nulls(data_df, x_df, y_df, show_plots=False, show_extra_plots=False):
    """

    :param data_df: A DataFrame of data
    :param x_df: A DataFrame of x values
    :param y_df: A DataFrame of y values
    :param show_plots: Whether or not to show the pdf and contour plots
    :param show_extra_plots: Whether or not to show the extra interpolation step plots
    
    :return: The corrected data as a DataFrame

    Corrects the nulls in the data DataFrame

    """
    num_x_vals = len(np.unique(x_df["Data"]))
    num_y_vals = len(np.unique(y_df["Data"]))

    assert num_x_vals > 0 and num_y_vals > 0
    if "Data" in data_df.columns:
        # Store values in an array
        data_1d = data_df["Data"].values

        # Show the data array before any interpolation occurs
        if show_extra_plots:
            plt.imshow(data_1d.reshape(num_x_vals, num_y_vals))
            plt.show()
        
        # Complete the first interpolation step
        interpolation_result_one = complete_interpolation(data_1d, x_df, y_df, "cubic")
        
        # Show the data array after one step of interpolation occurs
        if show_extra_plots:
            # print(grid1)
            plt.imshow(interpolation_result_one.reshape(num_x_vals, num_y_vals))
            plt.show()

        interpolation_result_two = complete_interpolation(interpolation_result_one, x_df, y_df, "nearest")

        if show_extra_plots:
            plt.imshow(interpolation_result_two.reshape(num_x_vals, num_y_vals), interpolation='nearest')
            plt.show()

        if show_plots:
            # Plotting the pdf of the cleaned data
            pdfh = PDFHelper.PDFHelper()
            pdfh.calculate_vals(input_data=interpolation_result_two)
            pdfh.plot_vals()

            # Plotting the contour plot of the cleaned data
            # Setting up variables to use for contour plot
            x_values = np.unique(x_df["Data"].values)
            y_values = np.unique(y_df["Data"].values)
            z_values = np.rot90(interpolation_result_two.reshape(num_x_vals, num_y_vals))

            fig, ax = plt.subplots(figsize=(6, 6))

            ax.set_aspect('equal')
            # Plots contour plot
            cf = ax.contourf(x_values, y_values, z_values)
            # Plots color bar
            cb = fig.colorbar(cf, ax=ax)
            # Plot labels
            cb.set_label("Clean Values")
            plt.title("Clean Data VS Coordinate")
            plt.xlabel("X Values (um)")
            plt.ylabel("Y Values (um)")

            plt.show()

        ret_df = pd.DataFrame(interpolation_result_two, columns=["Data"])
        return ret_df
    elif "Hardness" in data_df.columns and "Modulus" in data_df.columns:
        # Interpolate the "Hardness" and "Modulus" columns separately
        hardness_data = data_df["Hardness"].values
        modulus_data = data_df["Modulus"].values

        # Interpolate the hardness column
        hardness_interpolation_one = complete_interpolation(hardness_data, x_df, y_df, "cubic")
        hardness_interpolation_two = complete_interpolation(hardness_interpolation_one, x_df, y_df, "nearest")
        hardness_df = pd.DataFrame(hardness_interpolation_two, columns=["Hardness"])

        # Interpolate the modulus column
        modulus_interpolation_one = complete_interpolation(modulus_data, x_df, y_df, "cubic")
        modulus_interpolation_two = complete_interpolation(modulus_interpolation_one, x_df, y_df, "nearest")
        modulus_df = pd.DataFrame(modulus_interpolation_two, columns=["Modulus"])

        # Concatenate the two DataFrames
        ret_df = pd.concat([hardness_df, modulus_df], axis=1)

        return ret_df


def complete_interpolation(data_list, x_df, y_df, method):
    """

    :param data_list: A list of data we are interpolating
    :param x_df: A DataFrame containing all x values
    :param y_df: A DataFrame containing all y values
    :param method: The method we are using to interpolate. This is based on the interpolate.griddata method so refer
        to their documentation. We typically use 'cubic' and then 'nearest'.

    :return: A 1D array of interpolated results

    This method will attempt to interpolate any and all null values in a list of data. It will then
    return the product of the interpolation process. This is not guaranteed to fill in all null values.

    """
    num_x_vals = len(np.unique(x_df["Data"]))
    num_y_vals = len(np.unique(y_df["Data"]))
    
    data_2d = data_list.reshape(num_x_vals, num_y_vals)
    # For every invalid value that exists, mark it as being invalid
    masked_data_2d = np.ma.masked_invalid(data_2d)
    
    # All possible points
    all_x_values = np.reshape(x_df["Data"].values, (num_x_vals, num_y_vals))
    all_y_values = np.reshape(y_df["Data"].values, (num_x_vals, num_y_vals))

    # This value will be false in every cell that needs to be replaced
    data_2d_mask = ~masked_data_2d.mask

    # Get only the valid values
    null_x_values = all_x_values[data_2d_mask]
    null_y_values = all_y_values[data_2d_mask]

    # Get all of the valid values
    unmasked_data_2d = masked_data_2d[data_2d_mask]
    
    # Complete the interpolation and get a grid result back
    interpolated_grid = interpolate.griddata((null_x_values, null_y_values), unmasked_data_2d,
                                             (all_x_values, all_y_values), method=method)

    # Return the grid reshaped into a 1D array
    return interpolated_grid.reshape(-1, 1)
