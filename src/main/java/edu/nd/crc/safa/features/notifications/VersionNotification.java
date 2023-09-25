package edu.nd.crc.safa.features.notifications;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class VersionNotification implements NotificationMessage {
    private final String entityType = "version";
    private ProjectVersion entity;
}
