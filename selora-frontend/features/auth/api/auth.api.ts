/**
 * Authentication API layer
 * All HTTP calls for auth feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import {
	LoginFormValues,
	LoginHistory,
	LoginResponse,
	RegisterFormValues,
	RegisterResponse,
} from "../types";

export const authApi = {
	login: (data: LoginFormValues) => {
		return apiClient.post<LoginResponse>(endpoints.auth.login, data);
	},

	logout: ({ refresh }: { refresh: string }) => {
		return apiClient.post(endpoints.auth.logout, {
			refresh: refresh,
		});
	},

	register: (data: RegisterFormValues) => {
		return apiClient.post<RegisterResponse>(endpoints.auth.register, data);
	},

	history: () => {
		return apiClient.get<LoginHistory[]>(endpoints.auth.history);
	},
};
