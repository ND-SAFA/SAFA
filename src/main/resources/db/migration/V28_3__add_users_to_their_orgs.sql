DELETE org_membership
    FROM org_membership
    INNER JOIN organization on org_membership.org_id = organization.id
    WHERE organization.personal_org = True;

INSERT INTO org_membership (user_id, org_id, role, id)
SELECT safa_user.user_id, organization.id, 'ADMIN', (SELECT ${uuid_generator})
FROM organization
    INNER JOIN safa_user on organization.owner_id = safa_user.user_id;