package edu.nd.crc.safa.utilities.graphql.entities;

import lombok.Data;

@Data
public class EdgeNode<T> {
    private T node;
}