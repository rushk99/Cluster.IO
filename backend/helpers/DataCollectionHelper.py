import sys

sys.path.append("../")


from helpers import Errors, ExcelFileReaderHelper, StringDefinitionsHelper


def get_data(file_name, file_format, clustered_column):
    """

    :param file_name: The name of the file being read in
    :param file_format: The format of the file being read
    :param clustered_column: The type of column we are clustering by
    :return: One DataFrame for the data being clustered, one for the x values, and one for the y values

    Reads in all of the data from an excel file that's stored in the data folder.

    """
    
    efrh = ExcelFileReaderHelper.ExcelFileReaderHelper()
    efrh.read_from_excel(file_path=file_name)
    # TODO Specify the sheet name, have it just be a possible option
    if file_format == StringDefinitionsHelper.FILE_FORMAT_ONE:
        hard_df, modu_df, x_df, y_df,hard_mod_df = efrh.read_next_sheet_format1(nulls=True)
    elif file_format == StringDefinitionsHelper.FILE_FORMAT_TWO:
        hard_df, modu_df, x_df, y_df,hard_mod_df = efrh.read_next_sheet_format2(nulls=True)
    else:
        raise Errors.InvalidClusteringFileFormat(file_format)
    
    if clustered_column == StringDefinitionsHelper.HARDNESS_LABEL:
        data_df = hard_df
    elif clustered_column == StringDefinitionsHelper.MODULUS_LABEL:
        data_df = modu_df
    elif clustered_column=="Hard_Mod":
        data_df=hard_mod_df
    else:
        raise Errors.InvalidClusteringColumn(clustered_column)
    
    #data_df=hard_mod_df
    return data_df, x_df, y_df
