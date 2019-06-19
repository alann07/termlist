# Term List Analysis

## Design

Initially, my first thought was to use trie and manheap, until I found out that I can actually use python collections Counter and external BeautifulSoup lib.

Python collection Counter uses heap underneath it. Therefore, it runs fast.

BeautifulSoup is 3rd party tool which help retrieves pure text between html tags, i.e., the terms we are interested in.

Python Counter provides the solutions to both FREQUENCY and TOP commands.

For IN_ORDER checking, it requires 2 conditions sorting. I didn't find api to do it directly. Instead, I use python sort based on counter numbers. Then, write an algorithm to scan through the entire term list just once to decide in order or not.

## How to run the program

I use python 3 for this project. Unzip the tar and come to project root folder.

```
> pip install -r requirements.txt
> python process_termlist.py input.html commands.txt output.txt
```

## Runtime Complextity 

For the given input.html and commands.txt files, the running results are shown as below.

Loading input files took 7 miliseconds. For each commands, it took roughly 0.1 mileseconds per command.

Time complexity for the counter construction is O(n). Running FREQUENCY takes O(1). For TOP, as it needs sorting, it is O(nlogn)

Running IN_ORDER takes O(n), as it requires to search through the entire term list, but just once.

```
2019-06-18 12:20:14,078 - __main__ - INFO - Start processing
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command FREQUENCY
2019-06-18 12:20:14,085 - termlist_service - INFO - Executing command TOP
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - termlist_service - INFO - Executing command IN_ORDER
2019-06-18 12:20:14,086 - __main__ - INFO - processing complete. check result in output.txt

```

## Memory Usage

Loading the input files and contruct the counter take O(n) space.

## Assumptions / Limitations

* Only checked BeautifulSoup tool. Not sure whether there's more efficient one than this.
* Assume collections Counter also uses trie and maxheap
* Have not tried on very large input xml files. Need to check such performance.
