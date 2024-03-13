package edu.nd.crc.safa.test.features.organizations;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
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
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestPaymentTierPermissionCheck extends ApplicationBaseTest {

    @MockBean
    private HGenService mockHgenService;

    @MockBean
    private ProjectSummaryService projectSummaryService;

    private ProjectVersion projectVersion;

    @BeforeEach
    public void setup() {
        projectVersion = rootBuilder.getActionBuilder().createProjectWithVersion(getCurrentUser());
    }

    @Test
    public void testTierCheckPass() {
        // Test account has UNLIMITED tier by default
        HGenRequest body = new HGenRequest();
        SafaRequest.withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(body);
    }

    @Test
    public void testTierCheckFail() {
        // TODO endpoint to set payment tier
        Organization defaultOrg = serviceProvider.getOrganizationService().getOrganizationById(getCurrentUser().getDefaultOrgId());
        defaultOrg.setPaymentTier(PaymentTier.AS_NEEDED);
        serviceProvider.getOrganizationService().updateOrganization(defaultOrg);

        HGenRequest body = new HGenRequest();
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
