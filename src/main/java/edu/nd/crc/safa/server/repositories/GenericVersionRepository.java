package edu.nd.crc.safa.server.repositories;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.IEntityVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * Implements the generic logic for retrieving, creating, and modifying versioned entities.
 *
 * @param <T> The versioned entity.
 */
public abstract class GenericVersionRepository<T extends IEntityVersion> implements IVersionRepository<T> {

    @Override
    public List<T> retrieveEntitiesAtProjectVersion(
        ProjectVersion projectVersion,
        Hashtable<String, List<T>> artifactBodiesByArtifactName) {
        List<T> artifacts = new ArrayList<>();
        for (String key : artifactBodiesByArtifactName.keySet()) {
            List<T> bodyVersions = artifactBodiesByArtifactName.get(key);
            T latest = null;
            for (T body : bodyVersions) {
                if (body.getProjectVersion().isLessThanOrEqualTo(projectVersion)) {
                    if (latest == null || body.getProjectVersion().isGreaterThan(latest.getProjectVersion())) {
                        latest = body;
                    }
                }
            }

            if (latest != null && latest.getModificationType() != ModificationType.REMOVED) {
                artifacts.add(latest);
            }
        }
        return artifacts;
    }
}
