"use client";

import { useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/features/api/lib";

import { storeApi } from "../api";

export function useGetCategories() {
	return useQuery({
		queryKey: queryKeys.store.categories,
		queryFn: storeApi.categories,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}

export function useGetCategoryDetails() {
	return useQuery({
		queryKey: queryKeys.store.categoryDetails,
		queryFn: storeApi.categoryDetails,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}

export function useGetProducts() {
	return useQuery({
		queryKey: queryKeys.store.products,
		queryFn: storeApi.products,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}

export function useGetProductDetails(slug: string) {
	return useQuery({
		queryKey: queryKeys.store.productDetails(slug),
		queryFn: () => storeApi.productDetails(slug),
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}
