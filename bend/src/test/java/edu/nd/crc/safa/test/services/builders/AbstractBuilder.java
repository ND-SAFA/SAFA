package edu.nd.crc.safa.test.services.builders;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;

public abstract class AbstractBuilder {

    public abstract void initializeData() throws IOException;

    protected <T, K> void addEntry(Map<String, Map<K, T>> table,
                                   String projectName,
                                   K entityIndex,
                                   T newEntity) {
        if (table.containsKey(projectName)) {
            table.get(projectName).put(entityIndex, newEntity);
        } else {
            Map<K, T> newTable = new HashMap<>();
            newTable.put(entityIndex, newEntity);
            table.put(projectName, newTable);
        }
    }

    protected <T> void addEntry(Map<String, Map<Integer, T>> table,
                                String projectName,
                                T newEntity) {
        if (table.containsKey(projectName)) {
            int entityIndex = table.get(projectName).size();
            table.get(projectName).put(entityIndex, newEntity);
        } else {
            Map<Integer, T> newTable = new HashMap<>();
            newTable.put(0, newEntity);
            table.put(projectName, newTable);
        }
    }

    protected void addArtifactBody(Map<String, Map<String, Map<Long, ArtifactVersion>>> table,
                                   String projectName,
                                   String artifactName,
                                   int versionIndex,
                                   ArtifactVersion body) {
        if (table.containsKey(projectName)) {
            Map<String, Map<Long, ArtifactVersion>> projectTable = table.get(projectName);
            if (projectTable.containsKey(artifactName)) {
                projectTable.get(artifactName).put((long) versionIndex, body);
            } else {
                Map<Long, ArtifactVersion> versionTable = new HashMap<>();
                versionTable.put((long) versionIndex, body);
                projectTable.put(artifactName, versionTable);
            }
        } else {
            Map<String, Map<Long, ArtifactVersion>> projectTable = new HashMap<>();
            table.put(projectName, projectTable);
            addArtifactBody(table, projectName, artifactName, versionIndex, body);
        }
    }
}
