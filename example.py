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
        [5, 3, 6, 5],
        [8, 2, 2, 3],
        [4, 4, 3, 4],
        [8, 4, 4, 2],
        [4, 5, 4, 5],
        [9, 3, 5, 6],
        [5, 6, 2, 3],
    ]

    def add_bins():
        bin_types = [
            BinType('large2', 20, 16, 6, 70.0),
            BinType('large', 16, 16, 5, 70.0),
            BinType('medium', 10, 10, 5, 70.0),
            BinType('small', 10, 5, 4, 70.0)
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
        packer.pack(max_dims)
        return pc

    def show_packed_items():
        for b in packer.bins:
            if not b.items:
                continue

            print("\nbox => " + b.bin_str())
            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())

            if not b.unfitted_items:
                continue
            print("UNFITTED ITEMS:")
            for item in b.unfitted_items:
                print("====> ", item.detailed_str())

    add_bins()

    sn = 1
    en = 16
    originals = products
    while sn < en:
        products = products + originals
        sn += 1

    start = time.time()
    pack_items()
    end = time.time()
    time_taken = f"\nTime taken with {en * 10} items => {end - start}"

    show_packed_items()
    print("\nCompletely Unfit Items")
    for item in packer.unfit_items:
        print("==>", item.detailed_str())

    print(time_taken)


packing_process()
