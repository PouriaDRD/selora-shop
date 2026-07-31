"use client";

import { useEffect, useEffectEvent } from "react";

import { useRouter, useSearchParams } from "next/navigation";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { queryClient, queryKeys } from "@/features/api/lib";
import { useUser } from "@/features/user/context";

import { createSession } from "../actions";
import { useRegister } from "../mutations";
import { registerSchema } from "../schemas";
import { useRegisterStore } from "../stores";
import { RegisterData } from "../types";

interface Props {
	onSuccess?: () => void;
}

export function useRegisterForm({ onSuccess }: Props) {
	const router = useRouter();
	const searchParams = useSearchParams();
	const next = searchParams.get("next");

	const { refetchUser } = useUser();
	const registerMutation = useRegister();
	const registerStore = useRegisterStore();

	const form = useForm({
		resolver: zodResolver(registerSchema),
		defaultValues: {
			username: registerStore.username,
			first_name: registerStore.first_name,
			last_name: registerStore.last_name,
			password: "",
			confirm_password: "",
		},
	});

	const handleOnSuccess = async (data: RegisterData) => {
		await Promise.all([
			createSession({
				token: data.access,
				expireTimeUtc: data.access_expires_at,
				type: "acs",
			}),
			createSession({
				token: data.refresh,
				expireTimeUtc: data.refresh_expires_at,
				type: "rfs",
			}),

			refetchUser(),

			queryClient.invalidateQueries({
				queryKey: queryKeys.cart.cart,
			}),
		]);

		toast.success("حساب کاربری با موفقیت ایجاد شد!");

		form.reset();
		registerStore.reset();

		onSuccess?.();

		const redirectTo = next ?? "/";

		router.push(redirectTo as "/");
	};

	const submit = form.handleSubmit(async (values) => {
		registerMutation.mutate(values, {
			onSuccess: async (res) => {
				if (!res.status) {
					toast.error("نام کاربری تکراری است!");
					return;
				}

				await handleOnSuccess(res.data);
			},
			onError: () => {
				toast.error("خطا ناخواسته در ثبت نام");
			},
		});
	});

	/**
	 * Sync form values with zustand store
	 */
	useEffect(() => {
		// eslint-disable-next-line react-hooks/incompatible-library
		const subscription = form.watch((values) => {
			registerStore.set({
				username: values.username,
				first_name: values.first_name,
				last_name: values.last_name,
				password: values.password,
				confirm_password: values.confirm_password,
			});
		});

		return () => subscription.unsubscribe();
	}, [form, registerStore]);

	/**
	 * Restore form after zustand hydration
	 */
	const onHasHydrated = useEffectEvent(() => {
		form.reset({
			username: registerStore.username,
			first_name: registerStore.first_name,
			last_name: registerStore.last_name,
			password: "",
			confirm_password: "",
		});
	});

	useEffect(() => {
		if (registerStore._hasHydrated) {
			onHasHydrated();
		}
	}, [registerStore._hasHydrated]);

	return {
		form,
		submit,
		isPending: registerMutation.isPending,
	};
}
