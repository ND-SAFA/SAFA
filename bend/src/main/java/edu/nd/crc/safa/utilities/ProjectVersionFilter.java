package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Defines an interface for a lambda that is used to filter through a list of project versions.
 */
public interface ProjectVersionFilter {
    boolean shouldKeep(ProjectVersion a);
}
