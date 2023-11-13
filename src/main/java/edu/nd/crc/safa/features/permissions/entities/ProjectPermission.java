package edu.nd.crc.safa.features.permissions.entities;

import java.util.List;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ProjectPermission implements Permission {
    DELETE("project.delete", List.of()),
    EDIT("project.edit", List.of()),
    EDIT_DATA("project.edit_data", List.of()),
    EDIT_INTEGRATIONS("project.edit_integrations", List.of()),
    EDIT_MEMBERS("project.edit_members", List.of()),
    EDIT_VERSIONS("project.edit_versions", List.of()),
    GENERATE("project.generate", List.of()),
    VIEW("project.view", List.of());

    private final String name;

    private final List<AdditionalPermissionCheck> additionalChecks;
}
