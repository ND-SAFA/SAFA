package edu.nd.crc.safa.features.permissions.entities;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.config.MaxProjectSizeCheck;
import edu.nd.crc.safa.features.permissions.checks.utility.NoAdditionalPermissionCheck;

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
    GENERATE("project.generate", new MaxProjectSizeCheck()),
    MOVE("project.move", new NoAdditionalPermissionCheck()),
    VIEW("project.view", new NoAdditionalPermissionCheck());

    private final String name;
    private final AdditionalPermissionCheck additionalCheck;
}
