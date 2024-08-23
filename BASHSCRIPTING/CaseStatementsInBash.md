### **Case Statements in Bash**
#### **1. Overview of Case Statements**
The `case` statement in Bash is a powerful control structure used to execute different blocks of code based on the value of a variable or expression. It's similar to the `switch` statement in other programming languages and is particularly useful when you have multiple possible conditions to check and handle.
##### **Basic Syntax:**
```
case $variable in
    pattern1)
        # Code to execute if variable matches pattern1
        ;;
    pattern2)
        # Code to execute if variable matches pattern2
        ;;
    *)
        # Code to execute if no patterns match
        ;;
esac
```
- **`case $variable in`**: Starts the case statement, with `$variable` being the value to match against different patterns.
- **`pattern1)`**: A pattern to match the variable against. If it matches, the corresponding block of code is executed.
- **`;;`**: Ends the block of code for a pattern.
- **`*)`**: The default case, executed if none of the specified patterns match.
- **`esac`**: Ends the case statement.
---
#### **2. Common Use Cases**
- **Handling User Input:** Case statements can be used to handle different user inputs, such as menu options.
- **File Type Checks:** You can use a case statement to perform different actions based on file extensions.
- **Conditional Logic:** Case statements are useful for implementing complex conditional logic with multiple possible outcomes.
---
#### **3. Practical Examples**
##### **Example 1: Basic Case Statement for User Input**
```
#!/bin/bash

echo "Enter a number between 1 and 3: "
read number

case $number in
    1)
        echo "You chose one."
        ;;
    2)
        echo "You chose two."
        ;;
    3)
        echo "You chose three."
        ;;
    *)
        echo "Invalid choice."
        ;;
esac
```
**Explanation:**
- **`case $number in`**: Starts the case statement, matching the user's input against the patterns.
- **`1)`**, **`2)`**, **`3)`**: Each case corresponds to a possible user input.
- **`*)`**: The default case, handling any input that doesn't match the specified patterns.
##### **Example 2: Handling File Extensions**
```
#!/bin/bash

filename="example.txt"

case $filename in
    *.txt)
        echo "Text file"
        ;;
    *.jpg)
        echo "JPEG image"
        ;;
    *.sh)
        echo "Shell script"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac
```
**Explanation:**
- **`*.txt)`**, **`*.jpg)`**, **`*.sh)`**: The case statement matches the file's extension and executes the corresponding block of code.
- **`*)`**: The default case, handling any file extension that isn't explicitly defined.

##### **Example 3: Case Statement with Multiple Patterns**
```
#!/bin/bash

day="Saturday"

case $day in
    "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday")
        echo "Weekday"
        ;;
    "Saturday"|"Sunday")
        echo "Weekend"
        ;;
    *)
        echo "Unknown day"
        ;;
esac
```
**Explanation:**
- **`"Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday")`**: Multiple patterns can be grouped together to execute the same block of code.
- **`"Saturday"|"Sunday")`**: Matches either "Saturday" or "Sunday" to execute the block for weekends.
---
#### **4. Advanced Usage**
##### **Example 4: Case Statement with Regular Expressions**
```
#!/bin/bash

string="This is a test."
case $string in
    *test*)
        echo "The string contains the word 'test'."
        ;;
    *example*)
        echo "The string contains the word 'example'."
        ;;
    *)
        echo "No match found."
        ;;
esac
```
**Explanation:**
- **`*test*)`**, **`*example*)`**: The case statement matches patterns using wildcards, checking if the string contains specific words.
- **`*)`**: The default case, handling any string that doesn't match the specified patterns.

##### **Example 5: Using Case Statements in Functions**
```
#!/bin/bash

check_os() {
    os_name=$1
    case $os_name in
        "Linux")
            echo "You are using Linux."
            ;;
        "Mac")
            echo "You are using macOS."
            ;;
        "Windows")
            echo "You are using Windows."
            ;;
        *)
            echo "Unknown operating system."
            ;;
    esac
}

check_os "Linux"
```
**Explanation:**
- **`check_os()`**: A function that takes the operating system name as an argument.
- **`case $os_name in`**: The case statement matches the argument against different OS names and executes the corresponding block of code.
---
#### **5. Conclusion**
The `case` statement is a flexible and efficient way to handle multiple conditions in Bash scripts. By using case statements, you can simplify complex conditional logic, making your scripts more readable and easier to maintain. Whether you're processing user input, checking file types, or implementing conditional logic, the `case` statement is an essential tool for any Bash script.

---

