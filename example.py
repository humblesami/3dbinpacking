import time
from py3dbp import Packer, Item
from py3dbp.main import BinType


def packing_process():

    packer = Packer()
    # packer.add_item(Item('p1', 5, 2, 2, 1))
    products = [
        [5, 2, 5, 4],
        [6, 5, 3, 2],
        [7, 4, 4, 6],
        [5, 3, 5, 5],
        [8, 2, 2, 3],
        [4, 4, 3, 4],
        [8, 4, 4, 2],
        [4, 5, 4, 5],
        [9, 3, 4, 6],
        [5, 6, 2, 3],
    ]

    def add_bins():
        bin_types = [
            BinType('large', 20, 16, 6, 70.0),
            BinType('medium', 16, 16, 5, 50.0),
            BinType('small', 10, 10, 5, 40.0),
            BinType('x-small', 10, 5, 4, 30.0)
        ]
        packer.bin_types = bin_types

    def pack_items():
        max_width = 0
        max_height = 0
        max_depth = 0

        pc = 0
        for product in products:
            pc += 1
            to_pack = Item(f'p{pc-1}', product[0], product[1], product[2], product[3])
            if to_pack.height > max_height:
                max_height = to_pack.height
            if to_pack.depth > max_depth:
                max_depth = to_pack.depth
            if to_pack.width > max_width:
                max_width = to_pack.width
            packer.add_item(to_pack)
        max_dims = [max_width, max_height, max_depth]
        # packer.pack(bigger_first=True)
        packer.pack()
        return pc

    def show_packed_items():
        used_bin_types = {}
        for b in packer.bins:
            if used_bin_types.get(b.name):
                used_bin_types[b.name]['count'] += 1
                used_bin_types[b.name]['items'] += len(b.items)
            else:
                used_bin_types[b.name] = {"count": 1, 'items': len(b.items)}

        for b in packer.bins:
            if not b.items:
                continue

            print("\nbox => " + b.bin_str())
            print(f"FITTED ITEMS: {len(b.items)}")
            for product in b.items:
                print("====> ", product.string())

            if not b.unfitted_items:
                continue

        print("\nUsed bins summary")
        for bin_type in used_bin_types:
            print(f"{bin_type.title()} {used_bin_types[bin_type]['count']}, items={used_bin_types[bin_type]['items']}")

    def increase_products(original, mul):
        sn = 1
        res = []
        while sn <= mul:
            res = res + original
            sn += 1
        return res

    products = increase_products(products, 3)
    add_bins()

    start = time.time()
    pack_items()
    end = time.time()
    time_taken = f"\nTime taken with {len(products)} items => {end - start}"

    show_packed_items()
    if packer.unfit_items:
        print("\nCompletely Unfit Items")
        for item in packer.unfit_items:
            print("==>", item.detailed_str())

    print(time_taken)


packing_process()
