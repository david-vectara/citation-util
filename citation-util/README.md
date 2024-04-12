# Citation Util for Vectara

This is a demonstration on how we can streamline the summary response by reducing the citation numbers to an ordered
list in which they appear. After streamlining the summary, we are left with a summary that is easier to read as well
as an array containing the results to show, in the order they should be cited (starting with an index of 1 rather
than 0)

## To Run

If you want to run using the example response included repository, use the following command:

```python
pip install -r requirements.txt
python retrieve_response.py
```

If you want to generate a summary response from your own corpus, please first configure vectara-skunk-client
using the instructions here https://github.com/davidglevy/vectara-skunk-client

Once done run the following (using either corpus_id or corpus_name):
```python
pip install -r requirements.txt
python retrieve_response.py -c [corpus_id] -C [corpus_name] -q [query]
```

You may also specify a filename to use as a cache or destination to write response to.

