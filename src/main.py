"""
    Main script.
"""
import json
import logging
from logger import log_manager
from sources.connectors.github_connector import GithubConnector
from sources.flows.projects_from_organization_github_flow import ProjectsFromOrganizationGithubFlow
from sources.flows.project_items_from_project_github_flow import ProjectItemsFromProject
from sources.flows.project_item_update_flow import ProjectItemUpdate

# --- LOGGING ---
log_manager.setup_logger(False)
logger = logging.getLogger(__name__)
logger.info('Logger available.')
# --- END OF: LOGGING ---

# # Execute the query
params_1 = {"org": "wp-media", "pagination_last": 100}
params_2 = {"node_id": "PVT_kwDOAMEyYM4ASOQZ", "pagination_first": 100, "pagination_after": "null"}
params_3 = {"node_id": "PVTI_lADOAMEyYM4ASOQZzgHy5wQ", "pagination_first": 100, "pagination_after": "null"}
params = {}
params[ProjectsFromOrganizationGithubFlow.name()] = params_1
params[ProjectItemsFromProject.name()] = params_2
params[ProjectItemUpdate.name()] = params_3

source = GithubConnector()
results = source.retrieve_data(params)
json_formatted_str = json.dumps(results, indent=2)
print(json_formatted_str)
