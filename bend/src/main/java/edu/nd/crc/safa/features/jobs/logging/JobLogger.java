package edu.nd.crc.safa.features.jobs.logging;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.reflect.InvocationTargetException;
import java.sql.Timestamp;
import java.time.Instant;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.logging.services.JobLoggingService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.Getter;
import lombok.Setter;

/**
 * A JobLogger is used to allow jobs to log to the database. Those logs can then be
 * sent to the user to be displayed.
 */
public class JobLogger {
    private final JobLoggingService loggingService;
    @Getter
    private final JobDbEntity job;
    @Setter
    private int stepNum;

    public JobLogger(JobLoggingService loggingService, JobDbEntity job, int stepNum) {
        this.loggingService = loggingService;
        this.job = job;
        this.stepNum = stepNum;
    }

    /**
     * Add a new log message.
     *
     * @param message The message to add.
     * @return Updated job entry.
     */
    public JobLogEntry log(String message) {
        Timestamp timestamp = Timestamp.from(Instant.now());
        JobLogEntry entry = new JobLogEntry(job, (short) stepNum, timestamp, message);
        loggingService.saveLog(entry);
        return entry;
        // Uncomment to show job logs on the command line
        //System.out.println(entry);
    }

    /**
     * Add a new log message.
     *
     * @param format The format of the message.
     * @param args   Args to fill into the format.
     * @return The updated job entry after committing log.
     */
    public JobLogEntry log(String format, Object... args) {
        return log(String.format(format, args));
    }

    /**
     * Adds additional string to log.
     *
     * @param entry    The Job log entry to add content to.
     * @param addition The new content to add.
     * @return The saved entity.
     */
    public JobLogEntry addToLog(JobLogEntry entry, String addition) {
        String newBody = entry.getEntry() + addition;
        entry.setEntry(newBody);
        entry = loggingService.saveLog(entry);
        return entry;
    }

    /**
     * Add a log message for an exception.
     *
     * @param exception The exception that was thrown.
     */
    public void logException(Throwable exception) {
        while (exception instanceof InvocationTargetException && exception.getCause() != null) {
            exception = exception.getCause();
        }

        StringWriter stringWriter = new StringWriter();
        PrintWriter printWriter = new PrintWriter(stringWriter);

        if (exception instanceof SafaError) {
            log(exception.getMessage());
        } else {
            exception.printStackTrace(printWriter);
            log(stringWriter.toString());
        }
    }
}
