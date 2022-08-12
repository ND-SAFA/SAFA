package edu.nd.crc.safa.features.notifications.messages;

import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Container for the versioned entity to update
 * along with the initiator.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class VersionMessage {

    String user;
    VersionEntityTypes type;
}
