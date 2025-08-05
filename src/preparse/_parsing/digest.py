
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *
from preparse._parsing.Item import *
from preparse._parsing.utils import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["digest"]



def digest(items:list[Item], /, *, parser:"PreParser"):
    items = digest_group(list(items), group=parser.group)
    items = digest_order(list(items), order=parser.order)
    items = digest_special(list(items), special=parser.special)
    items = digest_starvation(list(items))
    return items


def digest_group(items:list[Item], /, *, group:Group):
    if group == Group.MINIMIZE:
        items = digest_group_min(list(items))
    if group == Group.MAXIMIZE:
        items = digest_group_max(list(items))
    return items

def digest_group_max(items:list[Item])->list[Item]:
    ans:list[Item] = list()
    for i, a in enumerate(items):
        if i == 0:
            ans.append(a)
            continue
        if (ans[-1].value is None) and ans[-1].isgroup() and a.isgroup():
            a.key = ans.pop().key + a.key
            ans.append(a)
    return items

def digest_group_min(items:list[Item])->list[Item]:
    ans:list[Item] = list()
    for a in items:
        ans += ungroup(a)
    return ans

def ungroup(item:Item)->list[Item]:
    if not item.isgroup():
        return [item]
    ans:list[Item] = list()
    for x in item.key:
        if x == "-":
            ans[-1].key += x
        else:
            ans.append(Item(key=x))
    item.key = ans.pop().key
    ans.append(item)
    return ans


def digest_order(items:list[Item], /, *, order:Order):
    if order == Order.PERMUTE:
        options:list = [item for item in items if item.isoption()]
        nonoptions:list = [item for item in items if not item.isoption()]
        return options + nonoptions
    return items


def digest_special(items:list[Item], /, *, special:Special):
    if special == Special.MAXIMIZE:
        j:int=len(items)-1
        while j >= 0:
            if items[j].isspecial():
                return items
            if not items[j].ispositional():
                break
            j-=1
        items.insert(j+1, Item())
        return items
    if special == Special.MINIMIZE:
        j:int=len(items)-1
        while j >= 0:
            if items[j].key is not None:
                return items
            if items[j].value is None:
                items.pop(j)
                return items
            if items[j].value != "-" and items[j].value.startswith("-"):
                return items
            j -= 1
        
def digest_starvation(items:list[Item], /,*, parser:"PreParser") -> list[Item]:
    j:int=0
    while j < len(items):
        if items[j].isstarving():
            break
        j += 1
    if j + 1 > len(items):
        return items
    if j + 1 == len(items):
        items[j].equal = False
        return items
    if items[j+1].value is not None:
        items[j].value = items.pop(j+1).value
        items[j].equal = parser.remainder == Remainder.MAXIMIZE
        return items
    if parser.special == Special.MAXIMIZE:
        items[j].value = "--"
        items[j].equal = parser.remainder == Remainder.MAXIMIZE
        return items
    
    