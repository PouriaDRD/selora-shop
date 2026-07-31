/**
 * Authentication API layer
 * All HTTP calls for auth feature
 */

import { apiClient, endpoints } from "@/features/api/lib";
import { getCartSession } from "@/features/cart/actions";

import {
	LoginFormValues,
	LoginHistory,
	LoginResponse,
	RegisterFormValues,
	RegisterResponse,
} from "../types";

export const authApi = {
	login: async (data: LoginFormValues) => {
		const cartSession = await getCartSession();

		return apiClient.post<LoginResponse>(endpoints.auth.login, {
			...data,
			session_key: cartSession ?? undefined,
		});
	},

	logout: ({ refresh }: { refresh: string }) => {
		return apiClient.post(endpoints.auth.logout, {
			refresh,
		});
	},

	register: async (data: RegisterFormValues) => {
		const cartSession = await getCartSession();

		return apiClient.post<RegisterResponse>(endpoints.auth.register, {
			...data,
			session_key: cartSession ?? undefined,
		});
	},

	history: () => {
		return apiClient.get<LoginHistory[]>(endpoints.auth.history);
	},
};
