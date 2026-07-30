"use client";

import Link from "next/link";

import { Minus, Plus, ShoppingBag, Trash2 } from "lucide-react";

import { Footer, Header } from "@/components/layouts";
import { Button } from "@/components/ui";
import { useCartActions, useGetMyCart } from "@/features/cart/hooks";

export default function CartPage() {
	const { cart, isLoading } = useGetMyCart();

	const {
		increaseQuantity,
		decreaseQuantity,
		removeItem,

		isUpdatingItem,
		isRemovingItem,
	} = useCartActions();

	if (isLoading) {
		return (
			<>
				<Header />

				<main className="container mx-auto max-w-7xl px-4 pt-12">
					<div className="flex min-h-100 items-center justify-center">
						در حال دریافت سبد خرید...
					</div>
				</main>

				<Footer />
			</>
		);
	}

	if (!cart || cart.items.length === 0) {
		return (
			<>
				<Header />

				<main className="container mx-auto flex max-w-7xl flex-1 px-4 pt-12">
					<div className="flex w-full flex-col items-center justify-center gap-6 rounded-xl border p-12">
						<ShoppingBag className="size-12 text-muted-foreground" />

						<h1 className="text-2xl font-bold">
							سبد خرید شما خالی است
						</h1>

						<Link href="/#products">
							<Button>مشاهده محصولات</Button>
						</Link>
					</div>
				</main>

				<Footer />
			</>
		);
	}

	return (
		<>
			<Header />

			<main
				className="
				container mx-auto
				max-w-7xl
				flex-1
				px-4
				pt-12
				pb-20
				">
				<div className="grid gap-8 lg:grid-cols-[1fr_360px]">
					<section className="space-y-4">
						<h1 className="text-3xl font-bold">سبد خرید</h1>

						<div className="space-y-4">
							{cart.items.map((item) => (
								<div
									key={item.id}
									className="
									flex
									items-center
									justify-between
									gap-4
									rounded-xl
									border
									p-4
									">
									<div className="space-y-2">
										<h3 className="font-semibold">
											{item.product_name}
										</h3>

										<p className="text-sm text-muted-foreground">
											{item.variant_label}
										</p>

										<p className="font-medium">
											{formatPrice(item.price)}
											{" تومان"}
										</p>
									</div>

									<div className="flex items-center gap-3">
										<Button
											size="icon"
											variant="outline"
											disabled={isUpdatingItem}
											onClick={() =>
												increaseQuantity(item.id)
											}>
											<Plus className="size-4" />
										</Button>

										<span className="min-w-8 text-center font-bold">
											{item.quantity.toLocaleString(
												"fa-IR",
											)}
										</span>

										<Button
											size="icon"
											variant="outline"
											disabled={isUpdatingItem}
											onClick={() =>
												decreaseQuantity(item.id)
											}>
											<Minus className="size-4" />
										</Button>

										<Button
											size="icon"
											variant="destructive"
											disabled={isRemovingItem}
											onClick={() => removeItem(item.id)}>
											<Trash2 className="size-4" />
										</Button>
									</div>
								</div>
							))}
						</div>
					</section>

					<aside
						className="
						h-fit
						rounded-xl
						border
						p-6
						space-y-6
						">
						<h2 className="text-xl font-bold">خلاصه سفارش</h2>

						<div className="flex justify-between">
							<span>تعداد کالا</span>

							<span>
								{cart.items_count.toLocaleString("fa-IR")}
							</span>
						</div>

						<div className="flex justify-between text-lg font-bold">
							<span>مبلغ کل</span>

							<span>
								{formatPrice(cart.total_price)}
								{" تومان"}
							</span>
						</div>

						<Button className="w-full" size="lg">
							ادامه ثبت سفارش
						</Button>
					</aside>
				</div>
			</main>

			<Footer />
		</>
	);
}

function formatPrice(price: number) {
	return new Intl.NumberFormat("fa-IR").format(price);
}
