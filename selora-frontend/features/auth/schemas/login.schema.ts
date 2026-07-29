import { z } from "zod";

export const loginSchema = z.object({
	username: z.string("نام‌کاربری اجباری است"),

	password: z.string().min(8, "رمز عبور باید حداقل 8 کاراکتر باشد"),
});
