package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.IAppEntity;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IVersionEntity<AppType extends IAppEntity> {

    ProjectVersion getProjectVersion();

    ModificationType getModificationType();

    String getBaseEntityId();

    UUID getEntityVersionId();

    void setEntityVersionId(UUID entityVersionId);

    boolean hasSameContent(IVersionEntity e);

    boolean hasSameContent(AppType a);
}
