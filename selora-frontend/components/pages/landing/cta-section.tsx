"use client";

import Link from "next/link";

export default function CtaSection() {
	return (
		<section>
			<div className="rounded-2xl bg-linear-to-l from-primary to-purple-600 p-8 text-center text-white shadow-xl md:p-12">
				<h2 className="text-3xl font-bold md:text-4xl">
					آماده‌اید تا سبک خود را ارتقا دهید؟
				</h2>
				<p className="mx-auto mt-4 max-w-2xl text-indigo-100">
					به هزاران مشتری خوشحال بپیوندید و قطعات عالی برای کمد لباس
					خود را کشف کنید.
				</p>
				<Link href="/#products">
					<button className="mt-8 rounded-full bg-white px-8 py-4 text-lg font-semibold text-primary transition hover:bg-indigo-50">
						شروع خرید
					</button>
				</Link>
			</div>
		</section>
	);
}
