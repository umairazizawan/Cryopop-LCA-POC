"""Entry point for the CryoPop Brightway proof-of-concept."""

from workflow import format_results, run_comparison


if __name__ == "__main__":
    results = run_comparison()
    print("\nCryoPop Brightway LCA comparison\n")
    print(format_results(results))
    print("\nResults were saved to the results/ folder.")
