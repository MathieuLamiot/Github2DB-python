from abc import ABCMeta, abstractmethod


class AbstractGithubFlow(object, metaclass=ABCMeta):

    query = None

    def __init__(self):
        self.query = self.build_gql_query()

    @abstractmethod
    def build_gql_query(self):
        raise NotImplementedError

    @abstractmethod
    def has_next_page(self, result):
        raise NotImplementedError

    @abstractmethod
    def get_end_cursor(self, result):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def name():
        raise NotImplementedError

    def execute(self, connector, params):
        results = []
        has_next_page = True

        params["pagination_after"] = "null"

        while has_next_page is True:
            result_page = connector.client.execute(self.query, variable_values=params)
            results.append(result_page)
            has_next_page = self.has_next_page(result_page)
            if has_next_page is True:
                params["pagination_after"] = self.get_end_cursor(result_page)

        return results
