export const UserRole = ["user", "admin", "superuser"] as const;

export type UserRole = (typeof UserRole)[number];

export const UserStatus = ["active", "inactive", "banned"] as const;

export type UserStatus = (typeof UserStatus)[number];

export type User = {
	id: string;
	username: string;
	first_name: string;
	last_name: string;
	full_name: string;
	role: UserRole;
	status: UserStatus;
	last_login: Date;
	created_at: Date;
};
