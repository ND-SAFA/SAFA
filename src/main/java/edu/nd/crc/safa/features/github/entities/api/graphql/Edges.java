package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.List;

import lombok.Data;

@Data
public class Edges<T> {
    private List<EdgeNode<T>> edges;
    private PageInfo pageInfo;
}
