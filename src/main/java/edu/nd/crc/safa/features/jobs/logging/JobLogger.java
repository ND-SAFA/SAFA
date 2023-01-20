package edu.nd.crc.safa.features.jobs.logging;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.sql.Timestamp;
import java.time.Instant;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.logging.services.JobLoggingService;

import lombok.Setter;

/**
 * A JobLogger is used to allow jobs to log to the database. Those logs can then be
 * sent to the user to be displayed.
 */
public class JobLogger {
    private final JobLoggingService loggingService;

    @Setter
    private int stepNum;

    private final JobDbEntity job;

    public JobLogger(JobLoggingService loggingService, JobDbEntity job, int stepNum) {
        this.loggingService = loggingService;
        this.job = job;
        this.stepNum = stepNum;
    }

    /**
     * Add a new log message.
     *
     * @param message The message to add.
     */
    public void log(String message) {
        Timestamp timestamp = Timestamp.from(Instant.now());
        JobLogEntry entry = new JobLogEntry(job, (short) stepNum, timestamp, message);
        System.out.println(entry);
        loggingService.saveLog(entry);
    }

    /**
     * Add a new log message.
     *
     * @param format The format of the message.
     * @param args Args to fill into the format.
     */
    public void log(String format, Object... args) {
        log(String.format(format, args));
    }

    /**
     * Add a log message for an exception.
     *
     * @param exception The exception that was thrown.
     */
    public void logException(Throwable exception) {
        StringWriter stringWriter = new StringWriter();
        PrintWriter printWriter = new PrintWriter(stringWriter);
        exception.printStackTrace(printWriter);
        log(stringWriter.toString());
    }
}
