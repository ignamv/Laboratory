from pint import UnitRegistry
Q_ = UnitRegistry().Quantity

def toUnits(units):
    """Return function that parses a string to a Quantity with the given units

    Use for command line argument parsing, for example

    parser = argparse.ArgumentParser()
    parser.add_argument('--pulse_width', type=toUnits('fs'), default=Q_(40, 'fs'))
    """
    return lambda s: Q_(s).to(units)

