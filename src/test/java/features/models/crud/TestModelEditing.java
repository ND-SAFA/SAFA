package features.models.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.fail;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.ObjectMapper;
import common.ApplicationBaseTest;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import requests.SafaRequest;

public class TestModelEditing extends ApplicationBaseTest {

    @Autowired
    private ObjectMapper jacksonObjectMapper;

    private Project project;
    private ModelAppEntity model;

    @BeforeEach
    public void setup() {
        ProjectVersion pv = creationService.createProjectWithNewVersion("projectName");
        project = pv.getProject();

        model = new ModelAppEntity();
        model.setName("testName");
        model.setBaseModel(BaseGenerationModels.NLBert);
        model = serviceProvider.getModelService().createOrUpdateModel(project, model);
    }

    @Test
    public void verifyNameIsEditable() throws Exception {
        ModelAppEntity editedModel = new ModelAppEntity();
        editedModel.setName("newName");

        JSONObject response = SafaRequest
                .withRoute(AppRoutes.Models.MODEL_BY_ID)
                .withProject(project)
                .withModelId(model.getId())
                .putWithJsonObject(editedModel, status().is2xxSuccessful());

        ModelAppEntity returnedModel = jacksonObjectMapper.readValue(response.toString(), ModelAppEntity.class);
        assertThat(returnedModel.getName()).isEqualTo(editedModel.getName());

        Model updatedModelInDb = serviceProvider.getModelService().getModelById(model.getId());
        assertThat(updatedModelInDb).isNotNull();
        assertThat(updatedModelInDb.getName()).isEqualTo(editedModel.getName());
    }

    @Test
    public void verifyIdIsNotEditable() throws Exception {
        ModelAppEntity editedModel = new ModelAppEntity();
        editedModel.setId(UUID.randomUUID());

        SafaRequest
                .withRoute(AppRoutes.Models.MODEL_BY_ID)
                .withProject(project)
                .withModelId(model.getId())
                .putWithJsonObject(editedModel, status().is4xxClientError());

        Model updatedModelInDb = serviceProvider.getModelService().getModelById(model.getId());
        assertThat(updatedModelInDb).isNotNull();
        assertThat(updatedModelInDb.getId()).isEqualTo(model.getId());

        try {
            serviceProvider.getModelService().getModelById(editedModel.getId());
            fail("getModelById should have thrown an exception");
        } catch (SafaError ignored) {

        }
    }

    @Test
    public void verifyBaseModelIsNotEditable() throws Exception {
        ModelAppEntity editedModel = new ModelAppEntity();
        editedModel.setBaseModel(BaseGenerationModels.VSM);

        SafaRequest
                .withRoute(AppRoutes.Models.MODEL_BY_ID)
                .withProject(project)
                .withModelId(model.getId())
                .putWithJsonObject(editedModel, status().is4xxClientError());

        Model updatedModelInDb = serviceProvider.getModelService().getModelById(model.getId());
        assertThat(updatedModelInDb).isNotNull();
        assertThat(updatedModelInDb.getBaseModel()).isEqualTo(model.getBaseModel());

    }
}
