package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum ProjectPermission implements Permission {
    VIEW("project.view"),
    EDIT("project.edit"),
    SHARE("project.share"),
    GENERATE("project.generate"),
    DELETE("project.delete");

    @Getter
    private final String name;
}
