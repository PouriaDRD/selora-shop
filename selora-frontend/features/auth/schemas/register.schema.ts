import { z } from "zod";

export const registerSchema = z
	.object({
		username: z.email("لطفا ایمیل صحیح وارد کنید"),

		password: z.string().min(8, "رمز عبور باید حداقل 8 کاراکتر باشد"),

		confirm_password: z
			.string()
			.min(8, "رمز عبور باید حداقل 8 کاراکتر باشد"),
	})
	.refine((data) => data.password === data.confirm_password, {
		message: "رمز عبور و تکرار آن یکسان نیستند",
		path: ["confirm_password"],
	});
