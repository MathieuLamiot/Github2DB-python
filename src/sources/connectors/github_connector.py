import json

from pathlib import Path
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from sources.flows.projects_from_organization_github_flow import ProjectsFromOrganizationGithubFlow
from sources.flows.project_items_from_project_github_flow import ProjectItemsFromProject
from sources.flows.project_item_update_flow import ProjectItemUpdate


  


class GithubConnector():

    client = None
    flows = []

    def __init__(self):
        # GitHub API endpoint
        url = 'https://api.github.com/graphql'
        # Your GitHub access token from JSON file
        file = open(Path(__file__).parent.parent.parent.parent / "config" / "tokens.json", encoding='utf-8')
        data = json.load(file)
        access_token = data["github_token"]
        # Set up the HTTP transport and add authentication header
        transport = RequestsHTTPTransport(
            url=url, headers={'Authorization': f'Bearer {access_token}'})
        # Create a GraphQL client
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        self.register_all_flows()

    def register_all_flows(self):
        # self.flows.append(ProjectsFromOrganizationGithubFlow())
        # self.flows.append(ProjectItemsFromProject())
        self.flows.append(ProjectItemUpdate())

    def retrieve_data(self, params):
        results = {}
        for flow in self.flows:
            result = flow.execute(self, params[flow.name()])
            results[flow.name()] = result
        return results
