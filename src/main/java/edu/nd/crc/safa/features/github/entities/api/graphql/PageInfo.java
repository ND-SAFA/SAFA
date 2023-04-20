package edu.nd.crc.safa.features.github.entities.api.graphql;

import lombok.Data;

@Data
public class PageInfo {
    private String endCursor;
    private boolean hasNextPage;
}
