package edu.nd.crc.safa.features.organizations.controllers;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrganizationController extends BaseController {

    private final OrganizationService organizationService;
    private final OrganizationMembershipService organizationMembershipService;

    public OrganizationController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                  OrganizationService organizationService,
                                  OrganizationMembershipService organizationMembershipService) {
        super(resourceBuilder, serviceProvider);
        this.organizationService = organizationService;
        this.organizationMembershipService = organizationMembershipService;
    }

    /**
     * Get all organizations for a given user.
     *
     * @return A list of organizations the user is a part of.
     */
    @GetMapping(AppRoutes.Organizations.ROOT)
    public List<OrganizationAppEntity> getUserOrganizations() {
        ServiceProvider serviceProvider = getServiceProvider();
        SafaUser user = serviceProvider.getSafaUserService().getCurrentUser();

        List<OrganizationMembership> orgMemberships = organizationMembershipService.getAllMembershipsByUser(user);

        return orgMemberships.stream()
            .map(OrganizationMembership::getOrganization)
            .map(org -> organizationService.getAppEntity(org, user))
            .collect(Collectors.toUnmodifiableList());
    }
}
