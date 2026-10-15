import argparse
import logging

from .export import save_to_csv, save_to_json
from .floridabar import FloridaBar, FloridaBarSearchError


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the Florida Bar member directory.")
    parser.add_argument("--bar-number", help="Search by bar number (ignores other filters).")
    parser.add_argument("--first-name", default="", help="Filter by first name.")
    parser.add_argument("--last-name", default="", help="Filter by last name.")
    parser.add_argument("--firm", default="", help="Filter by law firm.")
    parser.add_argument("--output", help="Path to write results to (.csv or .json).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    client = FloridaBar()
    try:
        client.search(
            bar_number=args.bar_number,
            first_name=args.first_name,
            last_name=args.last_name,
            law_firm=args.firm,
        )
    except FloridaBarSearchError as e:
        parser.error(str(e))
        return

    for lawyer in client.lawyers:
        print(lawyer)

    if args.output:
        if args.output.endswith(".json"):
            save_to_json(client.lawyers, args.output)
        else:
            save_to_csv(client.lawyers, args.output)
        print(f"Wrote {len(client.lawyers)} result(s) to {args.output}")
