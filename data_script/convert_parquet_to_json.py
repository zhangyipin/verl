#!/usr/bin/env python3

import argparse
import os

import pandas as pd


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Convert a parquet file to JSON or JSONL.")
	parser.add_argument("input", help="Path to the input parquet file.")
	parser.add_argument("output", help="Path to the output .json or .jsonl file.")
	parser.add_argument(
		"--indent",
		type=int,
		default=2,
		help="Indentation for .json output. Ignored for .jsonl. Default: 2.",
	)
	return parser.parse_args()


def convert_parquet_to_json(input_path: str, output_path: str, indent: int) -> None:
	input_suffix = os.path.splitext(input_path)[1].lower()
	output_suffix = os.path.splitext(output_path)[1].lower()

	if input_suffix != ".parquet":
		raise ValueError(f"Input file must be a .parquet file: {input_path}")
	if output_suffix not in {".json", ".jsonl"}:
		raise ValueError(f"Output file must be a .json or .jsonl file: {output_path}")

	dataframe = pd.read_parquet(input_path)

	os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
	if output_suffix == ".jsonl":
		dataframe.to_json(output_path, orient="records", lines=True, force_ascii=False)
	else:
		dataframe.to_json(output_path, orient="records", indent=indent, force_ascii=False)

	print(f"Converted {len(dataframe)} rows: {input_path} -> {output_path}")


def main() -> None:
	args = parse_args()
	convert_parquet_to_json(args.input, args.output, args.indent)


if __name__ == "__main__":
	main()
