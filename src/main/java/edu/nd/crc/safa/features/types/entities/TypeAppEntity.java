package edu.nd.crc.safa.features.types.entities;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The front-end model of an artifact type
 */
@NoArgsConstructor
@Data
public class TypeAppEntity implements IAppEntity {

    /**
     * ID of artifact type
     */
    private UUID typeId;

    /**
     * Name of artifact type
     */
    private String name;

    /**
     * Icon representing artifact type
     */
    private String icon;

    /**
     * Color that should be used for this type
     */
    private String color;

    /**
     * Number of artifacts of this type in the current project version. If the version is unknown, this is -1
     */
    private int count;

    public TypeAppEntity(ArtifactType artifactType) {
        this.typeId = artifactType.getId();
        this.name = artifactType.getName();
        this.icon = artifactType.getIcon();
        this.color = artifactType.getColor();

        // Counts are set within a specific project version, but we don't know the version yet,
        // so set this to -1 to indicate it hasn't been set
        this.count = -1;
    }

    @Override
    public UUID getId() {
        return this.typeId;
    }

    @Override
    public void setId(UUID id) {
        this.typeId = id;
    }
}
