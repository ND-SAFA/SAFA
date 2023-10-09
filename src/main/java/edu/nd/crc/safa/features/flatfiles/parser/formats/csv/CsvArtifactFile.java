package edu.nd.crc.safa.features.flatfiles.parser.formats.csv;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.flatfiles.parser.base.AbstractArtifactFile;
import edu.nd.crc.safa.utilities.CsvFileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.apache.commons.csv.CSVRecord;
import org.javatuples.Pair;
import org.springframework.web.multipart.MultipartFile;

/**
 * A CSV file defining a set of artifacts on each row.
 *
 * <p>File is expected to contain a name, summary, and body
 */
@Setter
@EqualsAndHashCode(callSuper = true)
public class CsvArtifactFile extends AbstractArtifactFile<CSVRecord> {

    /**
     * The artifact type to be associated with all artifacts.
     */
    private String artifactType;

    public CsvArtifactFile(String artifactType,
                           List<ArtifactAppEntity> artifacts) {
        super(artifacts);
        setPossibleNullArgument(this::setArtifactType, artifactType, "artifactType");
    }

    public CsvArtifactFile(String artifactType,
                           String pathToFile) throws IOException {
        super(pathToFile, false);
        setPossibleNullArgument(this::setArtifactType, artifactType, "artifactType");
        this.parseEntities();
    }

    public CsvArtifactFile(String artifactType,
                           MultipartFile file) throws IOException {
        super(file, false);
        setPossibleNullArgument(this::setArtifactType, artifactType, "artifactType");
        this.parseEntities();
    }

    @Override
    protected void exportAsFileContent(File file) throws IOException {
        String[] headers = getHeaders();
        CsvFileUtilities.writeEntitiesAsCsvFile(file, headers, this.getEntities(),
            artifact -> this.getArtifactRow(artifact, headers));
    }

    /**
     * Retrieve the list of headers for the output file. The list consists of all the
     * default headers plus all the keys for the custom attributes.
     *
     * @return The headers
     */
    private String[] getHeaders() {
        Set<String> headers = Constants.ALL_COLUMNS_SET;
        for (ArtifactAppEntity entity : getEntities()) {
            headers.addAll(entity.getAttributes().keySet());
        }
        return headers.toArray(new String[0]);
    }

    /**
     * Gets a row for the output file based on the given artifact.
     *
     * @param artifact The artifact to output.
     * @param headers  The list of headers (used to determine the order of the items to output).
     * @return A list of strings corresponding to entries in this row of the CSV file.
     */
    private String[] getArtifactRow(ArtifactAppEntity artifact, String[] headers) {
        List<String> rowItems = new ArrayList<>();

        for (String header : headers) {
            rowItems.add(getValueOfColumn(artifact, header));
        }

        return rowItems.toArray(new String[0]);
    }

    /**
     * Retrieves the value of the given column for the given artifact.
     *
     * @param artifact The artifact
     * @param header   The column in the CSV file we are trying to get the value of
     * @return The value of that column
     */
    private String getValueOfColumn(ArtifactAppEntity artifact, String header) {
        switch (header) {
            case Constants.NAME_PARAM:
                return artifact.getName();
            case Constants.CONTENT_PARAM:
                return artifact.getBody();
            case Constants.SUMMARY_PARAM:
                return artifact.getSummary();
            default:
                Map<String, JsonNode> attributes = artifact.getAttributes();
                return attributes.containsKey(header) ? attributes.get(header).toString() : null;
        }
    }

    @Override
    public List<CSVRecord> readFileRecords(String pathToFile) throws IOException {
        return CsvFileUtilities.readArtifactFile(pathToFile);
    }

    @Override
    public List<CSVRecord> readFileRecords(MultipartFile file) throws IOException {
        return CsvFileUtilities.readArtifactFile(file);
    }

    @Override
    public Pair<ArtifactAppEntity, String> parseRecord(CSVRecord entityRecord) {
        if (artifactType == null) {
            throw new IllegalArgumentException("Cannot parse record without artifact type");
        }
        try {
            String artifactName = entityRecord.get(Constants.NAME_PARAM);
            String artifactSummary = entityRecord.isSet(Constants.SUMMARY_PARAM)
                ? entityRecord.get(Constants.SUMMARY_PARAM) : "";
            String artifactContent = entityRecord.get(Constants.CONTENT_PARAM);

            Map<String, JsonNode> recordAttributes = getCustomAttributes(entityRecord);

            artifactSummary = artifactSummary == null ? "" : artifactSummary;
            artifactContent = artifactContent == null ? "" : artifactContent;
            ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
                null,
                artifactType,
                artifactName,
                artifactSummary,
                artifactContent,
                recordAttributes
            );

            return new Pair<>(artifactAppEntity, null);
        } catch (Exception e) {
            return new Pair<>(null, String.format("%s: %s", getFilename(), e.getMessage()));
        }
    }

    /**
     * Given a line in a CSV file, get the custom attributes in the line.
     *
     * @param entityRecord The CSV file entry.
     * @return A map from the names of the attributes to their values.
     * @throws JsonProcessingException If there is an issue parsing the value of the attribute.
     */
    private Map<String, JsonNode> getCustomAttributes(CSVRecord entityRecord) throws JsonProcessingException {
        Map<String, JsonNode> recordAttributes = new HashMap<>();
        ObjectMapper objectMapper = ObjectMapperConfig.create();

        for (Map.Entry<String, String> entry : entityRecord.toMap().entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();

            if (!isKnownColumn(key)) {
                recordAttributes.put(key, getCustomAttributeValue(objectMapper, value));
            }
        }

        return recordAttributes;
    }

    /**
     * Check whether a column is known or if it describes a custom attribute.
     *
     * @param key The name of the column.
     * @return True if the column maps to a known field, false if it is for a custom attribute.
     */
    private boolean isKnownColumn(String key) {
        return Constants.ALL_COLUMNS_SET.contains(key.toLowerCase());
    }

    /**
     * Checks if a string is likely to be JSON. We consider it likely to be JSON encoded
     * if it starts and ends with {}, [], or "".
     *
     * @param value The string in question.
     * @return Whether the string is probably a JSON encoded string.
     */
    private boolean isLikelyJsonString(String value) {
        return (value.startsWith("{") && value.endsWith("}"))
            || (value.startsWith("[") && value.endsWith("]"))
            || (value.startsWith("\"") && value.endsWith("\""));
    }

    /**
     * Gets the JsonNode value of a custom attribute value.
     *
     * @param objectMapper The object mapper for reading JSON values.
     * @param value        The string value of the custom attribute.
     * @return The parsed JSON value of the custom attribute.
     * @throws JsonProcessingException If the JSON is invalid.
     */
    private JsonNode getCustomAttributeValue(ObjectMapper objectMapper, String value) throws JsonProcessingException {
        TypeReference<JsonNode> type = new TypeReference<>() {
        };

        try {
            return objectMapper.readValue(value, type);
        } catch (JsonProcessingException e) {

            // If the string is likely to be a JSON string, then the processing exception is likely
            // valid, so allow it to pass through. Otherwise, it's likely just a normal string that
            // needs to be surrounded in quotes in order for the object mapper to recognize it as such.
            if (isLikelyJsonString(value)) {
                throw e;
            } else {
                return objectMapper.readValue(String.format("\"%s\"", value), type);
            }
        }
    }

    public <T> void setPossibleNullArgument(Consumer<T> argumentSetter, T argument, String name) {
        if (argument == null) {
            throw new IllegalArgumentException(name + " cannot be null.");
        }
        argumentSetter.accept(argument);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Constants {
        public static final String NAME_PARAM = "id";
        public static final String SUMMARY_PARAM = "summary";
        public static final String CONTENT_PARAM = "content";

        public static final String[] REQUIRED_COLUMNS = new String[]{NAME_PARAM, CONTENT_PARAM};
        public static final String[] ALL_COLUMNS = new String[]{NAME_PARAM, SUMMARY_PARAM, CONTENT_PARAM};

        public static final Set<String> ALL_COLUMNS_SET = new HashSet<>(List.of(ALL_COLUMNS));
    }
}
