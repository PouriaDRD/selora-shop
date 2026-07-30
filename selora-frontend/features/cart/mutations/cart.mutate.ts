"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/features/api/lib";

import { cartApi } from "../api";

export const useMyCart = () => {
	return useQuery({
		queryKey: queryKeys.cart.cart,
		queryFn: cartApi.getCart,
		// auto refresh every 20 seconds
		refetchInterval: 20 * 1000,
	});
};

interface AddItemProps {
	variant_id: string;
	quantity: number;
	cartSession: string;
}

/**
 * Add single item
 */
export const useAddItem = () => {
	return useMutation({
		mutationFn: async ({
			variant_id,
			quantity,
			cartSession,
		}: AddItemProps) => {
			return cartApi.addItem(variant_id, quantity, cartSession);
		},
	});
};

/**
 * Update single item
 */
export const useUpdateItem = () => {
	return useMutation({
		mutationFn: ({
			item_id,
			new_quantity,
		}: {
			item_id: string;
			new_quantity: number;
		}) => cartApi.updateItem(item_id, new_quantity),
	});
};

/**
 * Remove single item
 */
export const useRemoveItem = () => {
	return useMutation({
		mutationFn: (item_id: string) => cartApi.removeItem(item_id),
	});
};
