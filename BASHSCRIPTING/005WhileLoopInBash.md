### **While Loop in Bash**
#### **1. Overview of While Loop**
A `while` loop in Bash is a control flow statement that allows code to be executed repeatedly based on a given boolean condition. The loop continues until the condition evaluates to false. This is useful when you want to perform repetitive tasks or iterate over data until a certain condition is met.
##### **Basic Syntax:**
```
while [ condition ]; do
    # Code to execute while the condition is true
done
```
- **`while`**: Starts the loop.
- **`[ condition ]`**: The condition is evaluated before each iteration. As long as this condition is true, the loop continues.
- **`do`**: Indicates the start of the block of code to be executed.
- **`done`**: Ends the loop block.
---
#### **2. Common Use Cases**
- **Counting or Iterating:** You can use a while loop to count numbers or iterate over a sequence.
- **Waiting for a Condition:** The loop can be used to repeatedly check if a condition is met (e.g., waiting for a file to exist).
- **Reading Files:** While loops are often used to read lines from a file one by one.
---
#### **3. Practical Examples**
##### **Example 1: Simple Counting Loop**
```
#!/bin/bash

counter=1

while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done
```
**Explanation:**
- **`counter=1`**: Initializes the counter variable to 1.
- **`while [ $counter -le 5 ]; do`**: The loop runs as long as `counter` is less than or equal to 5.
- **`echo "Counter: $counter"`**: Prints the value of the counter.
- **`((counter++))`**: Increments the counter by 1 after each iteration.
##### **Example 2: Infinite Loop (with a Break Condition)**
```
#!/bin/bash

while true; do
    echo "This will run forever unless we stop it."
    sleep 1  # Pauses the loop for 1 second
    break    # Exits the loop
done
```
**Explanation:**
- **`while true; do`**: The loop runs indefinitely because `true` is always true.
- **`sleep 1`**: Pauses the loop for 1 second in each iteration.
- **`break`**: Exits the loop, preventing an infinite loop.
##### **Example 3: Reading a File Line by Line**
```
#!/bin/bash

file="example.txt"

while IFS= read -r line; do
    echo "Line: $line"
done < "$file"
```
**Explanation:**
- **`file="example.txt"`**: Specifies the file to read.
- **`while IFS= read -r line; do`**: Reads the file line by line, storing each line in the `line` variable.
- **`echo "Line: $line"`**: Prints each line of the file.
- **`done < "$file"`**: Redirects the file's content to the loop.
##### **Example 4: Waiting for a File to Appear**
```
#!/bin/bash

file="/tmp/myfile.txt"

while [ ! -f "$file" ]; do
    echo "Waiting for $file to exist..."
    sleep 2
done

echo "$file exists!"
```
**Explanation:**
- **`file="/tmp/myfile.txt"`**: Defines the file to check.
- **`while [ ! -f "$file" ]; do`**: The loop runs as long as the file does not exist.
- **`echo "Waiting for $file to exist..."`**: Prints a message indicating the wait.
- **`sleep 2`**: Pauses the loop for 2 seconds between checks.
- **`echo "$file exists!"`**: Prints a message when the file is found.
---
#### **4. Advanced Usage**
##### **Example 5: Using a Counter with a Condition**
```
#!/bin/bash

counter=0
max_count=10

while [ $counter -lt $max_count ]; do
    echo "Current count is $counter"
    ((counter++))
done
```
**Explanation:**
- **`counter=0`**: Initializes the counter to 0.
- **`max_count=10`**: Sets a maximum count.
- **`while [ $counter -lt $max_count ]; do`**: The loop runs until the counter reaches 10.
- **`echo "Current count is $counter"`**: Prints the current counter value.
- **`((counter++))`**: Increments the counter by 1 in each iteration.
---
#### **5. Conclusion**
The `while` loop is a powerful tool in Bash scripting, enabling you to perform repetitive tasks efficiently. Whether you're iterating through numbers, reading files, or waiting for a condition to be met, the `while` loop provides a flexible way to handle repetitive tasks in your scripts. Understanding its structure and use cases allows you to write more dynamic and effective Bash scripts.