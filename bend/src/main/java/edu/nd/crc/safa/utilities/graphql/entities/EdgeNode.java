package edu.nd.crc.safa.utilities.graphql.entities;

import lombok.Data;

@Data
public class EdgeNode<T> implements DefaultPaginatable {
    private T node;
}