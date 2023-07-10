package edu.nd.crc.safa.features.types.entities;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import lombok.Data;

/**
 * The front-end model of an artifact type
 */
@Data
public class TypeAppEntity implements IAppEntity {

    /**
     * ID of artifact type.
     */
    private UUID typeId;

    /**
     * Name of artifact type .
     */
    private String name;

    /**
     * Icon representing artifact type.
     */
    private String icon;

    private String color;
    private int count;

    public TypeAppEntity(ArtifactType artifactType) {
        this.typeId = artifactType.getId();
        this.name = artifactType.getName();
        this.icon = artifactType.getIcon();
        this.color = artifactType.getColor();
        this.count = 0; //TODO
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
