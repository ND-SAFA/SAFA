package edu.nd.crc.safa.features.common;

import java.util.UUID;

import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

/**
 * Interface that generalizing similarities between all versioned entities.
 */
public interface IVersionEntity<A extends IAppEntity> {

    ProjectVersion getProjectVersion();

    ModificationType getModificationType();

    String getBaseEntityId();

    UUID getVersionEntityId();

    void setVersionEntityId(UUID versionEntityId);

    boolean hasSameContent(IVersionEntity<A> e);

    boolean hasSameContent(A a);
}
