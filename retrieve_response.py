from vectara_client.core import Factory
from vectara_client.util import _custom_asdict_factory
from argparse import ArgumentParser
from pathlib import Path
from dataclasses import asdict
from citation_util import streamline
import json
import logging
import sys

def retrieve_response():
    print("Yep")


def retrieve_response(query: str, filename: str, corpus_name: str = None, corpus_id: str = None):
    logger.info(f"Retrieving response for query [{query}]")

    # See authentication options here to configure Yaml in home directory
    # https://github.com/davidglevy/vectara-skunk-client

    target_corpus_id = None

    # Initialize Client
    client = Factory().build()
    if corpus_name:
        corpora = client.admin_service.list_corpora(corpus_name)
        corpora = filter(lambda x: x.name == corpus_name, corpora)
        if len(corpora) == 1:
            target_corpus_id = corpora[0].id
            logger.info(f"Found matching corpus [{target_corpus_id}] for name [{corpus_name}]")
        else:
            raise Exception(f"We expected a single corpus with name [{corpus_name}] but found multiple")
    else:
        target_corpus_id = corpus_id

    # Make Request
    response = client.query_service.query(query, target_corpus_id)


    # TODO Persist request (overwrite existing)
    response_json = json.dumps(asdict(response, dict_factory=_custom_asdict_factory),indent=4)
    path = Path(filename)
    logger.info(f"Persisting response to [{path.absolute}]")
    with open(path, "w") as f:
        f.write(response_json)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Setup Logging
    logging.basicConfig(format='%(asctime)s:%(name)-35s %(levelname)s:%(message)s', level=logging.INFO,
                        datefmt='%H:%M:%S %z')

    logger = logging.getLogger(__name__)

    # Parse Arguments
    parser = ArgumentParser(prog="retrieve_response.py", description="Demonstrates how to streamline citations in a "
                                                                     "summary, using either a cached response or making"
                                                                     " a new one.",
                            epilog="For instructions on configuration of vectara-skunk-client see: "
                                   "https://github.com/davidglevy/vectara-skunk-client")
    parser.add_argument("-f", "--filename", default="response.json", help="This is the name of the response file, to either use as a cache or overwrite if corpus/query specified.")
    parser.add_argument("-c", "--corpus_id", required=False, help="The corpus ID", type=int)
    parser.add_argument("-C", "--corpus_name", required=False, help="The unique name for the corpus, fails is there are two with same name")
    parser.add_argument("-q", "--query", help="The query to run if we're making a request")

    args = parser.parse_args()

    corpus_id = None
    corpus_name = None
    query = None
    filename = args.filename

    # Retrieve and validate corpus_id/corpus_name
    if args.corpus_id and args.corpus_name:
        sys.exit("You must either supply a corpus_id or a corpus_name (not both)")
    elif args.corpus_id:
        corpus_id = args.corpus_id
    elif args.corpus_name:
        corpus_name = args.corpus_name

    if corpus_id or corpus_name:
        if args.query:
            query = args.query
        else:
            sys.exit("You must supply a query if you provide a corpus")

    # Check if we're using cache or running real query with vectara-skunk-client
    if query:
        retrieve_response(query, filename, corpus_id=corpus_id,corpus_name=corpus_name)

    # Read Request from local file
    path = Path(filename)
    with open(path, "r") as f:
        response_json = f.read()
        response = json.loads(response_json)

    streamline(response)









