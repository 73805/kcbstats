from utilities import openPkl
from utilities import saveJson


def jsonify():

    contests = openPkl("contests")
    contests_basic = openPkl("contests_basic")
    teams = openPkl("teams")
    states = openPkl("states")

    saveJson(contests, "contests_updated")
    saveJson(contests_basic, "contests_basic_updated")
    saveJson(teams, "teams_updated")
    saveJson(states, "states_updated")
    print "saved all Json"
