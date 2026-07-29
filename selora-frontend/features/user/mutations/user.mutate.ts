"use client";

import { useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/features/api/lib";

import { userApi } from "../api";

export function useMeQuery() {
	return useQuery({
		queryKey: queryKeys.accounts.profile,
		queryFn: userApi.getMyProfile,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}
