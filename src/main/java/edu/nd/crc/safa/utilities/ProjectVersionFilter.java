package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * Defines an interface for a lambda that is used to filter through a list of project versions.
 */
public interface ProjectVersionFilter {
    boolean shouldKeep(ProjectVersion a);
}
