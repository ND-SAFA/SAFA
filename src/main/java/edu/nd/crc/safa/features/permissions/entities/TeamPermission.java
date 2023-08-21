package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum TeamPermission implements Permission {
    VIEW("team.view"),
    EDIT("team.edit"),
    EDIT_MEMBERS("team.edit_members"),
    DELETE("team.delete"),
    VIEW_PROJECTS("team.view_projects"),
    CREATE_PROJECTS("team.create_projects"),
    DELETE_PROJECTS("team.delete_projects");

    @Getter
    private final String name;
}
