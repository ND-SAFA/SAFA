package edu.nd.crc.safa.features.types;

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
    String typeId;
    /**
     * Name of artifact type .
     */
    String name;
    /**
     * Icon representing artifact type.
     */
    String icon;

    public TypeAppEntity(ArtifactType artifactType) {
        this.typeId = artifactType.getTypeId().toString();
        this.name = artifactType.getName();
        this.icon = artifactType.getIcon();
    }

    @Override
    public String getBaseEntityId() {
        return null;
    }

    @Override
    public void setBaseEntityId(String id) {

    }
}
