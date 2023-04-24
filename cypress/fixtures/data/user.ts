// Lets create an interface for all users
export interface userData {
  validUser: {
    email: string;
    password: string;
  };
  invalidUser: {
    email: string;
    password: string;
  };
  editUser: {
    email: string;
    password: string;
    newPassword: string;
  };
  createUser: {
    email: string;
    password: string;
  };
  deleteUser: {
    email: string;
    password: string;
  };
  inviteUser: {
    email: string;
    invalidEmail: string;
  };
}

// Now lets create a user object
export const user: userData = {
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
