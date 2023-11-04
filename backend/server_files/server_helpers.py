from helpers import MainCallable, StringDefinitionsHelper


async def cluster_helper(method, clustering_details,file_name,clusterDataOn):
    """
    Runs clustering methods with a default file
    :param method: the clustering method to run
    :param clustering_details: the parameters for the clustering method
    :return: A response results and/or errors
    """
    try:
        await MainCallable.execute(method, clustering_details, file_name, StringDefinitionsHelper.FILE_FORMAT_TWO,
                                   clustered_column=clusterDataOn)
    except Exception as e:
        error = e.args
        response = createResponse(e, "","","")
        return response
    else:
        rawData = ""
        clusteredData = ""
        clustersFractions = ""
        response = createResponse("", rawData, clusteredData, clustersFractions)
        return response


def createResponse(error, rawData, clusteredData,clustersFractions ):
    """
    Formats results and errors for sending as a response via the API
    :param error: errors
    :param result: results
    :return: a dict of results and errors
    """
    return {"error": error, "rawData": rawData, "clusteredData":clusteredData, "clustersFractions":clustersFractions}
