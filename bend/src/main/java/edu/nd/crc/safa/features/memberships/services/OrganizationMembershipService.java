package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.repositories.OrganizationMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class OrganizationMembershipService implements IMembershipService {

    private final OrganizationMembershipRepository orgMembershipRepo;

    /**
     * {@inheritDoc}
     */
    @Override
    public OrganizationMembership addUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Organization;
        assert iRole instanceof OrganizationRole;
        Organization organization = (Organization) entity;
        OrganizationRole role = (OrganizationRole) iRole;

        Optional<OrganizationMembership> membershipOptional =
                orgMembershipRepo.findByUserAndOrganizationAndRole(user, organization, role);

        return membershipOptional.orElseGet(() -> {
            OrganizationMembership newMembership = new OrganizationMembership(user, organization, role);
            return orgMembershipRepo.save(newMembership);
        });
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void removeUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Organization;
        assert iRole instanceof OrganizationRole;
        Organization organization = (Organization) entity;
        OrganizationRole role = (OrganizationRole) iRole;

        Optional<OrganizationMembership> membershipOptional =
                orgMembershipRepo.findByUserAndOrganizationAndRole(user, organization, role);

        membershipOptional.ifPresent(orgMembershipRepo::delete);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IRole> getRolesForUser(SafaUser user, IEntityWithMembership entity) {
        assert entity instanceof Organization;
        Organization organization = (Organization) entity;
        return orgMembershipRepo.findByUserAndOrganization(user, organization).stream()
                .map(OrganizationMembership::getRole)
                .collect(Collectors.toUnmodifiableList());
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public Optional<IEntityMembership> getMembershipOptionalById(UUID membershipId) {
        // The map call forces it to understand that the type is indeed correct
        return orgMembershipRepo.findById(membershipId).map(m -> m);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForUser(SafaUser user) {
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(getOrganizationMembershipsForUser(user));
    }

    /**
     * Get the list of organization memberships for the given user. This function differs
     * from {@link #getMembershipsForUser(SafaUser)} in that it specifically returns a list of
     * {@link OrganizationMembership} objects.
     *
     * @param user The user
     * @return The memberships for this user
     */
    public List<OrganizationMembership> getOrganizationMembershipsForUser(SafaUser user) {
        return orgMembershipRepo.findByUser(user);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForEntity(IEntityWithMembership entity) {
        assert entity instanceof Organization;
        Organization organization = (Organization) entity;
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(orgMembershipRepo.findByOrganization(organization));
    }
}
