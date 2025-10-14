package edu.nd.crc.safa.utilities.graphql.entities;

import java.util.List;

import lombok.Data;

@Data
public class Edges<T> {
    private List<EdgeNode<T>> edges;
    private PageInfo pageInfo;
}
