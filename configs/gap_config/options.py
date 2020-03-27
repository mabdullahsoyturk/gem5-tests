from optparse import OptionParser

def get_opts():
    parser = OptionParser()

    parser.add_option("--bench-path", help="Binary of the program to be simulated")
    parser.add_option("--input-path", help="Fault input file")
    parser.add_option("--output", help="Output", default="")
    parser.add_option("--cache-level", help="Cache Level", default="1")

    # Cache Options
    parser.add_option("--l1d-size", type="string", default="2kB")
    parser.add_option("--l1i-size", type="string", default="32kB")
    parser.add_option("--l2-size", type="string", default="2MB")
    parser.add_option("--l3-size", type="string", default="16MB")
    parser.add_option("--l1d-assoc", type="int", default=2)
    parser.add_option("--l1i-assoc", type="int", default=2)
    parser.add_option("--l2-assoc", type="int", default=8)
    parser.add_option("--l3-assoc", type="int", default=16)

    return parser.parse_args()