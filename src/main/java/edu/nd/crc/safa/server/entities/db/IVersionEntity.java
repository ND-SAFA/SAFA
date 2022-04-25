package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.project.IAppEntity;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IVersionEntity<AppType extends IAppEntity> {

    ProjectVersion getProjectVersion();

    ModificationType getModificationType();

    String getBaseEntityId();

    UUID getVersionEntityId();

    void setVersionEntityId(UUID versionEntityId);

    boolean hasSameContent(IVersionEntity e);

    boolean hasSameContent(AppType a);
}
