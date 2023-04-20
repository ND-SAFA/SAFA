package edu.nd.crc.safa.features.github.entities.api.graphql;

import lombok.Data;

@Data
public class EdgeNode<T> {
    private T node;
}