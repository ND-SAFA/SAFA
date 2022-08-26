package edu.nd.crc.safa.features.projects.entities.app;

import java.util.UUID;

/**
 * Interface defined over all the application-side entities.
 */
public interface IAppEntity {
    UUID getId();

    void setId(UUID id);
}
