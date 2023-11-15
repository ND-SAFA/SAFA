package edu.nd.crc.safa.features.permissions.entities;

import java.util.Set;

import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.NoAdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PaymentTierCheck;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ProjectPermission implements Permission {
    DELETE("project.delete", new NoAdditionalPermissionCheck()),
    EDIT("project.edit", new NoAdditionalPermissionCheck()),
    EDIT_DATA("project.edit_data", new NoAdditionalPermissionCheck()),
    EDIT_INTEGRATIONS("project.edit_integrations", new NoAdditionalPermissionCheck()),
    EDIT_MEMBERS("project.edit_members", new NoAdditionalPermissionCheck()),
    EDIT_VERSIONS("project.edit_versions", new NoAdditionalPermissionCheck()),
    GENERATE("project.generate", new PaymentTierCheck(Set.of(PaymentTier.RECURRING, PaymentTier.UNLIMITED))),
    VIEW("project.view", new NoAdditionalPermissionCheck());

    private final String name;

    private final AdditionalPermissionCheck additionalCheck;
}
