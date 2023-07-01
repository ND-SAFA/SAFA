package edu.nd.crc.safa.test.features.attributes.crud;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestReservedAttributes extends ApplicationBaseTest {

    private static final String key = "~shouldBeReserved";
    private static final String label = "Reserved";

    @Test
    public void testCreatingReservedAttributeFails() throws Exception {
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);
        CustomAttributeAppEntity appEntity = new CustomAttributeAppEntity(key, label, CustomAttributeType.TEXT);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Attribute.ROOT)
            .withProject(project)
            .postWithJsonObject(appEntity, status().is4xxClientError());

        assertEquals("Key is reserved for internal use", response.getString("message"));
    }

    @Test
    public void testModifyingReservedAttributeFails() throws Exception {
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);
        CustomAttributeAppEntity appEntity = new CustomAttributeAppEntity(key, label, CustomAttributeType.TEXT);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Attribute.BY_KEY)
            .withProject(project)
            .withKey(key)
            .putWithJsonObject(appEntity, status().is4xxClientError());

        assertEquals("Cannot modify reserved attribute", response.getString("message"));
    }

    @Test
    public void testDeletingReservedAttributeFails() throws Exception {
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Attribute.BY_KEY)
            .withProject(project)
            .withKey(key)
            .deleteWithJsonObject(status().is4xxClientError());

        assertEquals("Cannot delete reserved attribute", response.getString("message"));
    }
}
