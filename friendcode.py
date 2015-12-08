from util import hook
import re, dataset

try:
    db = dataset.connect('sqlite:///friendcodes.db')
    table = db['friendcodes']
except Exception as e:
    raise e

# Usage:
#    .friendcode or .fc will work.
#
#    .fc Displays your friendcode if set.
#    .fc [code] Sets your friendcode
#    .fc [nick] Displays the friendcode for another person.
#
#    .friendcodedelete or .fcdelete or .fcdel
#
#    .fcdel Removes your friendcode.

r = re.compile('^\d{4}-\d{4}-\d{4}$')

@hook.command('fc')
@hook.command
def friendcode(inp, nick=''):
    if inp:
        target = table.find_one(nickname=inp)
        if r.match(inp):
            table.upsert(dict(nickname=nick, code=inp), ['nickname'])
            return "Friendcode set to {}".format(inp)
        else:
            if target:
                return "{}'s friendcode is {}".format(inp, target['code'])
    else:
        target = table.find_one(nickname=nick)
        if target:
            return target['code']

@hook.command('fcdel')
@hook.command('fcdelete')
@hook.command
def friendcodedelete(inp, nick=''):
    target = table.find_one(nickname=nick)
    if target:
        table.delete(nickname=nick)
        return "Your friendcode has been deleted"
    else:
        return "You do not have a friendcode"
