import time

from py3dbp import Packer, Bin, Item
from py3dbp.main import BinType


def packing(complexity):

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

    def pack_items(pc):
        max_width = 0
        max_height = 0
        max_depth = 0
        for item in products:
            pc += 1
            p_item = Item(f'p{pc-1}', item[0], item[1], item[2], item[3])
            if p_item.height > max_height:
                max_height = p_item.height
            if p_item.depth > max_depth:
                max_depth = p_item.depth
            if p_item.width > max_width:
                max_width = p_item.width
            packer.add_item(p_item)
        max_dims = [max_width, max_height, max_depth]
        packer.pack(max_dims)
        return pc

    def show_packed_items():
        for b in packer.bins:
            if not b.items:
                continue

            print("\n\nbox => " + b.bin_str())
            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())

            if not b.unfitted_items:
                continue
            print("UNFITTED ITEMS:")
            for item in b.unfitted_items:
                print("====> ", item.detailed_str())

    add_bins()
    cnt = 0
    while cnt < complexity:
        pack_items(cnt * 10)
        cnt += 1
    show_packed_items()
    print("\nCompletely Unfit Items")
    for item in packer.unfit_items:
        print("==>", item.detailed_str())


def call_packing_process():
    start = time.time()
    cnt = 1
    packing(cnt)
    end = time.time()
    time_taken = f"Time taken with {cnt * 10} items => {end - start}"
    print(time_taken)


call_packing_process()
