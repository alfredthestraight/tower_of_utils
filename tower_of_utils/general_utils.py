import pandas as pd
import itertools


def dir_(obj, substring: str = '') -> pd.DataFrame:
    """List attributes/methods of an object filtered by substring, returned as a numpy array of names."""
    returned_values = [x for x in dir(obj) if substring in x]
    return pd.DataFrame(columns=returned_values).columns.values


def flatten_list_of_lists(lst):
    return list(itertools.chain(*lst))


def find_all_paths_leading_to_key(
    d: dict, target_key: str, current_path: str = None
) -> list[str]:
    """
    Search through a nested dictionary (or list of dictionaries) to
    find all the paths that lead to a specified key
    """
    if current_path is None:
        current_path = []
    paths = []
    if isinstance(d, dict):
        for key, value in d.items():
            new_path = current_path + [key]
            if key == target_key:
                paths.append(new_path)
            paths.extend(find_all_paths_leading_to_key(value, target_key, new_path))
    elif isinstance(d, list):
        for index, item in enumerate(d):
            new_path = current_path + [index]
            paths.extend(find_all_paths_leading_to_key(item, target_key, new_path))
    return paths


def which_is_true(lst: list) -> list:
    """Which values in a list are True"""
    return [i for i, x in enumerate(lst) if x]


def is_price(st):
    def is_price_symbol(st, sep=",", dec="."):

        if not st.replace(dec, "").replace(sep, "").isdigit():
            return False

        if st.isdigit():
            return True

        str_splt = st.split(dec)

        if len(str_splt) >= 3:
            return False

        if len(str_splt) == 2:
            if str_splt[0] == "" or str_splt[1] == "" or not str_splt[1].isdigit():
                return False

        str_int_part = str_splt[0]

        str_int_part_list = str_int_part.split(sep)

        if len(str_int_part_list) == 1:
            return True

        str_int_part_list_2 = str_int_part_list[1: len(str_int_part_list)]
        return (
            min([len(sec) == 3 for sec in str_int_part_list_2])
            and len(str_int_part_list[0]) <= 3
        )

    # pdb.set_trace()
    currency_list = ["MOP$", "Ptas", "so'm", "د. م", "AED", "AFN", "ALL", "AMD", "ANG", "AOA",
                     "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD",
                     "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF",
                     "CKD", "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "din", "DJF",
                     "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP",
                     "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK",
                     "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD",
                     "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KPW", "KRW", "KWD", "KYD",
                     "KZT", "LAK", "LBP", "lei", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA",
                     "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN",
                     "NAD", "Nfk", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK",
                     "PHP", "PKR", "PLN", "PND", "PRB", "PYG", "QAR", "RD$", "RON", "RSD", "RUB",
                     "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SLS", "SOS",
                     "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY",
                     "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VES", "VND",
                     "VUV", "WST", "XAF", "XCD", "XOF", "XPF", "YER", "ZAR", "ZMW", "ден", "дин",
                     "сўм", "ج.س", "ج.م", "د.ا", "د.ب", "د.ت", "د.ج", "د.ك", "د.م", "ر.ع", "ر.ق",
                     "ر.ي", "ع.د", "ل.د", "ل.س", "ل.ل", "Ar", "Br", "Bs", "C$", "Db", "Fr", "Ft",
                     "Kč", "KM", "kn", "kr", "Ks", "Kz", "Le", "MK", "MT", "Nu", "R$", "RM", "Rp",
                     "Rs", "Sh", "Sl", "T$", "UM", "Vt", "ZK", "zł", "ЅМ", "лв", "դր", "रू", "ரூ",
                     "රු", "$", "₾", "£", "¥", "₱", "﷼", "₣", "₭", "₦", "₧", "₨", "₩", "₮",
                     "€", "฿", "₡", "৳", "៛", "؋", "₲", "₴", "₵", "₪", "₫", "₹", "₺", "D", "ƒ",
                     "G", "K", "L", "m", "P", "Q", "R", "T", "р", "с", "ރ", "元", "円",
                     ]
    i = 0
    currency_identified = False
    while i < len(currency_list) and not currency_identified:
        currency_identified = currency_identified | (currency_list[i] in st)
        i += 1

    if not currency_identified:
        return False

    st = st.replace(currency_list[i], "").rstrip().lstrip()

    return (
        is_price_symbol(st, sep=",", dec=".")
        or is_price_symbol(st, sep=".", dec=",")
        or is_price_symbol(st, sep=" ", dec=",")
    )
