from gql import gql
from sources.flows.abstract_github_flow import AbstractGithubFlow


class ProjectItemsFromProject(AbstractGithubFlow):

    def build_gql_query(self):
        query = gql("""
                    query GetItemsFromProject ($node_id: ID!, $pagination_first: Int!, $pagination_after: String!) {
                        node(id: $node_id) {
                        ... on ProjectV2 {
                            __typename
                            items(first: $pagination_first, after: $pagination_after) {
                                pageInfo {
                                    endCursor
                                    hasNextPage
                                }
                                nodes {
                                    id
                                    content{
                                        __typename
                                        ... on DraftIssue {
                                            title
                                        }
                                        ...on Issue {
                                            title
                                            number
                                        }
                                        ...on PullRequest {
                                            title
                                            number
                                        }
                                    }
                                    fieldValues(first: 20) {
                                        nodes {
                                            __typename,
                                            ... on ProjectV2ItemFieldTextValue {
                                            text
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldNumberValue {
                                            number
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldDateValue {
                                            date
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldIterationValue {
                                            title
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldSingleSelectValue {
                                            name
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldMilestoneValue {
                                            milestone {
                                                title
                                            }
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldRepositoryValue {
                                            repository {
                                                name
                                            }
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                            ... on ProjectV2ItemFieldUserValue {
                                            users(first: 10) {
                                                nodes {
                                                login
                                                }
                                            }
                                            field {
                                                ... on ProjectV2FieldCommon {
                                                name
                                                }
                                            }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        }
                    }
                """)
        return query

    def has_next_page(self, result):
        return result["node"]["items"]["pageInfo"]["hasNextPage"]

    def get_end_cursor(self, result):
        return result["node"]["items"]["pageInfo"]["endCursor"]

    @staticmethod
    def name():
        return "ProjectItemsFromProject"
