package edu.nd.crc.safa.test.services.builders;

import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import lombok.Getter;

public class TypeBuilder {
    @Getter
    private final ArtifactType artifactType;

    public TypeBuilder() {
        this.artifactType = new ArtifactType();
    }

    public TypeBuilder withName(String name) {
        this.artifactType.setName(name);
        return this;
    }

    public TypeBuilder withIcon(String icon) {
        this.artifactType.setIcon(icon);
        return this;
    }

    public TypeBuilder withDummyIcon() {
        return withIcon("mdi-alert");
    }

    public TypeBuilder withColor(String color) {
        this.artifactType.setColor(color);
        return this;
    }
}
