package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum OrganizationPermission implements Permission {
    CREATE_TEAMS("org.create_teams"),
    DELETE("org.delete"),
    DELETE_TEAMS("org.delete_teams"),
    EDIT("org.edit"),
    EDIT_MEMBERS("org.edit_members"),
    VIEW("org.view"),
    VIEW_BILLING("org.view_billing"),
    VIEW_TEAMS("org.view_teams");

    @Getter
    private final String name;
}
