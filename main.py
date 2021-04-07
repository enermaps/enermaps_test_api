import settings
from scen_01 import scenario_01

if __name__ == "__main__":
    # Initialize the global variables once
    settings.init()

    # TODO call the different scenario
    scenario_01.scenario_01()
