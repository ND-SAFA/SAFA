ALTER TABLE job ADD COLUMN job_type_class_name VARCHAR(255) NOT NULL DEFAULT '';

UPDATE job SET job_type_class_name = CASE
    WHEN job_type = 0 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob'
    WHEN job_type = 1 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob'
    WHEN job_type = 2 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob'
    WHEN job_type = 3 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob'
    WHEN job_type = 4 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob'
    WHEN job_type = 5 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectUpdateJob'
    WHEN job_type = 6 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectImportJob'
    WHEN job_type = 7 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectImportJob'
    WHEN job_type = 8 THEN ''
    WHEN job_type = 9 THEN ''
    WHEN job_type = 10 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.TrainModelJob'
    WHEN job_type = 11 THEN 'edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob'
    ELSE ''
    END
WHERE job_type IN (0,1,2,3,4,5,6,7,8,9,10,11);

DELETE FROM job WHERE job_type_class_name = '';

ALTER TABLE job DROP COLUMN job_type;

ALTER TABLE job RENAME COLUMN job_type_class_name TO job_type;