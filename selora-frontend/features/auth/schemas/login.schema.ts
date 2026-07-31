import { z } from "zod";

export const loginSchema = z.object({
	username: z
		.string()
		.min(3, "نام کاربری باید حداقل 3 کارکتر باشد")
		.max(30, "نام کاربری باید حداکثر 30 کارکتر باشد"),

	password: z.string().min(1, "رمز عبور باید حداقل 1 کاراکتر باشد"),
});
