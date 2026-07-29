import { z } from "zod";

export const registerSchema = z
	.object({
		username: z
			.string("نام کاربری الزامی است")
			.trim()
			.min(3, "نام کاربری باید حداقل ۳ کاراکتر باشد")
			.max(150, "نام کاربری باید حداکثر ۱۵۰ کاراکتر باشد")
			.regex(
				/^[a-zA-Z0-9_]+$/,
				"نام کاربری فقط می‌تواند شامل حروف انگلیسی، اعداد و _ باشد",
			),

		first_name: z
			.string()
			.trim()
			.min(2, "نام باید حداقل ۲ کاراکتر باشد")
			.max(150, "نام باید حداکثر ۱۵۰ کاراکتر باشد")
			.optional()
			.or(z.literal("")),

		last_name: z
			.string()
			.trim()
			.min(2, "نام خانوادگی باید حداقل ۲ کاراکتر باشد")
			.max(150, "نام خانوادگی باید حداکثر ۱۵۰ کاراکتر باشد")
			.optional()
			.or(z.literal("")),

		password: z.string().min(8, "رمز عبور باید حداقل 8 کاراکتر باشد"),

		confirm_password: z
			.string()
			.min(8, "رمز عبور باید حداقل 8 کاراکتر باشد"),
	})
	.refine((data) => data.password === data.confirm_password, {
		message: "رمز عبور و تکرار آن یکسان نیستند",
		path: ["confirm_password"],
	});
