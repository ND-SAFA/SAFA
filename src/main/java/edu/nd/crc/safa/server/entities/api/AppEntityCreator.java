package edu.nd.crc.safa.server.entities.api;

/**
 * Defines a lambda function for creating app entities from
 * a version entity.
 */
public interface AppEntityCreator<AppEntity, VersionEntity> {
    AppEntity createAppEntity(VersionEntity versionEntity);
}
