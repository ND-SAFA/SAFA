// Now let's create a user object
export const user = {
  validUser: {
    email: `test-${Math.random()}@test.com`,
    password: "123",
  },
  invalidUser: {
    email: `test-invalid-${Math.random()}@test.com`,
    password: "super-invalid-password",
  },
  editUser: {
    email: `test-edit-${Math.random()}@test.com`,
    password: "123",
    newPassword: "newPassword",
  },
  createUser: {
    email: `test-create-${Math.random()}@test.com`,
    password: "123",
  },
  deleteUser: {
    email: `test-delete-${Math.random()}@test.com`,
    password: "123",
  },
  inviteUser: {
    email: `test-invite-${Math.random()}@test.com`,
    invalidEmail: `test-invite-${Math.random()}@test.com`,
  },
};
