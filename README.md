# Asset_Liability_Optimization4
This program is a model for asset and liability optimization. The program is created in a collaboration project between Oracle and the Bank of China. The computation boundaries are designed by Bank of China financial engineers and business experts.

## Running the demo program
The main method which optimizes results for multiple years is stored in the "main.py" file. However, it requires a rading of Oracle sql Database which people not working on this project cannot gain access. To demonstrate our model, I wrote a simplified program of optimizing the result of 1 year with hypothetical scenario parameters. Enter 

```sh
python3 main_annual.py
  ```
The result will be printed, which includes all boundaries computation and assset&liability computation after optimization. The data input and processing is stored in the "input_annual.py" file. The simplified computation description is written in the word document. However, I am not a business major, so it is difficult for me to translate in English. However, computation can be understood through the code. 

## Tree structured explained
In accounting for the constantly changing banking scenarios which produces different variables to optimize, we observed that all variables follow a hierarchical structure, so we created a tree structure so that computation are done with reference to the tree. This structure significantly reduces workload for every iteration of the project, and will be applied in future versions. Since the algorithm package requires that every variable is stored in an ordered array, each node of the tree stores the array index slice of the variables. When computation functions pertaining to the business domain such as LCR and NII requires certain variables, we simplify enter the path to the variable node and retrieve its index slice. The following diagram is a simplified model for the structure. For example, to retrieve the term1 of liabilities data, we go enter the node and retrieve (4, 6) slice, which corresponds to array [1500, 1700]. 

![alt text](https://github.com/Muhanzhang10/Asset_Liability_Optimization4/blob/main/tree_example.png)



## Optimization 
Mathematically, the program deals with non linear optimization of the form
![alt text](https://github.com/Muhanzhang10/Asset_Liability_Optimization4/blob/main/Optimization%20problem%20description.png)

This program employs the scipy optimization model. Specifically, we used trust-constr optimization algorithm after testing using a tiral-error method and concluded that it yields the best result. 
