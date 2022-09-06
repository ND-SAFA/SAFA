package edu.nd.crc.safa.features.types;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;

/**
 * The front-end model of an artifact type
 */
@Data
public class TypeAppEntity implements IAppEntity {

    /**
     * ID of artifact type.
     */
    UUID typeId;
    /**
     * Name of artifact type .
     */
    String name;
    /**
     * Icon representing artifact type.
     */
    String icon;

    public TypeAppEntity(ArtifactType artifactType) {
        this.typeId = artifactType.getTypeId();
        this.name = artifactType.getName();
        this.icon = artifactType.getIcon();
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
