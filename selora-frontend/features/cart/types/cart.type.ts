import { CartItem } from "./cart-item.type";

export type Cart = {
	id: string;
	session_key: string;
	items: CartItem[];
	items_count: number;
	total_price: number;
	created_at: Date;
	updated_at: Date;
};

export interface CartStore {
	items: CartItem[];

	setCart: (cart: Cart) => void;

	addItem: (item: CartItem) => void;

	setItems: (items: CartItem[]) => void;

	updateItemData: (item_id: string, data: Partial<CartItem>) => void;

	removeItem: (item_id: string) => void;

	updateQuantity: (item_id: string, quantity: number) => void;

	increaseQuantity: (item_id: string) => void;

	decreaseQuantity: (item_id: string) => void;

	getItemByVariantId: (variant_id: string) => CartItem | undefined;

	clear: () => void;

	hasItem: (item_id: string) => boolean;

	getItem: (item_id: string) => CartItem | undefined;

	totalItems: () => number;

	totalPrice: () => number;
}
