package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.server.entities.db.ProjectVersion;

public interface ArtifactBodyFilter {
    boolean compareTo(ProjectVersion a);
}
