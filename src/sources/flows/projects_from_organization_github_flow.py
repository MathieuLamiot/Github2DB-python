from gql import gql
from sources.flows.abstract_github_flow import AbstractGithubFlow


class ProjectsFromOrganizationGithubFlow(AbstractGithubFlow):

    def build_gql_query(self):
        query = gql("""
                    query GetProjectsFromOrganization ($org: String!, $pagination_last: Int!) {
                        organization(login: $org){
                            projectsV2(last: $pagination_last) {
                                pageInfo {
                                    endCursor
                                    hasNextPage
                                }
                                nodes {
                                    id, title, closed
                                }
                            }
                        }
                        }
                    """)
        return query

    def has_next_page(self, result):
        return result["organization"]["projectsV2"]["pageInfo"]["hasNextPage"]

    def get_end_cursor(self, result):
        return result["organization"]["projectsV2"]["pageInfo"]["endCursor"]

    @staticmethod
    def name():
        return "ProjectsFromOrganization"
