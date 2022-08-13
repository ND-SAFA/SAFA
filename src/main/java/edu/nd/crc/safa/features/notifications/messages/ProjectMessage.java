package edu.nd.crc.safa.features.notifications.messages;

import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * WebSocket message alerting clients that some entity was changed.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProjectMessage {
    /**
     * User initiating update of entity below.
     */
    String user;
    /**
     * The entity that was changed.
     */
    ProjectEntityTypes type;
}
