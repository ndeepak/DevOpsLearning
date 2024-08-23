### **Command-line Arguments in Bash**
#### **1. Handling Positional Parameters**
**Overview:**
- Positional parameters are the arguments passed to a Bash script when it is executed. These parameters are accessed within the script using special variables: `$0`, `$1`, `$2`, etc.
    - `$0` refers to the script's name.
    - `$1`, `$2`, ..., `$N` refer to the first, second, ..., Nth argument passed to the script.

**Example:**
```
#!/bin/bash
echo "Script Name: $0"
echo "First Argument: $1"
echo "Second Argument: $2"
```

**Running the Script:**
`./script.sh arg1 arg2`

**Output:**
```
Script Name: ./script.sh
First Argument: arg1
Second Argument: arg2
```
**Special Parameters:**

- `$#`: Number of arguments passed to the script.
- `$@`: All arguments passed to the script.
- `$*`: All arguments passed to the script as a single string.
- `$?`: Exit status of the last command.
- `$$`: Process ID of the script.
- `$!`: Process ID of the last background command.

**Example Using Special Parameters:**
```
#!/bin/bash
echo "Total Number of Arguments: $#"
echo "All Arguments: $@"
```
#### **2. Practice Using Arguments in Scripts**

**Example Script with Arguments:**
```
#!/bin/bash

if [ $# -lt 2 ]; then
  echo "Usage: $0 arg1 arg2"
  exit 1
fi

echo "Argument 1: $1"
echo "Argument 2: $2"

sum=$(( $1 + $2 ))
echo "Sum of arguments: $sum"
```

**Running the Script:**
`./script.sh 10 20`

**Output:**
```
Argument 1: 10
Argument 2: 20
Sum of arguments: 30
```

---
### **Arrays in Bash**
#### **1. Declare and Initialize Arrays**
**Overview:**

- Arrays in Bash are declared using the following syntax:
    `array_name=(element1 element2 element3)`
    

**Example:**
```
#!/bin/bash

# Declaring and initializing an array
fruits=("apple" "banana" "cherry")
```
- **Empty Array Declaration:**
    `empty_array=()`
    
- **Adding Elements to an Array:**
    `fruits+=("orange")  # Adding a single element`
    

#### **2. Access and Manipulate Array Elements**
**Accessing Elements:**
- Use the following syntax to access elements:   
```
echo ${fruits[0]}  # Access the first element
echo ${fruits[1]}  # Access the second element
```
    

**Looping Through Array Elements:**
- **Example:**
```
for fruit in "${fruits[@]}"; do
  echo $fruit
done
```

**Array Length:**
- **Example:**
    `echo "Number of fruits: ${#fruits[@]}"`
    

**Modifying Elements:**
- **Example:**
```
fruits[1]="blueberry"
echo "Updated array: ${fruits[@]}"
```
**Removing Elements:**
- **Example:**
```
fruits[1]="blueberry"
echo "Updated array: ${fruits[@]}"
```
#### **Putting It All Together:**
**Example Script Using Arrays:**
```
#!/bin/bash

fruits=("apple" "banana" "cherry")

# Adding elements
fruits+=("orange" "grape")

# Accessing elements
echo "First fruit: ${fruits[0]}"
echo "All fruits: ${fruits[@]}"

# Modifying elements
fruits[1]="blueberry"
echo "Updated fruits: ${fruits[@]}"

# Array length
echo "Number of fruits: ${#fruits[@]}"

# Looping through array
for fruit in "${fruits[@]}"; do
  echo "Fruit: $fruit"
done

# Removing an element
unset fruits[2]
echo "After removal: ${fruits[@]}"
```
**Running the Script:**
`./array_script.sh`

**Output:**
```
First fruit: apple
All fruits: apple banana cherry orange grape
Updated fruits: apple blueberry cherry orange grape
Number of fruits: 5
Fruit: apple
Fruit: blueberry
Fruit: cherry
Fruit: orange
Fruit: grape
After removal: apple blueberry orange grape
```

---
### **Conclusion**
Understanding command-line arguments and arrays in Bash is crucial for creating dynamic and flexible scripts. These concepts allow you to handle input parameters, store and manipulate lists of data, and automate repetitive tasks efficiently.