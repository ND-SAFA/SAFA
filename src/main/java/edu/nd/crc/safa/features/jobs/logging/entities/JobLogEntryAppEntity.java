package edu.nd.crc.safa.features.jobs.logging.entities;

import java.sql.Timestamp;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class JobLogEntryAppEntity {
    private Timestamp timestamp;

    private String entry;
}
