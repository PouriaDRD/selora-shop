"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

import { LoginStoreState } from "../types/login.type";

export const useLoginStore = create<LoginStoreState>()(
	persist(
		(set) => ({
			username: "",
			password: "",

			set: (patch) => set((state) => ({ ...state, ...patch })),

			reset: () =>
				set({
					username: "",
					password: "",
				}),

			_hasHydrated: false,
			setHasHydrated: (state: boolean) => set({ _hasHydrated: state }),
		}),
		{
			name: "lgs-store",

			// Store in Browser's localStorage only if browser is available
			storage: createJSONStorage(() => {
				if (typeof window !== "undefined") {
					return localStorage;
				}
				return {
					getItem: () => null,
					setItem: () => {},
					removeItem: () => {},
				};
			}),

			// Only save these states to storage (Not Password)
			partialize: (state) => ({
				username: state.username,
			}),
			onRehydrateStorage: () => (state) => {
				state?.setHasHydrated(true);
			},
		},
	),
);
