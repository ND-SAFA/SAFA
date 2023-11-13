package edu.nd.crc.safa.test.features.users.crud;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestDefaultOrg extends ApplicationBaseTest {

    @Autowired
    private SafaUserService safaUserService;

    @Test
    void testDefaultOrgDefaultValue() throws Exception {
        OrganizationAppEntity personalOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.SELF)
                .getAsType(new TypeReference<>() {
                });

        assertThat(getCurrentUser().getDefaultOrgId()).isEqualTo(personalOrg.getId());
    }

    @Test
    void testUpdateDefaultOrg() throws Exception {
        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser();

        OrganizationAppEntity newOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.ROOT)
                .postAndParseResponse(new OrganizationAppEntity("org name", "org desc"), new TypeReference<>() {
                });

        SafaRequest.withRoute(AppRoutes.Accounts.DEFAULT_ORG)
            .putWithJsonObject(new DefaultOrgDTO(newOrg.getId()));

        SafaUser updatedUser = safaUserService.getUserById(getCurrentUser().getUserId());
        assertThat(updatedUser.getDefaultOrgId()).isEqualTo(newOrg.getId());
    }

    @Test
    void testSetDefaultOrgWithBadId() throws Exception {
        SafaRequest.withRoute(AppRoutes.Accounts.DEFAULT_ORG)
            .putWithJsonObject(
                new DefaultOrgDTO(UUID.randomUUID()),
                status().is4xxClientError()
            );
    }

    @Data
    @AllArgsConstructor
    private static class DefaultOrgDTO {
        private UUID defaultOrgId;
    }
}
