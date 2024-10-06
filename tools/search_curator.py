from dataclasses import dataclass
from googlesearch import search

@dataclass
class Response:
    href:str
    query_by:list

class SearchCurator:

    def deduplicate_by_href(responses: list[Response]):
        dedeplicated_responses:dict = {}

        for response in responses:
            href = response.href

            if href in dedeplicated_responses.keys():
                dedeplicated_responses[href].query_by.extend(response.query_by)
            else:
                dedeplicated_responses[href] = response
        return dedeplicated_responses

    @classmethod
    def search(
        cls,
        queries:str | list[str],
        per_query_max_results:int=5,
        deduplicate_by_href:bool=True,
    ):
        if isinstance(queries, str):
            queries = [queries]

        responses = [
            Response(href=response, query_by=[query])
            for query in queries for response in search(query, num_results=per_query_max_results)
        ]

        if deduplicate_by_href:
            responses = cls.deduplicate_by_href(responses)

        responses = [response.__dict__ for response in responses]
        return responses