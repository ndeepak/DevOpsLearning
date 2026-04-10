#!/bin/bash

# Usage: ./add_coupon.sh input.txt output.txt
# Example: ./add_coupon.sh udemy_links.txt udemy_links_with_coupon.txt

input="$1"
output="$2"
couponCode="NOV9FREE"

if [[ -z "$input" || -z "$output" ]]; then
    echo "Usage: $0 input.txt output.txt"
    exit 1
fi

# Make sure output file is empty before writing
> "$output"

while IFS= read -r line; do
    # Skip empty lines
    if [[ -z "$line" ]]; then
        echo "" >> "$output"
        continue
    fi

    # If line already has a couponCode parameter, leave it unchanged
    if [[ "$line" == *"couponCode="* ]]; then
        echo "$line" >> "$output"
    # If it's a valid Udemy course link, append coupon code
    elif [[ "$line" == *"https://www.udemy.com/course/"* ]]; then
        echo "${line%/}/?couponCode=${couponCode}" >> "$output"
    # Otherwise just copy as-is (e.g., "NOV9FREE" line itself)
    else
        echo "$line" >> "$output"
    fi
done < "$input"

echo "✅ Done! Updated links saved to: $output"
