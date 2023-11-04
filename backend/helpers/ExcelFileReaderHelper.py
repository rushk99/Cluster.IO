"""
Last Modified on 7/31
"""

import pandas as pd


class ExcelFileReaderHelper:
    """
    This class is responsible for reading from excel files, especially when it needs to read from multiple sheets
    This structure allows it to only bring the excel file into memory once, saving run time.
    """

    def __init__(self):
        """
        Init method, just sets xls to None
        """
        self.xls = None
        self.found_sheet_names = False
        self.test_sheets = []
        self.current_sheet_index = 0
        self.current_sheet = ""

    def read_from_excel(self, file_path="data/1.16 um Radii Spherical Nanoindentation of 99.99 Percent CP Al.xlsx"):
        """
        :param file_path: The path to the excel file
        :return: Nothing

        Method used to read from excel document, stores the entire excel document in memory
        """
        self.xls = pd.ExcelFile(file_path)

    def get_sheet(self, sheet_name, skip_first_row=True, use_cols="D:T", hard_col_name="HARDNESS",
                  mod_col_name="MODULUS", x_col_name="X Position", y_col_name="Y Position", get_stiffness=False,
                  stif_col_name="Stiffness", nulls=False):
        """
        :param sheet_name: The name of the sheet to get from the excel document
        :param skip_first_row: A boolean of whether or not to skip the first row of data being read
        :param use_cols: The column range to read from
        :param hard_col_name: The name of the column containing the hardness data
        :param mod_col_name: The name of the column containing the modulus data
        :param x_col_name: Name of the x values column
        :param y_col_name: Name of the y values column
        :param stif_col_name: Name of the stiffness column
        :param get_stiffness: Boolean of whether or not to get the stiffness column
        :param nulls:
        :return: A DataProcessingHelper that represents the excel sheet that is being read

        Reads from the excel document already stored in memory, reading a single sheet. Returns a DataFrame containing
        the hardness values and a DataFrame containing the modulus values, in that order.

        """

        if nulls:
            test1_sheet = pd.read_excel(self.xls, sheet_name, )
        else:
            test1_sheet = pd.read_excel(self.xls, sheet_name, ).dropna()
        if any(isinstance(val, str) for val in test1_sheet.iloc[0]):
            skip_first_row = True
        else:
            skip_first_row = False
        # If skip_first_row then read every row after the first, otherwise read them all
        if skip_first_row:
            # Remove the first row from every area due to it being a units label
            # The hardness values
            hardness_column = test1_sheet[hard_col_name].iloc[1:]
            # The modulus values
            modulus_column = test1_sheet[mod_col_name].iloc[1:]
            # The x values
            x_column = test1_sheet[x_col_name].iloc[1:]
            # The y values
            y_column = test1_sheet[y_col_name].iloc[1:]
            # The stiffness column
            if get_stiffness:
                stif_col = test1_sheet[stif_col_name].iloc[1:]
        else:
            # The hardness values
            hardness_column = test1_sheet[hard_col_name].iloc[:]
            # The modulus values
            modulus_column = test1_sheet[mod_col_name].iloc[:]
            # The x values
            x_column = test1_sheet[x_col_name].iloc[:]
            # The y values
            y_column = test1_sheet[y_col_name].iloc[:]
            # The stiffness column
            if get_stiffness:
                stif_col = test1_sheet[stif_col_name].iloc[:]

        # Asserts that the columns have values
        assert hardness_column is not None
        assert modulus_column is not None
        assert x_column is not None
        assert y_column is not None
        if get_stiffness:
            assert stif_col is not None

        hard_df = pd.DataFrame(hardness_column)
        modu_df = pd.DataFrame(modulus_column)
        x_df = pd.DataFrame(x_column)
        y_df = pd.DataFrame(y_column)
        if get_stiffness:
            stif_df = pd.DataFrame(stif_col)

        # Renames columns of all read data for consistency
        hard_df = hard_df.rename(columns={hard_col_name: "Data"})
        modu_df = modu_df.rename(columns={mod_col_name: "Data"})
        x_df = x_df.rename(columns={x_col_name: "Data"})
        y_df = y_df.rename(columns={y_col_name: "Data"})
        if get_stiffness:
            stif_df = stif_df.rename(columns={stif_col_name: "Data"})

        # Makes all read data numeric
        hard_df["Data"] = pd.to_numeric(hard_df["Data"], downcast="float")
        modu_df["Data"] = pd.to_numeric(modu_df["Data"], downcast="float")
        x_df["Data"] = pd.to_numeric(x_df["Data"], downcast="float")
        y_df["Data"] = pd.to_numeric(y_df["Data"], downcast="float")
        if get_stiffness:
            stif_df["Data"] = pd.to_numeric(stif_df["Data"], downcast="float")
            return hard_df, modu_df, x_df, y_df, stif_df
        hard_mod_df = pd.concat([hard_df, modu_df], axis=1)
        hard_mod_df.columns = ['Hardness', 'Modulus']
        return hard_df, modu_df, x_df, y_df,hard_mod_df

    def read_next_sheet(self, skip_first_row=True, use_cols="D:T", hard_col_name="HARDNESS", mod_col_name="MODULUS",
                        x_col_name="X Position", y_col_name="Y Position", get_stiffness=False,
                        stif_col_name="Stiffness", nulls=False):
        """

        :param skip_first_row: A boolean of whether or not to skip the first row of data being read
        :param use_cols: The column range to read from
        :param hard_col_name: The name of the column containing the hardness data
        :param mod_col_name: The name of the column containing the modulus data
        :param x_col_name: Name of the x values column
        :param y_col_name: Name of the y values column
        :param get_stiffness: Boolean of whether or not to get the stiffness column
        :param stif_col_name: Name of the stiffness column
        :param nulls:
        :return: A DataProcessingHelper that represents the excel sheet that is being read

        Reads from the excel document already stored in memory, reading a single sheet. Automated sheet
        reading is added into this process as well.
        """

        if not self.found_sheet_names:
            self.get_test_sheets()

        current_sheet = self.test_sheets[self.current_sheet_index]
        self.current_sheet = current_sheet
        self.current_sheet_index = self.current_sheet_index + 1

        return self.get_sheet(skip_first_row=skip_first_row, use_cols=use_cols, hard_col_name=hard_col_name,
                              mod_col_name=mod_col_name, sheet_name=current_sheet, x_col_name=x_col_name, nulls=nulls,
                              y_col_name=y_col_name, get_stiffness=get_stiffness, stif_col_name=stif_col_name)

    def get_test_sheets(self):
        """

        :return: Nothing

        Finds all of the sheets in the data excel file that are meant to be used for data analysis. These
        sheets have always had the format of Test # Tagged or Test # thus far so we are just checking if
        the first four letters of the sheet are Test at the moment.

        """
        sheet_names = self.xls.sheet_names

        for name in sheet_names:
            # print(name)
            if name[0:4] == "Test":
                self.test_sheets.append(name)

        # print("Names of sheets being read from as test sheets are:")
        # print(self.test_sheets)
        self.found_sheet_names = True
        return

    def is_next_sheet(self):
        """

        :return: True if there is another test sheet that can be read

        Used as a way to check if there is another test sheet after the current test sheet that can be read

        """

        if not self.found_sheet_names:
            self.get_test_sheets()

        return self.current_sheet_index < len(self.test_sheets)

    def read_next_sheet_format1(self, nulls=False):
        """

        :return: A DataProcessingHelper that represents the excel sheet that is being read
        :param nulls: Whether or not to include nulls in the data

        Reads an excel sheet in the format of the sheets we were first given to use. These have the hardness column
        named as HARDNESS and modulus as MODULUS.

        """

        return self.read_next_sheet(skip_first_row=True, use_cols="B:X", hard_col_name="HARDNESS", nulls=nulls,
                                    mod_col_name="MODULUS", x_col_name="X Axis Position", y_col_name="Y Axis Position")

    def read_next_sheet_format2(self, get_stiffness=False, nulls=False):
        """

        :param get_stiffness: Boolean of whether or not to get the stiffness column
        :param nulls: Whether or not to include nulls in the data

        :return: A DataProcessingHelper that represents the excel sheet that is being read

        Reads an excel sheet in the format of the sheets we were given that has three phases and was given
        around 8/3/20.

        """

        return self.read_next_sheet(skip_first_row=True, use_cols="A:I", hard_col_name="HARDNESS",
                                    mod_col_name="MODULUS", x_col_name="X Position", y_col_name="Y Position",
                                    get_stiffness=get_stiffness, stif_col_name="Stiffness", nulls=nulls)
