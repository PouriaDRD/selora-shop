"use client";

import { useState } from "react";

import { toast } from "sonner";

import { useUser } from "@/features/user/context";

import { getRefreshToken, logoutAction } from "../actions";
import { useLogoutMutation } from "../mutations";

export function useLogout() {
	const [isLoading, setIsLoading] = useState(false);
	const { clearUser } = useUser();

	const logoutMutation = useLogoutMutation();

	const handleLogout = async () => {
		setIsLoading(true);
		try {
			const refreshToken = await getRefreshToken();
			console.log("refreshToken", refreshToken);

			if (refreshToken) {
				logoutMutation.mutate(
					{
						refresh: refreshToken,
					},
					{
						onSuccess: async (data) => {
							if (!data.status) {
								toast.error("خطا در خارج شدن از سیستم");
								return;
							}
							await logoutAction();
							clearUser();
							toast.success("با موفقیت خارج شدید");
							window.location.href = "/auth/login";
						},
						onError: async () => {
							toast.error("خطا در خارج شدن از سیستم");
							return;
						},
					},
				);
			}

			// clear user session
			// await logoutAction();
			// clearUser();
			// toast.success("با موفقیت خارج شدید");

			// redirect to login page
			// window.location.href = "/auth/login";
		} catch (error) {
			if (process.env.NODE_ENV === "development") {
				console.error("[LogoutAction]", error);
			}

			toast.error("خطایی رخ داده است. لطفا مجددا تلاش کنید.");
		} finally {
			setIsLoading(false);
		}
	};

	return {
		isLoading,
		handleLogout,
	};
}
