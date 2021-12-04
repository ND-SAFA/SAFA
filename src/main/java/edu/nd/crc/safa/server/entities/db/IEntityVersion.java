package edu.nd.crc.safa.server.entities.db;

import edu.nd.crc.safa.server.entities.app.IAppEntity;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IEntityVersion<AppType extends IAppEntity> {

    ProjectVersion getProjectVersion();

    ModificationType getModificationType();

    String getEntityId();

    boolean hasSameContent(IEntityVersion e);

    boolean hasSameContent(AppType a);
}
