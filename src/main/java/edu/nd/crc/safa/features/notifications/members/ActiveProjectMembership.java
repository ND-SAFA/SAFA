package edu.nd.crc.safa.features.notifications.members;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.IUser;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Holds a record of an active user on a project.
 */
@AllArgsConstructor
@Data
public class ActiveProjectMembership {
    private final IUser user;
    private final UUID projectId;
}
