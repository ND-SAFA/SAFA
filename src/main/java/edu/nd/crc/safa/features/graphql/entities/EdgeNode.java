package edu.nd.crc.safa.features.graphql.entities;

import lombok.Data;

@Data
public class EdgeNode<T> {
    private T node;
}