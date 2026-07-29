/**
 * Base successful API response.
 */
export interface ApiSuccessResponse<T = unknown> {
	status: true;
	message: string | null;
	data: T;
}

/**
 * API error formats.
 *
 * Backend can return:
 * - string
 * - object with field errors
 * - array of errors
 */
export type ApiError = string | string[] | Record<string, string | string[]>;

/**
 * Base failed API response.
 */
export interface ApiErrorResponse {
	status: false;
	message: string | null;
	data: [];
	errors: ApiError | null;
}

/**
 * Union of all API responses.
 */
export type ApiResponse<T = unknown> = ApiSuccessResponse<T> | ApiErrorResponse;

/**
 * Type guard helpers
 */
export function isApiSuccess<T>(
	response: ApiResponse<T>,
): response is ApiSuccessResponse<T> {
	return response.status === true;
}

export function isApiError<T>(
	response: ApiResponse<T>,
): response is ApiErrorResponse {
	return response.status === false;
}
