package edu.nd.crc.safa.features.search;

/***
 * Enumerates the different search modes.
 */
public enum SearchMode {
    PROMPT("prompt"),
    ARTIFACTS("artifacts"),
    ARTIFACTTYPES("artifactTypes");
    String value;

    SearchMode(String value) {
        this.value = value;
    }
}
