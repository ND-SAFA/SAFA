package edu.nd.crc.safa.utilities;

import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;

public interface ArtifactBodyFilter {
    boolean compareTo(ProjectVersion a);
}
