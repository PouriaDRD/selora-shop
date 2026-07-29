"use client";

import { Button, FieldGroup, Spinner } from "@/components/ui";

import { useRegisterForm } from "../../hooks";
import {
	ConfirmPasswordField,
	NameField,
	PasswordField,
	UsernameField,
} from "../fields";

interface Props {
	onSuccess?: () => void;
}

function RegisterForm({ onSuccess }: Props) {
	const { form, submit, isPending } = useRegisterForm({
		onSuccess() {
			onSuccess?.();
		},
	});

	return (
		<form id="register-form" onSubmit={submit}>
			<FieldGroup>
				{/* Username*/}
				<UsernameField
					control={form.control}
					name="username"
					label="نام کاربری"
				/>

				{/* First Name */}
				<NameField
					key={"first_name"}
					control={form.control}
					name="first_name"
					label="نام(اختیاری)"
				/>

				{/* Last Name */}
				<NameField
					key={"last_name"}
					control={form.control}
					name="last_name"
					label="نام خانوادگی(اختیاری)"
				/>

				{/* Password */}
				<PasswordField
					control={form.control}
					name="password"
					label="رمز عبور"
				/>

				{/* Confirm Password */}
				<ConfirmPasswordField
					control={form.control}
					name="confirm_password"
					label="تکرار رمز عبور"
				/>
			</FieldGroup>

			<Button
				type="submit"
				form="register-form"
				className="w-full mt-6"
				disabled={isPending}>
				{isPending ? <Spinner /> : "ثبت نام"}
			</Button>
		</form>
	);
}

export default RegisterForm;
