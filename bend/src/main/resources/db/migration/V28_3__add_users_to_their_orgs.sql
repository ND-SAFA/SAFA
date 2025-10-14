DELETE FROM org_membership
WHERE EXISTS (
    SELECT 1
        FROM organization
        WHERE org_membership.org_id = organization.id
            AND organization.personal_org = True
);

INSERT INTO org_membership (user_id, org_id, role, id)
SELECT safa_user.user_id, organization.id, 'ADMIN', (SELECT ${uuid_generator})
FROM organization
    INNER JOIN safa_user on organization.owner_id = safa_user.user_id;