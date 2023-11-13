package edu.nd.crc.safa.test.features.organizations;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.SimplePermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestOrganizationPermissions extends AbstractPermissionViolationTest {

    private Organization organization;

    @BeforeEach
    public void getOrg() {
        organization = serviceProvider.getOrganizationService().getPersonalOrganization(getCurrentUser());
    }

    @Test
    public void testGetOrg() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(organization.getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(OrganizationPermission.VIEW)
        );
    }

    @Test
    public void testCreateOrg() {
        OrganizationAppEntity orgDefinition = new OrganizationAppEntity();
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.ROOT)
                .postWithJsonObject(orgDefinition, status().is4xxClientError()),
            Set.of((SimplePermission) () -> "safa.superuser")
        );
    }

    @Test
    public void testUpdateOrg() {
        OrganizationAppEntity orgDefinition = new OrganizationAppEntity();
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(organization.getId())
                .putWithJsonObject(orgDefinition, status().is4xxClientError()),
            Set.of(OrganizationPermission.EDIT)
        );
    }

    @Test
    public void testDeleteOrg() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(organization.getId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(OrganizationPermission.DELETE)
        );
    }
}
