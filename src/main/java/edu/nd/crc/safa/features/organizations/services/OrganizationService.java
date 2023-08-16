package edu.nd.crc.safa.features.organizations.services;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.repositories.OrganizationRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class OrganizationService {

    private final OrganizationRepository organizationRepo;
    private final TeamService teamService;

    /**
     * Create a new organization. This will also create a new team for the organization.
     *
     * @param name The name of the organization
     * @param owner The owner of the organization
     * @param paymentTier The payment tier of the organization
     * @param personalOrg Whether the organization is a personal organization
     * @return The newly created organization
     */
    public Organization createNewOrganization(String name, SafaUser owner, String paymentTier, boolean personalOrg) {
        Organization organization = new Organization(name, owner, paymentTier, personalOrg);
        organization = organizationRepo.save(organization);  // Save once so it gets an id

        Team orgTeam = teamService.createNewTeam(name, organization, true);
        organization.setFullOrgTeamId(orgTeam.getId());

        return organizationRepo.save(organization);  // Save again to add the team ID
    }

    /**
     * Gets the personal organization representing a given user
     *
     * @param user The user
     * @return The personal org for that user
     */
    public Organization getPersonalOrganization(SafaUser user) {
        UUID orgId = user.getPersonalOrgId();
        return organizationRepo.findById(orgId)
                .orElseThrow(() -> new SafaError("User does not have a personal organization"));
    }
}
