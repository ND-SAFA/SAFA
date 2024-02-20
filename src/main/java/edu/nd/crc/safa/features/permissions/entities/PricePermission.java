package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * A sort of pseudo permission used to indicate that a user cannot perform
 * an action due to not having enough funds in their account. This permission
 * should not be assigned to a role, it exists solely to indicate that the
 * user is lacking funds.
 */
@Getter
@AllArgsConstructor
public enum PricePermission implements SimplePermission {

    GENERATE_TRACES("price.generate_traces"),
    HGEN("price.hgen"),
    SEARCH("price.search"),
    SUMMARIZE_ARTIFACTS("price.summarize_artifacts"),
    SUMMARIZE_PROJECT("price.summarize_project");


    private final String name;
}
