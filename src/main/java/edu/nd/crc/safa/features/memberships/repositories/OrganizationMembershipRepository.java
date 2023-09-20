package edu.nd.crc.safa.features.memberships.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;

public interface OrganizationMembershipRepository extends CrudRepository<OrganizationMembership, UUID> {
    List<OrganizationMembership> findByUserAndOrganization(SafaUser user, Organization organization);

    Optional<OrganizationMembership> findByUserAndOrganizationAndRole(SafaUser user, Organization organization, OrganizationRole role);

    List<OrganizationMembership> findByUser(SafaUser user);

    List<OrganizationMembership> findByOrganization(Organization organization);
}
