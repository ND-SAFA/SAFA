package edu.nd.crc.safa.utilities.graphql.entities;

import lombok.Data;

@Data
public class PageInfo {
    private String endCursor;
    private boolean hasNextPage;
}
