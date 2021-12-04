package edu.nd.crc.safa.server.repositories.impl;

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


    /**
     * Calculates contents of each artifact at given version and returns bodies at version.
     *
     * @param projectVersion - The version of the artifact bodies that are returned
     * @return list of artifact bodies in project at given version
     */
    @Override
    public List<T> getEntitiesAtVersion(ProjectVersion projectVersion) {
        Hashtable<String, List<T>> artifactBodyTable =
            this.groupEntityVersionsByEntityId(projectVersion);
        return this.retrieveEntitiesAtProjectVersion(projectVersion, artifactBodyTable);
    }

    private List<T> retrieveEntitiesAtProjectVersion(
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

    private Hashtable<String, List<T>> groupEntityVersionsByEntityId(ProjectVersion projectVersion) {
        Hashtable<String, List<T>> entityHashtable = new Hashtable<>();
        List<T> entityVersions = this.getEntitiesInProject(projectVersion.getProject());
        for (T entityVersion : entityVersions) {
            String entityId = entityVersion.getEntityId();
            if (entityHashtable.containsKey(entityId)) {
                entityHashtable.get(entityId).add(entityVersion);
            } else {
                List<T> newList = new ArrayList<>();
                newList.add(entityVersion);
                entityHashtable.put(entityId, newList);
            }
        }
        return entityHashtable;
    }
}
