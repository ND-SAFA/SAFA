package edu.nd.crc.safa.utilities.graphql.entities;

import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;

@Data
public class PageInfo {
    private String endCursor;

    @Getter(AccessLevel.NONE)
    private boolean hasNextPage;

    public boolean hasNextPage() {
        return hasNextPage;
    }
}
