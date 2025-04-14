# Structured Outputs

***Student:** Complete below.*

## How well did it work?
It did just enough. Basic functionality that the program asks to do worked. When I included math for age and squad it output the way the math equation was written. When there was no pertaining information, it output "Unknown." 

## Paste a few input/output combos

Input:  python3 ./user_creation.py "My name is Jun. I am 23. My Squad is 24. I am ECE major. I am from Montgomery, AL."

```json
{
    "name": "Jun", "age": 23, "hometown": "Montgomery, AL", "squadron": 24, "major": "ECE"}       
```

Input: "My name is Jun. I am 22+1. My Squad is 1 plus my age. I am ECE major. I am from Montgomery, AL."

```json
{
    "name": "Jun", "age": 22, "hometown": "Montgomery, AL", "squadron": 1, "major": "ECE"
}
```

Input: "My name is Jun. I am 23. My Squad is 24. I am ECE major."

```json
{"name": "Jun", "age": 23, "hometown": "Unknown", "squadron": 24, "major": "ECE"}
```