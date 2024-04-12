import logging
import json
import re

logger = logging.getLogger(__name__)

def streamline(search_response):
    """
    Streamlines a vectara response (starting with a specific response under the outer array)

    :param search_response: the first response inside the array response
    :return: a dict containing a "summary" with citations streamlined and a list of results used with ordering preserved
    """

    # TODO 1. Create a list of search results
    # TODO 2. Iterate through the summary, and record which search result is used at which index

    summary_text = search_response['summary'][0]['text']
    logger.info(f"Found summary:\n{summary_text}")

    find_result = re.finditer(r"\[(\d)\]", summary_text)

    index = 1
    dict_map = {}

    # The end index of the last match.
    last_end = None

    results = []

    result_index = []

    for match_obj in find_result:
        match = match_obj.group(1)
        logger.info(f"At {index} we found {match}")
        start = match_obj.start()
        end = match_obj.end()

        if match in dict_map:
            logger.info(f"We already have result [{match}] at position [{dict_map[match]}]")
            pass
        else:
            logger.info(f"Recording result [{match}] at position [{index}]")
            dict_map[match] = index
            result_index.append(int(match))
            index += 1

        if last_end:
            logger.info("Using end of the last match to get last text chunk")
            results.append(summary_text[last_end:start])
        else:
            logger.info("First iteration, use everything from beginning to start")
            if start > 0:
                results.append(summary_text[0:start])

        results.append("[" + str(dict_map[match]) + "]")

        last_end = end

    if last_end < len(summary_text):
        results.append(summary_text[last_end:])

    result_summary = "".join(results)

    logger.info(f"After transformation, we have the following summary:\n{result_summary}")

    logger.info(f"The mapping to the result summary is as follows:\n{result_index}")

    streamline_response = {
        "summary": result_summary,
        "result_indexes": result_index
    }
    return streamline_response

