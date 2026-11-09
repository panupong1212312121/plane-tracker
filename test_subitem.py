import os
os.environ['PLANE_API_KEY'] = 'plane_api_753422726aad47afb951dc6cd3a7ceb4'
os.environ['PLANE_WORKSPACE_SLUG'] = 'panupong'

from plane_mcp.client import get_plane_client_context
from plane.models.work_items import CreateWorkItem

client, workspace_slug = get_plane_client_context()
project_id = '6c496f89-d85a-4744-a685-3bc17d4bc4b2' # Panupong project

# Create parent
parent = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_id,
    data=CreateWorkItem(
        name="Test Parent Work Item",
        description_stripped="Testing parent work item"
    )
)
print("Parent created:", parent.id, parent.name)

# Create child
child = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_id,
    data=CreateWorkItem(
        name="Test Sub Item 1",
        parent=parent.id,
        description_stripped="Testing sub item 1"
    )
)
print("Child created:", child.id, child.name, "parent:", child.parent)

# Clean up
client.work_items.delete(workspace_slug=workspace_slug, project_id=project_id, work_item_id=child.id)
client.work_items.delete(workspace_slug=workspace_slug, project_id=project_id, work_item_id=parent.id)
print("Cleaned up successfully!")
