PROMPT_FOR_QUERY_DECOMPOSITION = '''
You are a multilingual web search assistant.
Your task is to extract the most important keywords or phrases from the user's query and generate a more concise and precise search query.
Remove unnecessary words and simplify complex sentences.
If you extract multiple keywords or phrases, separate them with commas.
Ensure that the output query is in the same language as the user's input.

The user's input query is: {query}

Based on this input, generate a better search query in the same language, separating multiple keywords or phrases with commas:
'''.strip()

PROMPT_FOR_QUERY_TRANSLATION = '''
You are a language translation assistant.
Your task is to convert the user's query into the specified language.
Make sure to maintain the original meaning while ensuring that the translation is accurate and natural in the target language.

The user's input query is: {query}

Please translate this query into {target_language}:
'''.strip()

class QueryCurator:

    def __init__(self, engine=None):
        self.engine = engine


    def decompose(
        self,
        query,
        *,
        engine=None,
        model:str=None,
        return_raw:bool=False,
        **chat_params
    ):

        assert engine or self.engine, "The inference engine was neither specified nor initialized."
        engine = engine or self.engine

        prompt = PROMPT_FOR_QUERY_DECOMPOSITION.format(query=query)
        messages = [{"role": "user", "content": prompt}]

        response = engine.chat_completions(
            messages=messages,
            model=model or engine.model,
            **chat_params
        )

        if return_raw:
            return response
        response = response.choices[0].message.content.split(',')
        response = [value.strip() for value in response]
        return response


    def translate(
        self,
        query,
        target_language:str='en',
        *,
        engine=None,
        model:str=None,
        return_raw:bool=False,
        **chat_params
    ):

        assert engine or self.engine, "The inference engine was neither specified nor initialized."
        engine = engine or self.engine

        prompt = PROMPT_FOR_QUERY_TRANSLATION.format(query=query, target_language=target_language)
        messages = [{"role": "user", "content": prompt}]

        response = engine.chat_completions(
            messages=messages,
            model=model or engine.model,
            **chat_params
        )
        if return_raw:
            return response
        return response.choices[0].message.content