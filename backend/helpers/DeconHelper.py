import sys

sys.path.append("../")


from helpers import ExcelFileReaderHelper, PDFHelper
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


class DeconHelper:
    """
    The purpose of this class is to assist in running the deconvolution method obtained through a MatLab project.
    A lot of the comments in this file are not in English due to the original program containing them.
    """

    def __init__(self):
        self.bh = None
        self.pdf = None
        self.minprumer = None
        self.minstddev = None
        self.minf = None

    def run_process(self, input_data, m=3, max_iter=1500, limit=10 ** -6, label=None, min_val=None, max_val=None,
                    use_pdf=True, show_plots=False, save_plots=False, save_dir="", cluster_iter=0, cluster_name=""):
        """

        :param input_data: The input data the deconvolution algorithm is being performed on
        :param m: The number of normal curves to use
        :param max_iter: The max number of iterations to perform
        :param limit: The limit used for precision
        :param label: The label associated with the data's plots
        :param min_val: The min value in the input data to use
        :param max_val: The max value in the input data to use
        :param use_pdf: Whether to use the pdf model or the cdf model, true to use pdf true by default
        :param show_plots: A boolean of whether to save the plots or not
        :param save_plots: A boolean of whether to save the plots or not
        :param save_dir: The directory to save the plots to
        :param cluster_iter: The iteration of the current clustering configuration
        :param cluster_name: The name of the current clustering configuration

        :return: Nothing

        Performs the deconvolution algorithm on the given parameters. Was translated over from a MatLab project.

        """

        pdf = PDFHelper.PDFHelper()
        pdf.calculate_vals(input_data=input_data, min_val=min_val, max_val=max_val, init_bin_inc=1)
        # pdf.plot_vals(label=label)

        bh = pdf.bh

        if not use_pdf:
            prev_val = 0
            for i in range(pdf.bh.final_prob_vals.size):
                val = pdf.bh.final_prob_vals[i] + prev_val
                pdf.bh.final_prob_vals[i] = val
                print(val)
                prev_val = val

        self.bh = bh
        self.pdf = pdf

        # print("Printing the pdf_vals...")
        # print(pdf_vals)
        # print("\n\nPrinting the bin values....")
        # print(bh.x_axis)
        # print("\n\n")

        # #load property, e.g. E[GPa], save to vector E
        E = input_data

        # #load experimental probability density function
        exphist = [bh.x_axis, bh.final_prob_vals]

        bin_interval = bh.x_axis[1] - bh.x_axis[0]
        # print("The interval between bins is " + str(bin_interval))

        # #Number of phases
        # M=str2double(get(handles.edit2_M,'String'));

        # #----------------
        # #---Deconvolution algorithm
        # #-----------------
        norma2 = 1
        minnorma = 1
        # #minmeze=1
        # #minprumer=1
        # #minstddev=1
        # #minf=1
        curr_iter = 0

        # #maximum value in E vector
        maxE = max(E)
        # #dimension of E vector
        # N=length(E)
        N = E.size

        # Numpy array declarations
        meze = np.zeros(m + 1)
        index_meze = np.zeros(m + 1, dtype=np.int)

        while (norma2 > limit) and (curr_iter <= max_iter):
            # r=rand(M-1,1); #nahodny vektor M-1 cisel 0,1 -- random vector M-1 numbers 0.1
            r = np.random.uniform(low=0, high=1, size=m - 1)

            # r=sort(r); #vzestupne serazeny vektor r -- vzestupne serazeny vektor r -- rise sereny vector r -- rising order???
            r = np.sort(r)
            # meze(1)=0;  #prvni mez je na nule -- the first limit is at zero
            # meze = np.array([])
            meze[0] = 0
            # meze = np.append(meze, 0)
            # pom= maxE .* r; # generace M-1 mezi z nahodneho vektoru -- generation of M-1 between from a random vector
            pom = maxE * r
            # for i=1:M-1;
            for i in range(m - 1):
                # meze(i+1)=pom(i);  # generace M-1 mezi -- generation M-1 between
                meze[i + 1] = pom[i]  # generace M-1 mezi -- generation M-1 between
                # meze = np.append(meze, pom(i))  # generace M-1 mezi -- generation M-1 between
            # end
            # meze(M+1)=maxE; #posledni mez -- last limit
            meze[m] = maxE
            # meze = np.append(meze, maxE)

            # sE=sort(E); #vzestupne serazeny vektor E -- successively separated vector E
            sE = np.sort(E)

            # index_meze = np.array([])

            # for i=1:M+1
            for i in range(m + 1):
                # index_meze(i)=N; #naplni vektor indexu maximalni hodnotou -- fill the index vector with the maximum value
                index_meze[i] = int(N)
                # index_meze = np.append(index_meze, N)
            # end

            # index_meze(1)=0; #index pred prvni mezi je nula -- the index before the first between is zero
            index_meze[0] = int(0)

            # j=2; #zacinam od druhe meze (prvni je nula) -- starting with the second limit (the first is zero)
            j = 1

            # mez=meze(j);
            mez = meze[j]

            # for i=1:N #cyklus pres vsechny hodnoty -- cycle through all values
            for i in range(N):
                # if (sE(i) > mez):
                if sE[i] > mez:
                    # index_meze(j)=i-1; #ulozi index hodnoty, ktera lezi pod mezi --
                    # saves the index of the value that is below the limit
                    index_meze[j] = int(i - 1)

                    # j=j+1;
                    j = j + 1

                    # mez=meze(j);
                    mez = meze[j]
            # end
            # end

            # prumer = np.array([])
            # stddev = np.array([])
            # f = np.array([])
            prumer = np.zeros(m)
            stddev = np.zeros(m)
            f = np.zeros(m)

            # Can't determine what this is used for either... commenting it out
            # x=exphist(1,1); #prvni kategorie -- first category
            # x = exphist(1, 1)
            # x = exphist[0][0]
            # for i=1:M #cyklus pres faze -- cyclus pres faze
            for i in range(m):
                # vektor=sE(index_meze(i)+1:index_meze(i+1));
                vektor = sE[index_meze[i] + 1: index_meze[i + 1]]
                # if (length(vektor)>1)
                if vektor.size > 1:
                    # prumer(i) = mean(vektor);
                    prumer[i] = np.mean(vektor)
                    # stddev(i) = std(vektor);
                    stddev[i] = np.std(vektor)
                else:
                    # prumer(i) = 0;
                    prumer[i] = 0
                    # stddev(i) = 0;
                    stddev[i] = 0
                # end
                # f(i)=length(vektor)/N; #fraction
                f[i] = vektor.size / N  # fraction
            # end

            # p2 = np.array([[]])
            p2 = np.zeros((exphist[0].size, m))

            # for j=1:M #cyklus pres faze -- cyklus pres faze
            for j in range(m):
                # x=exphist(1,1);
                # x = exphist(1, 1)
                x = exphist[0][0]
                # if (prumer(j)~=0)
                if float(prumer[j]) != 0.0:
                    # p(1,j)=cdf('normal',x,prumer(j), stddev(j)); #cdf pro prvni kategorii --cdf for the first category
                    # p2(1,j)=pdf('normal',x,prumer(j), stddev(j)); #pdf
                    if use_pdf:
                        p2[0, j] = normpdf(x, prumer[j], stddev[j]) * f[j] * bin_interval
                    else:
                        p2[0, j] = norm.cdf((x - prumer[j]) / stddev[j]) * f[j] * bin_interval

                else:
                    # p(1,j)=0;
                    # p2(1,j)=0;
                    p2[0, j] = 0
                # end

                # for i = 2 : length(exphist)  #cyklus pres vsechny kategorie -- cycle through all categories
                # for i in range(2, exphist):
                for i in range(exphist[0].size):
                    # I can't find out what this x_prev var is used for... it doesn't seem to be use elsewhere
                    # x_prev=exphist(i-1,1);
                    # x_prev = exphist(i - 1, 1)
                    # x_prev = exphist[0][i - 1]
                    # x=exphist(i,1);
                    # x = exphist(i, 1)
                    x = exphist[0][i]
                    # if (prumer(j)~=0)
                    if float(prumer[j]) != 0.0:
                        # p2(i,j)=pdf('normal',x,prumer(j), stddev(j))*f(j);
                        if use_pdf:
                            p2[i, j] = normpdf(x, prumer[j], stddev[j]) * f[j] * bin_interval
                        else:
                            p2[i, j] = norm.cdf((x - prumer[j]) / stddev[j]) * f[j] * bin_interval
                    else:
                        # p2(i,j)=0;
                        p2[i, j] = 0
                    # end
                # end
            # end

            # norma2=0;
            norma2 = 0

            # p_all2 = np.array([])
            p_all2 = np.zeros(exphist[0].size)

            # for i = 1 : length(exphist)
            # for i in range(1, exphist):
            for i in range(exphist[1].size):
                # p_all2(i)=0;
                p_all2[i] = 0
                # for j=1:M #cyklus pres faze
                for j in range(m):
                    # p_all2(i)=p_all2(i)+p2(i,j);
                    p_all2[i] = p_all2[i] + p2[i, j]
                # end
                # norma2=norma2+(exphist(i,2)-p_all2(i))^2 * exphist(i,2)^2;
                # norma2 = norma2 + (exphist(i, 2) - p_all2[i]) ^ 2 * exphist(i, 2) ^ 2
                norma2 = norma2 + (exphist[1][i] - p_all2[i]) ** 2 * exphist[1][i] ** 2
            # end

            # iter=iter+1;
            curr_iter = curr_iter + 1

            # onscreen output during iteration

            # Show text
            # t=strcat('Iteration: ' , num2str(iter))
            # set(handles.text25_iter,'String',num2str(iter-1) );
            # set(handles.text28_norm,'String', num2str(norma2) );
            # drawnow;

            # if(norma2<minnorma)
            if norma2 < minnorma and sum(f) <= 1.0:
                # # output if precision was reached
                # minnorma=norma2;
                minnorma = norma2
                # minmeze=meze;
                minmeze = meze
                # minprumer=prumer;
                minprumer = prumer
                # minstddev=stddev;
                minstddev = stddev
                # minf=f;
                minf = f
                last_p_all2 = p_all2
                last_p2 = p2
                # #Show text output and graph
                # axes(handles.graf_decon); #plots the x and y data
                # cla;
                # plot(exphist(:,1), exphist(:,2),'-ko');
                # hold on; #legend ('show');
                # print("Here are some values that I think are a result of what was done above....")
                # print("The minnorma is:")
                # print(minnorma)
                # print("The minmeze is:")
                # print(minmeze)
                # print("The minprumer (mindiameter) is:")
                # print(minprumer)
                # print("The mind stddev is:")
                # print(minstddev)
                # print("The min f (function or fraction) is:")
                # print(minf)
                #
                # print("\n\n\n")

        sets = []

        self.minprumer = minprumer
        self.minstddev = minstddev
        self.minf = minf

        for j in range(m):
            # TODO Inspect area, print report doesn't make sense
            print("Distribution #" + str(j))
            print("Mean " + str(minprumer[j]))
            print("St. Dev. " + str(minstddev[j]))
            print("Fraction " + str(minf[j]))
            print("-------------------\n")
            x_axis = np.arange(min(bh.x_axis), max(bh.x_axis), 0.0001)
            if use_pdf:
                y_axis = norm.pdf(x_axis, minprumer[j], minstddev[j]) * minf[j] * bin_interval
            else:
                y_axis = norm.cdf(x_axis, minprumer[j], minstddev[j]) * minf[j] * bin_interval
            sets.append(y_axis)
            # plt.plot(x_axis, y_axis, label="Normal Curve " + str(j))
            # print(exphist[0])
            # print(last_p2[:, j])
            print("The sum of the p2 list is " + str(sum(last_p2[:, j])))
            plt.plot(exphist[0], last_p2[:, j], label="Normal Curve " + str(j))

        plt.plot(bh.x_axis, bh.final_prob_vals, "-", label="PDF")
        # plt.plot(bh.x_axis, p_all2, "-", label="Overall PDF")
        plt.plot(bh.x_axis, last_p_all2, "-", label="Overall PDF Flag")

        final_vals = np.zeros(x_axis.size)
        for item in sets:
            # TODO This is acting weird with out data set, the Overall PDF Custom
            final_vals = final_vals + item
            # final_vals = [first_val + second_val for first_val, second_val in zip(final_vals, item)]

        # plt.plot(np.arange(min(bh.x_axis), max(bh.x_axis), 0.0001), final_vals, "-", label="Overall PDF Custom")

        plt.legend(loc="best")

        if label is not None:
            plt.title(label="Probability Density Function For " + str(label))
            plt.xlabel(xlabel=label + " Values")
        else:
            plt.title(label="Probability Density Function")
            plt.xlabel(xlabel="Bin Starting Value")

        plt.ylabel(ylabel="Probability")

        if save_plots:
            # print(save_dir)
            # print(str(cluster_iter))
            # print(str(cluster_name))
            plt.savefig(save_dir + "/decon_process_data_" + str(cluster_iter) + "_" + str(cluster_name))

        if show_plots:
            plt.show()
        else:
            plt.close()

        return

    def run_process_on_file(self, file_path, is_csv, excel_format, m=3, max_iter=1500, limit=10 ** -6, col="Hardness",
                            min_val=None, max_val=None):
        """

        :param file_path: The path to the file being read
        :param is_csv: Whether or not it is a csv file
        :param excel_format: The number associated with the format of the excel file
        :param m: The number of normal curves to use
        :param max_iter: The max number of iterations to perform
        :param limit: The limit used for precision
        :param col: The label associated with the data's plots
        :param min_val: The min value in the input data to use
        :param max_val: The max value in the input data to use

        Runs the deconvolution method on a file, not requiring the user to gather the input data themselves.

        :return: Nothing

        """

        if is_csv:
            input_data = pd.read_csv(filepath_or_buffer="../data/orig_proj_data.csv")
            input_data = input_data.iloc[:].values
        else:
            efr = ExcelFileReaderHelper.ExcelFileReaderHelper()
            efr.read_from_excel(file_path=file_path)

            if excel_format == 1:
                hard_df, modu_df, x_vals, y_vals = efr.read_next_sheet_format1()
            else:
                hard_df, modu_df, x_vals, y_vals = efr.read_next_sheet_format2()

            if col == "Hardness":
                input_data = hard_df["Data"].values
            else:
                input_data = modu_df["Data"].values

        self.run_process(input_data=input_data, m=m, max_iter=max_iter, limit=limit, label=col, min_val=min_val,
                         max_val=max_val)

        return

    def run_process_on_file_both_sets(self, file_path, excel_format, m1=3, m2=3, max_iter=1500, limit=10 ** -6):
        """

        :param file_path: The path to the file being read
        :param excel_format: The number associated with the format of the excel file
        :param m1: The number of normal curves to use for the hardness vals
        :param m2: The number of normal curves to use for the modulus vals
        :param max_iter: The max number of iterations to perform
        :param limit: The limit used for precision

        :return: Nothing

        Runs the deconvolution process on an excel file. It runs the process on both the hardness and modulus columns.

        """
        self.run_process_on_file(file_path=file_path, is_csv=False, excel_format=excel_format, m=m1, max_iter=max_iter,
                                 limit=limit, col="Hardness")
        self.run_process_on_file(file_path=file_path, is_csv=False, excel_format=excel_format, m=m2, max_iter=max_iter,
                                 limit=limit, col="Modulus")
        return


def normpdf(x, mean, sd):
    """

    :param x: Value being checked
    :param mean: Mean of the normal curve
    :param sd: The standard deviation of the curve

    :return: The score of x

    Used to determine the score of a value in reference to a normal curve.

    """

    var = float(sd) ** 2
    if var == 0:
        return 0
    denom = (2 * math.pi * var) ** .5
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom
