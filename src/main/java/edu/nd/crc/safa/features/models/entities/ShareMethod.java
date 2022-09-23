package edu.nd.crc.safa.features.models.entities;

public enum ShareMethod {
    COPY_BY_VALUE,
    COPY_BY_REFERENCE;

    @Override
    public String toString() {
        return this.name();
    }
}
