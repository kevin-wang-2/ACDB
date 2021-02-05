export interface StockModel {
  name: string;
  slots: Array<Array<string>>;
  rent: boolean;
}

type ProcessSlotFunc = (item: string) => string | Promise<string>;

export async function forEachSlots(stock: StockModel, cb: ProcessSlotFunc) {
  for (let first = 0; first < stock.slots.length; first++) {
    for (let second = 0; second < stock.slots[first].length; second++) {
      stock.slots[first][second] = await cb(stock.slots[first][second]);
    }
  }
}
