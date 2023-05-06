package edu.nd.crc.safa.utilities.graphql.entities;

import java.util.List;

import lombok.Data;

@Data
public class Edges<T extends Paginatable> {
    private List<EdgeNode<T>> edges;
    private PageInfo pageInfo;
}
