package edu.nd.crc.safa.features.jira.entities.api;

import java.util.UUID;

import lombok.Data;

@Data
public class JiraImportSettings {
    private UUID teamId;
    private UUID orgId;
}
