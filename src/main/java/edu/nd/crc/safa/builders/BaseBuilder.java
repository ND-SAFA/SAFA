package edu.nd.crc.safa.builders;

import java.util.Hashtable;

import edu.nd.crc.safa.db.entities.sql.ArtifactBody;

public abstract class BaseBuilder {

    abstract public void createEmptyData();

    protected <T, K> void addEntry(Hashtable<String, Hashtable<K, T>> table,
                                   String projectName,
                                   K entityIndex,
                                   T newEntity) {
        if (table.containsKey(projectName)) {
            table.get(projectName).put(entityIndex, newEntity);
        } else {
            Hashtable<K, T> newTable = new Hashtable<>();
            newTable.put(entityIndex, newEntity);
            table.put(projectName, newTable);
        }
    }

    protected <T> void addEntry(Hashtable<String, Hashtable<Integer, T>> table,
                                String projectName,
                                T newEntity) {
        if (table.containsKey(projectName)) {
            int entityIndex = table.get(projectName).size();
            table.get(projectName).put(entityIndex, newEntity);
        } else {
            Hashtable<Integer, T> newTable = new Hashtable<>();
            newTable.put(0, newEntity);
            table.put(projectName, newTable);
        }
    }

    protected void addArtifactBody(Hashtable<String, Hashtable<String, Hashtable<Long, ArtifactBody>>> table,
                                   String projectName,
                                   String artifactName,
                                   int versionIndex,
                                   ArtifactBody body) {
        if (table.containsKey(projectName)) {
            Hashtable<String, Hashtable<Long, ArtifactBody>> projectTable = table.get(projectName);
            if (projectTable.contains(artifactName)) {
                projectTable.get(projectName).put((long) versionIndex, body);
            } else {
                Hashtable<Long, ArtifactBody> versionTable = new Hashtable<>();
                versionTable.put((long) versionIndex, body);
                projectTable.put(artifactName, versionTable);
            }
        } else {
            Hashtable<String, Hashtable<Long, ArtifactBody>> projectTable = new Hashtable<>();
            table.put(projectName, projectTable);
            addArtifactBody(table, projectName, artifactName, versionIndex, body);
        }
    }
}
