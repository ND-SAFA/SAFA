CREATE TABLE job_log_entry
(
    id         BINARY(16)   NOT NULL,
    job_id     VARCHAR(255) NOT NULL,
    step_num   SMALLINT     NOT NULL,  /* Honestly I think TINYINT would be enough but just in case */
    entry      MEDIUMTEXT   NOT NULL,
    timestamp  DATETIME(6)  NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (job_id) REFERENCES job (id) ON DELETE CASCADE,
    INDEX (job_id, step_num, timestamp)
);