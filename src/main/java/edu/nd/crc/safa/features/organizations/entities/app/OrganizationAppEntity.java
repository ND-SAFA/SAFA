package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class OrganizationAppEntity {
    private UUID id;
    private String name;
    private String description;
    private boolean personalOrg;
    private String paymentTier;
    private List<MembershipAppEntity> members;
    private List<TeamAppEntity> teams;
    private List<String> permissions;

    /**
     * This constructor sets the fields that are read by our creation/modification endpoints.
     * It should only be used for testing
     *
     * @param name The name of the org
     * @param description The org description
     */
    public OrganizationAppEntity(String name, String description) {
        this.name = name;
        this.description = description;
    }

    public OrganizationAppEntity(Organization organization, List<MembershipAppEntity> members,
                                 List<TeamAppEntity> teams, List<String> permissions) {
        this.id = organization.getId();
        this.name = organization.getName();
        this.description = organization.getDescription();
        this.personalOrg = organization.isPersonalOrg();
        this.paymentTier = organization.getPaymentTier();
        this.members = members;
        this.teams = teams;
        this.permissions = permissions;
    }
}
