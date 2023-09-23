package edu.nd.crc.safa.features.memberships.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.repositories.OrganizationMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class OrganizationMembershipService {

    private final OrganizationMembershipRepository orgMembershipRepo;

    /**
     * Applies a role to a user within an organization. If the user already has this
     * role in this organization, this function does nothing.
     *
     * @param user         The user to get the new role
     * @param organization The organization the role applies to
     * @param role         The role
     * @return The new membership, or the existing membership if the user already had that role
     */
    public OrganizationMembership addUserRole(SafaUser user, Organization organization, OrganizationRole role) {
        Optional<OrganizationMembership> membershipOptional =
                orgMembershipRepo.findByUserAndOrganizationAndRole(user, organization, role);

        return membershipOptional.orElseGet(() -> {
            OrganizationMembership newMembership = new OrganizationMembership(user, organization, role);
            return orgMembershipRepo.save(newMembership);
        });
    }

    /**
     * Removes a role from a user within an organization. If the user didn't already have this
     * role in this organization, this function does nothing.
     *
     * @param user The user to remove the role from
     * @param organization The organization the role applies to
     * @param role The role
     */
    public void removeUserRole(SafaUser user, Organization organization, OrganizationRole role) {
        Optional<OrganizationMembership> membershipOptional =
                orgMembershipRepo.findByUserAndOrganizationAndRole(user, organization, role);

        membershipOptional.ifPresent(orgMembershipRepo::delete);
    }

    /**
     * Get the list of roles the user has within the organization.
     *
     * @param user The user in question
     * @param organization The organization to check within
     * @return The roles the user has in that organization
     */
    public List<OrganizationRole> getUserRoles(SafaUser user, Organization organization) {
        return orgMembershipRepo.findByUserAndOrganization(user, organization).stream()
                .map(OrganizationMembership::getRole)
                .collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get all organization memberships for a given user.
     *
     * @param user The user
     * @return A list of memberships for that user. Note that the same organization may appear
     *         multiple times in this list if the user has multiple roles within that organization.
     */
    public List<OrganizationMembership> getAllMembershipsByUser(SafaUser user) {
        return orgMembershipRepo.findByUser(user);
    }

    /**
     * Get all user memberships for a given organization.
     *
     * @param organization The organization
     * @return A list of memberships for that organization. Note that the same user may
     *         appear multiple times in this list if they have multiple roles within this organization.
     */
    public List<OrganizationMembership> getAllMembershipsByOrganization(Organization organization) {
        return orgMembershipRepo.findByOrganization(organization);
    }
}
