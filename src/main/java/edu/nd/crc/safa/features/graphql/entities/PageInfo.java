package edu.nd.crc.safa.features.graphql.entities;

import lombok.Data;

@Data
public class PageInfo {
    private String endCursor;
    private boolean hasNextPage;
}
