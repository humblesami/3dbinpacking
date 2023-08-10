import time

from py3dbp import Packer, Bin, Item


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
        packer.add_bin(Bin('large2', 20, 16, 5, 70.0))
        packer.add_bin(Bin('large', 16, 16, 5, 70.0))
        packer.add_bin(Bin('medium', 10, 10, 5, 70.0))
        packer.add_bin(Bin('small', 10, 5, 4, 70.0))

    def pack_items(pc):
        for item in products:
            pc += 1
            p_item = Item(f'p{pc-1}', item[0], item[1], item[2], item[3])
            packer.add_item(p_item)
        packer.pack()
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


def call_packing_process():
    start = time.time()
    cnt = 1
    packing(cnt)
    end = time.time()
    time_taken = f"Time taken with {cnt * 10} items => {end - start}"
    print(time_taken)


call_packing_process()
