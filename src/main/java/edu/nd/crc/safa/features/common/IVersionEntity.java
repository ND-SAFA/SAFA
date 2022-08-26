package edu.nd.crc.safa.features.common;

import java.util.UUID;

import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.versions.entities.IProjectVersionGetter;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IVersionEntity<A extends IAppEntity> extends IProjectVersionGetter {

    ModificationType getModificationType();

    UUID getBaseEntityId();

    UUID getVersionEntityId();

    void setVersionEntityId(UUID versionEntityId);

    boolean hasSameContent(IVersionEntity<A> e);

    boolean hasSameContent(A a);
}
