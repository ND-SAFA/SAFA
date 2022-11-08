package features.models.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.ObjectMapper;
import common.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultMatcher;
import requests.SafaRequest;

public class TestModelEditing extends ApplicationBaseTest {

    @Autowired
    private ObjectMapper jacksonObjectMapper;

    /**
     * Test for
     * {@link edu.nd.crc.safa.features.models.controllers.ModelController#editModelById(UUID, UUID, ModelAppEntity)}
     * 
     * @throws Exception On error
     */
    @Test
    public void testModelEdit() throws Exception {
        // Test values
        String testNameBefore = "testNameBefore";
        String testNameAfter = "testNameAfter";
        BaseGenerationModels baseModelBefore = BaseGenerationModels.NLBert;
        BaseGenerationModels baseModelAfter = BaseGenerationModels.VSM;

        // Create project and model
        ProjectVersion pv = creationService.createProjectWithNewVersion("projectName");
        Project project = pv.getProject();

        ModelAppEntity model = new ModelAppEntity();
        model.setName(testNameBefore);
        model.setBaseModel(baseModelBefore);
        model = serviceProvider.getModelService().createOrUpdateModel(project, model);
        UUID uuidBefore = model.getId();

        // Update all fields in model entity
        ModelAppEntity editedModel = new ModelAppEntity();
        editedModel.setName(testNameAfter);
        editedModel.setBaseModel(baseModelAfter);
        editedModel.setId(UUID.randomUUID());

        // Create matcher to assert that the request is successful and returns the updated model
        // with only the allowed fields updated
        ResultMatcher matcher = (MvcResult result) -> {
            HttpStatus status = HttpStatus.resolve(result.getResponse().getStatus());
            assertThat(status).isNotNull();
            assertThat(status.is2xxSuccessful()).isTrue();

            String body = result.getResponse().getContentAsString();
            assertThat(result.getResponse().getContentType()).isEqualTo("application/json");
            assertThat(body).isNotEmpty();

            ModelAppEntity returnedModel = jacksonObjectMapper.readValue(body, ModelAppEntity.class);
            assertThat(returnedModel.getName()).isEqualTo(testNameAfter);
            assertThat(returnedModel.getBaseModel()).isEqualTo(baseModelBefore);
            assertThat(returnedModel.getId()).isEqualTo(uuidBefore);
        };

        // Send request
        SafaRequest
                .withRoute(AppRoutes.Models.MODEL_BY_ID)
                .withProject(project)
                .withModelId(model.getId())
                .putWithJsonObject(editedModel, matcher);

        // Check that DB is updated
        Model updatedModelInDb = serviceProvider.getModelService().getModelById(uuidBefore);
        assertThat(updatedModelInDb).isNotNull();
        assertThat(updatedModelInDb.getName()).isEqualTo(testNameAfter);
        assertThat(updatedModelInDb.getBaseModel()).isEqualTo(baseModelBefore);
        assertThat(updatedModelInDb.getId()).isEqualTo(uuidBefore);
    }
}
