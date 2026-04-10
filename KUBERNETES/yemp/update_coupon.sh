#!/bin/bash

# Input file
input_file="links"
temp_file="links.tmp"

# Remove the first 3 lines (they contain just the coupon code)
tail -n +4 "$input_file" > "$temp_file"

# Process each line
while IFS= read -r line; do
    if [[ $line =~ ^https://.*udemy\.com/course/.* ]]; then
        # Remove existing coupon code if present
        line=$(echo "$line" | sed 's/\?couponCode=[^/]*$//')
        # Add new coupon code
        echo "${line}/?couponCode=NOV9FREE"
    else
        echo "$line"
    fi
done < "$temp_file" > "links.new"

# Add the coupon code identifier at the top of the new file
echo "NOV9FREE" > "$input_file"
echo "" >> "$input_file"
echo "/?couponCode=NOV9FREE" >> "$input_file"

# Append the processed links
cat "links.new" >> "$input_file"

# Clean up temporary files
rm "$temp_file" "links.new"

echo "URLs have been updated with the new coupon code."