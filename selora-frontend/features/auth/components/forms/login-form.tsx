"use client";

import { Button, FieldGroup, Spinner } from "@/components/ui";

import { useLoginForm } from "../../hooks";
import { PasswordField, UsernameField } from "../fields";

interface Props {
	onSuccess?: () => void;
}

function LoginForm({ onSuccess }: Props) {
	const { form, submit, isPending } = useLoginForm({
		onSuccess() {
			onSuccess?.();
		},
	});

	return (
		<form id="login-form" onSubmit={submit}>
			<FieldGroup>
				{/* Username Name */}
				<UsernameField
					control={form.control}
					name="username"
					label="نام کاربری"
				/>

				{/* Password */}
				<PasswordField
					control={form.control}
					name="password"
					label="رمز عبور"
				/>
			</FieldGroup>

			<Button
				type="submit"
				form="login-form"
				className="w-full mt-6"
				disabled={isPending}>
				{isPending ? <Spinner /> : "ورود به حساب"}
			</Button>
		</form>
	);
}

export default LoginForm;
