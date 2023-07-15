from gql import gql
from sources.flows.abstract_github_flow import AbstractGithubFlow


class ProjectItemUpdate(AbstractGithubFlow):

    def build_gql_query(self):
        query = gql("""
                    query GetProjectItem ($node_id: ID!) {
                        node(id: $node_id) {
                        ... on ProjectV2Item {
                            id
                            createdAt
                            creator {
                                login
                            }
                            isArchived
                            project {
                                title
                            }
                            type
                            updatedAt
                            content{
                                ... on DraftIssue {
                                    title
                                }
                                ...on Issue {
                                    title
                                    number
                                    labels(first: 20) {
                                        nodes {
                                            name
                                        }
                                    }
                                }
                                ...on PullRequest {
                                    title
                                    number
                                    labels(first: 20) {
                                        nodes {
                                            name
                                        }
                                    }
                                }
                            }
                            fieldValues(first: 20) {
                                nodes {
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
                                    users(first: 1) {
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
                                    ... on ProjectV2ItemFieldLabelValue {
                                    labels(first: 20) {
                                        nodes {
                                        name
                                        }
                                    }
                                    field {
                                        ... on ProjectV2FieldCommon {
                                        name
                                        }
                                    }
                                    }
                                    ... on ProjectV2ItemFieldPullRequestValue {
                                    pullRequests(first: 1) {
                                        nodes {
                                            number
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
                """)
        return query

    def has_next_page(self, result):
        return False

    def get_end_cursor(self, result):
        return None

    @staticmethod
    def name():
        return "ProjectItemUpdate"
