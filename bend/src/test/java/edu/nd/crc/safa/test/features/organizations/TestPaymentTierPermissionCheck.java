package edu.nd.crc.safa.test.features.organizations;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.generation.summary.ProjectSummaryService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestPaymentTierPermissionCheck extends ApplicationBaseTest {

    private final static String projectName = "projectName";
    @MockBean
    private HGenService mockHgenService;
    @MockBean
    private ProjectSummaryService projectSummaryService;
    private ProjectVersion projectVersion;

    @BeforeEach
    public void setup() {

        projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
    }

    @Test
    public void testTierCheckPass() {
        // Test account has UNLIMITED tier by default
        HGenRequest body = new HGenRequest();
        SafaRequest.withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(body);
    }

    @Disabled("Migration to desktop version is turning off billing.")
    @Test
    public void testTierCheckFail() {
        // TODO endpoint to set payment tier
        Organization defaultOrg = serviceProvider.getOrganizationService().getOrganizationById(getCurrentUser().getDefaultOrgId());
        defaultOrg.setPaymentTier(PaymentTier.AS_NEEDED);
        serviceProvider.getOrganizationService().updateOrganization(defaultOrg);

        String typeName = "type";
        String artifactName = "artifact";
        ArtifactVersion artifactVersion =
            dbEntityBuilder.newType(projectName, typeName)
                .newArtifact(projectName, typeName, artifactName)
                .newArtifactBodyWithReturn(projectName, 0, ModificationType.ADDED, artifactName, "summary", "content");

        HGenRequest body = new HGenRequest();
        body.setArtifacts(List.of(artifactVersion.getEntityVersionId()));
        body.setTargetTypes(List.of("newType"));
        JSONObject response = SafaRequest.withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(body, status().is4xxClientError());

        assertThat(response.getString("message")).isNotNull();
        assertThat(response.getString("message").toLowerCase()).contains("additional errors were encountered");

        JSONArray additionalErrors = response.getJSONArray("additionalErrors");
        assertThat(additionalErrors.length()).isEqualTo(1);
        assertThat(additionalErrors.getString(0)).contains("credit balance must be at least");
    }
}
