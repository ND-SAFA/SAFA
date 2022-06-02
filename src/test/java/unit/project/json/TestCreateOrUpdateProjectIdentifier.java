package unit.project.json;

import java.util.UUID;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that user is able to create and update a project idenfier via JSON.
 */
public class TestCreateOrUpdateProjectIdentifier extends BaseProjectJsonTest {


    /**
     * Tests that a new project identifier can be created with given
     * name and description.
     */
    @Test
    public void createProjectIdentifier() throws Exception {
        // Step - Create JSON
        JSONObject projectJson = createBaseProjectJson();

        // Step - POST to create project
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getString("projectId");

        // VP - Verify that information was saved.
        verifyProjectInformation(UUID.fromString(projectId), projectName, projectDescription);
    }

    /**
     * Tests that project identifier can be updated with new name and description.
     */
    @Test
    public void updateProjectIdentifier() throws Exception {
        String newName = "new-project-name";
        String newDescription = "new-description";

        // Step - Create JSON
        JSONObject projectJson = jsonBuilder
            .withProject("", projectName, projectDescription)
            .getProjectJson(projectName);

        // Step - POST to create project
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent.getString("projectId");

        // Step - POST to update project
        responseContent.put("name", newName);
        responseContent.put("description", newDescription);
        postProjectJson(responseContent);

        // VP - Verify that information was saved.
        verifyProjectInformation(UUID.fromString(projectId), newName, newDescription);
    }
}
