import { ApiResponse } from "@/features/api/types";
import { getSession, refreshAccessToken } from "@/features/auth/actions";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_API_URL?.trim() ?? "";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface RequestProps {
	url: string;
	method: HttpMethod;
	body?: unknown;
	params?: Record<string, string | number | boolean | undefined>;
	init?: RequestInit;
	timeout?: number;
	isMultipart?: boolean;
	retry?: boolean;
}

class ApiClient {
	private async request<T>(props: RequestProps): Promise<ApiResponse<T>> {
		const {
			url,
			method,
			body,
			params,
			init,
			timeout = 60000,
			isMultipart = false,
			retry = true,
		} = props;

		const controller = new AbortController();

		const timer = setTimeout(() => controller.abort(), timeout);

		try {
			const finalUrl = buildApiUrl(url, params);

			const headers: HeadersInit = {
				...(init?.headers ?? {}),
			};

			const token = await this.getToken();

			if (token) {
				(headers as Record<string, string>)["Authorization"] =
					`Bearer ${token}`;
			}

			if (!isMultipart) {
				(headers as Record<string, string>)["Content-Type"] =
					"application/json";
			}

			const response = await fetch(finalUrl, {
				method,
				headers,
				body: this.buildBody(body, isMultipart),
				signal: controller.signal,
				...init,
			});

			clearTimeout(timer);

			/**
			 * Rate limit
			 */
			if (response.status === 429) {
				return {
					status: false,
					message: "درخواست‌های زیادی ارسال شده است",
					data: [],
					errors: "لطفا چند لحظه بعد دوباره تلاش کنید",
				};
			}

			/**
			 * Refresh token
			 */
			if (response.status === 401 && retry) {
				const refreshed = await this.refreshToken();

				if (refreshed) {
					return this.request<T>({
						...props,
						retry: false,
					});
				}
			}

			const json = await response.json();

			return json as ApiResponse<T>;
		} catch (error: unknown) {
			clearTimeout(timer);

			if (process.env.NODE_ENV === "development") {
				console.error("[ApiClient]", error);
			}

			const errorName = error instanceof Error ? error.name : undefined;

			/**
			 * Timeout
			 */
			if (errorName === "AbortError") {
				return {
					status: false,
					message: "زمان درخواست به پایان رسید",
					data: [],
					errors: "Request timeout",
				};
			}

			/**
			 * Network error
			 */
			return {
				status: false,
				message: "خطای ارتباط با سرور",
				data: [],
				errors: "Network error",
			};
		}
	}

	// =========================
	// HTTP METHODS
	// =========================

	get<T>(url: string, params?: RequestProps["params"], init?: RequestInit) {
		return this.request<T>({
			url,
			method: "GET",
			params,
			init,
		});
	}

	post<T>(
		url: string,
		body?: unknown,
		init?: RequestInit,
		isMultipart = false,
	) {
		return this.request<T>({
			url,
			method: "POST",
			body,
			init,
			isMultipart,
		});
	}

	put<T>(url: string, body?: unknown, init?: RequestInit) {
		return this.request<T>({
			url,
			method: "PUT",
			body,
			init,
		});
	}

	patch<T>(url: string, body?: unknown, init?: RequestInit) {
		return this.request<T>({
			url,
			method: "PATCH",
			body,
			init,
		});
	}

	delete<T>(url: string, init?: RequestInit) {
		return this.request<T>({
			url,
			method: "DELETE",
			init,
		});
	}

	// =========================
	// AUTH
	// =========================

	private async getToken() {
		const token = await getSession();

		return token ?? null;
	}

	private async refreshToken() {
		try {
			const token = await refreshAccessToken();

			return Boolean(token);
		} catch {
			return false;
		}
	}

	// =========================
	// BODY
	// =========================

	private buildBody(body: unknown, isMultipart = false) {
		if (!body) {
			return undefined;
		}

		if (isMultipart && body instanceof FormData) {
			return body;
		}

		return JSON.stringify(body);
	}
}

export const apiClient = new ApiClient();

export function buildApiUrl(
	path: string,
	params?: Record<string, string | number | boolean | undefined>,
) {
	const base = BASE_URL.replace(/\/+$/, "");

	const cleanPath = path.replace(/^\/+/, "").replace(/\/+$/, "");

	const isAbsolute = /^https?:\/\//i.test(path);

	const url = isAbsolute
		? new URL(path)
		: new URL(`${cleanPath}/`, `${base}/`);

	if (params) {
		Object.entries(params).forEach(([key, value]) => {
			if (value !== undefined && value !== null) {
				url.searchParams.append(key, String(value));
			}
		});
	}

	return url.toString();
}
