#!/bin/bash

directory="environment"
output_file=".env"

if test -f "$output_file"; then
  rm .env
  echo "Remove previous .env file: $output_file"
fi

for file in "$directory"/*
do
  printf "\n\n# $file\n\n" >> "$output_file"
  cat "$file" >> "$output_file"
done

echo "Create .env file: $output_file"