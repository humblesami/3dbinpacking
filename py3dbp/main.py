from .constants import RotationType, Axis
from .auxiliary_methods import intersect, set_to_decimal

DEFAULT_DECIMALS = 1
START_POSITION = [0, 0, 0]


class Item:
    def __init__(self, name, width, height, depth, weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.volume = width * height * depth
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_DECIMALS

    def get_position(self):
        pos = self.position
        return f'{pos[0]},{pos[2]},{pos[2]}'

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.weight = set_to_decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        res = f"{self.name}, {self.weight} gm, {self.volume}"
        return res

    def detailed_str(self):
        dimensions = f"{self.width}, {self.height}, {self.depth}"
        rotation = ''
        if self.rotation_type != 1:
            rotation = f'\trot:{self.rotation_type}'
        pos_rot_vol = f"\tpos:{self.get_position()}\t\tvol:{self.get_product_volume_str()}{rotation}"
        details = f"{self.name} {dimensions}, weight:{self.weight}, {pos_rot_vol}"
        return details

    def get_product_volume_str(self):
        return set_to_decimal(self.width * self.height * self.depth, self.number_of_decimals)

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension


class Bin:
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        volume = width * height * depth
        self.volume = volume
        self.max_weight = max_weight
        self.items = []
        self.unfitted_items = []
        self.number_of_decimals = DEFAULT_DECIMALS

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.max_weight = set_to_decimal(self.max_weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def bin_str(self):
        dimensions = f"{self.width},{self.height},{self.depth}"
        products_volume = self.get_products_volume()
        res = f"{self.name} => vol_detail: {dimensions},\tmax_weight:{self.max_weight},\tvol:{self.get_volume()}"
        res += f"\tproducts_volume:{products_volume}"
        return res

    def get_volume(self):
        return set_to_decimal(self.volume, self.number_of_decimals)

    def get_total_weight(self):
        total_weight = 0
        for item in self.items:
            total_weight += item.weight
        return set_to_decimal(total_weight, self.number_of_decimals)

    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot
        for i in range(0, len(RotationType.ALL)):
            if i > 0:
                break
            item.rotation_type = i
            dimension = item.get_dimension()
            nmw = self.width < pivot[0] + dimension[0]
            nmh = self.height < pivot[1] + dimension[1]
            nmd = self.depth < pivot[2] + dimension[2]
            if nmw or nmh or nmd:
                continue
            fit = True
            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break
            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                self.items.append(item)

            if not fit:
                item.position = valid_item_position
            return fit
        if not fit:
            item.position = valid_item_position

        return fit

    def get_products_volume(self):
        volume = 0
        for item in self.items:
            volume += item.volume
        return volume


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, box):
        return self.bins.append(box)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)

    @classmethod
    def pack_to_bin(cls, box, item):
        fitted = False
        if not box.items:
            response = box.put_item(item, START_POSITION)
            if not response:
                box.unfitted_items.append(item)
            return
        for axis in range(0, 3):
            items_in_bin = box.items
            for ib in items_in_bin:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]

                if box.put_item(item, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            box.unfitted_items.append(item)

    def pack(self, bigger_first=False, distribute_items=False, number_of_decimals=DEFAULT_DECIMALS):
        for box in self.bins:
            box.format_numbers(number_of_decimals)

        for item in self.items:
            item.format_numbers(number_of_decimals)

        # self.bins.sort(key=lambda bx: bx.get_volume(), reverse=bigger_first)
        self.items.sort(key=lambda it: it.volume, reverse=bigger_first)

        prev_box = None
        for box in self.bins:
            for item in self.items:
                self.__class__.pack_to_bin(box, item)

            if distribute_items:
                for item in box.items:
                    self.items.remove(item)
            box.items.sort(key=lambda it: it.name)
            if prev_box:
                if prev_box.items == box.items:
                    prev_box.items.items = []

            prev_box = box
            box.unfitted_items.sort(key=lambda it: it.name)
            if not box.unfitted_items:
                break
