package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import lombok.Data;

@Data
public class OrganizationAppEntity {
    private UUID id;
    private String name;
    private String description;
    private boolean personalOrg;
    private String paymentTier;
    private List<MembershipAppEntity> members;
    private List<TeamAppEntity> teams;

    public OrganizationAppEntity(Organization organization, List<MembershipAppEntity> members,
                                 List<TeamAppEntity> teams) {
        this.id = organization.getId();
        this.name = organization.getName();
        this.description = organization.getDescription();
        this.personalOrg = organization.isPersonalOrg();
        this.paymentTier = organization.getPaymentTier();
        this.members = members;
        this.teams = teams;
    }
}
