ALTER TABLE user_project_membership DROP FOREIGN KEY user_project_membership_ibfk_1;
ALTER TABLE user_project_membership DROP FOREIGN KEY user_project_membership_ibfk_2;

ALTER TABLE user_project_membership DROP CONSTRAINT SINGLE_ROLE_PER_PROJECT;

ALTER TABLE user_project_membership ADD FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE;
ALTER TABLE user_project_membership ADD FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE;