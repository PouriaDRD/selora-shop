"use client";

import {
	type Control,
	Controller,
	type FieldValues,
	type Path,
} from "react-hook-form";

import { Field, FieldError, FieldLabel, Input } from "@/components/ui";

type Props<T extends FieldValues> = {
	control: Control<T>;
	name: Path<T>;
	label?: string;
};

export function UsernameField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "نام کاربری" } = props;
	return (
		<Controller
			name={name}
			control={control}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid}>
					<FieldLabel htmlFor="form-username">{label}</FieldLabel>
					<Input
						{...field}
						autoFocus
						type="username"
						autoComplete="username"
						id="form-username"
						aria-invalid={fieldState.invalid}
						placeholder="my_username"
						className="placeholder:text-right"
					/>
					{fieldState.invalid && (
						<FieldError
							errors={[fieldState.error]}
							className="text-xs"
						/>
					)}
				</Field>
			)}
		/>
	);
}
